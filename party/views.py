from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for)
from flask import session
import twilio.twiml
from twilio.rest import TwilioRestClient
import os
import pdb
import json
from party import *
from user.models import *
from flask.ext.login import login_user, logout_user, current_user, login_required


party = Blueprint('party', __name__, template_folder="")

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@party.route('/')
@login_required
def index():
    u = g.user
    return render_template('templates/party.html', parties = u.parties, user=u)

@party.route('/do/newparty', methods=['POST'])
def new_party():
    u = g.user
    party_name = request.form['party-name']
    party_code = request.form['party-code']
    p = Party(name=party_name, code=party_code, user=u)
    db.session.add(p)
    db.session.commit()
    sl = Song_List(party=p)
    db.session.add(sl)
    db.session.commit()
    return redirect(url_for('party.listen'))

@party.route("/do/get_song_id", methods=['POST'])
def get_song_id():
    respDict = gettrackinfo(request.form['songid'])
    return respDict[0]

@party.route('/listen', methods=['GET', 'POST'])
@login_required
def listen():
    u = g.user
    if request.method == 'POST':
        room = request.form['party-code']
    else:
        if u.parties == []:
            return redirect(url_for('party.index', user=u))
        room = u.parties[-1].code
    return render_template('templates/listen.html', room=room, user=u)

@party.route('/do/get_first_song', methods=['POST'])
def return_first():
    room = request.form['partycode']
    res = Party.query.filter(Party.code == room).first().song_lists[0].songs
    if res == []:
        return getRandomTrack()
    else:
        retID = res[0].uid
        db.session.delete(Party.query.filter(Party.code == room).first().song_lists[0].songs[0])
        db.session.commit()
        return retID

@party.route("/textrequest", methods=['GET', 'POST'])
def text_request():
    party = session.get('party')

    messages = client.messages.list() 
    message = messages[0].body

    # if we start the message with the code setparty, we want to reset the party that the user is attending
    if message[0:8].lower() == 'setparty':
        message = message[8:].strip()
        session['party'] = 0

    if (session.get('party', 0) == 0):
        message = message.strip().lower()
        p = Party.query.filter(Party.code == message).first()
        if p is None:
        	returnmessage = "".join(["We're sorry, we couldn't find the party \"", message, "\" that you were looking for. Respond to try again."])
        else:
	        session['party'] = message
	        returnmessage = "".join(["You are now part of the party \"", message, ".\" Reply with a song title and/or artist to queue a song, or reply with the word 'setparty' and a new party code to switch rooms!"])
    else:
        songinfo = gettrackinfo(message)
        if songinfo == None:
            returnmessage = "".join(["We're sorry, we couldn't find the song \"", messages[0].body, "\" that you were looking for. Respond to try again."])
        else:
            returnmessage = "".join(["Thank you for adding ", songinfo[1], ", by ", songinfo[2], " to the party playlist. Reply to add another song."])
            sl = Party.query.filter(Party.code == session['party']).first().song_lists[0]
            s = Song(uid=songinfo[0], title=songinfo[1], artist=songinfo[2], votes=1, approved=1, album=songinfo[3], coverpic=songinfo[4], songlist = sl)
            db.session.add(s)
            db.session.commit()

    resp = twilio.twiml.Response()
    resp.sms(returnmessage)
 
    return str(resp)

@party.route("/callrequest", methods=['GET', 'POST'])
def call_request():
    resp = twilio.twiml.Response()
    resp.say("Hello. Our calling service has not been set up yet. Please call again later")
    return str(resp)

@party.route("/get_pending", methods=['POST'])
def get_pending():
    #get the party key
    jsonResp = json.loads(request.data)
    partykey = jsonResp['partykey']
    # pdb.set_trace()
    res = Party.query.filter(Party.code == partykey).first()
    if res is None:
        return "{'success': 'false'}"
    else:
        sl = res.song_lists[0]
    goodSongs = []
    for song in sl.songs:
        if song.approved == 1:
            goodSongs.append({'title': song.title, 'artist': song.artist, 'coverpic': song.coverpic, 'id': song.id})
    return json.dumps(goodSongs)

@party.route("/approval", methods=['POST'])
def approval():
    j = json.loads(request.data)
    # pdb.set_trace()
    sID = j['id']
    action = j['action']
    s = Song.query.filter(Song.id == sID).first()
    if s is None:
        return "{'success': 'true'}"
    if action == 'denied':
        db.session.delete(s)
        db.session.commit()
        return "{'success': 'true'}"
    else:
        s.approved = 0
        db.session.commit()
        return "{'success': 'true'}"




