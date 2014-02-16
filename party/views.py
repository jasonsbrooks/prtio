from flask import (Flask, render_template, Response, request, 
    Blueprint, redirect, send_from_directory, send_file, jsonify, g)
from flask import session
import twilio.twiml
from twilio.rest import TwilioRestClient
import os
import pdb
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
    return render_template('templates/party.html', parties = u.parties)

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
    return render_template('templates/party.html')

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
        # query the party to make sure it exists, for now just set the party
        session['party'] = message
        returnmessage = "".join(["You are now part of the party \"", message, ".\" Reply with a song title and/or artist to queue a song!"])
    else:
        songinfo = gettrackinfo(message)
        if songinfo == None:
            returnmessage = "".join(["We're sorry, we couldn't find the song \"", messages[0].body, "\" that you were looking for. Respond to try again."])
        else:
            returnmessage = "".join(["Thank you for adding ", songinfo[1], ", by ", songinfo[2], " to the party playlist. Reply to add another song."])
            # songid.add(songinfo[0])
    
    # if request.method == "GET":
    #     return songid
    # code here to add songinfo[0] to the queue

    resp = twilio.twiml.Response()
    resp.sms(returnmessage)
 
    return str(resp)