from flask import Blueprint, send_from_directory, request, render_template, redirect, flash, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from user.models import User
from user import *
from main import app
import json
import pdb
from flask_oauth import OAuth
import os
from main import lm

FACEBOOK_APP_ID = os.environ['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = os.environ['FACEBOOK_APP_SECRET']

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


# auth = Auth(app, login_url_name='user_page')
# auth.user_timeout = 0


user = Blueprint('user', __name__, template_folder="")

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@user.route('/show_users/')
def show_users():
    users = User.query.all()
    return render_template('templates/show_users.html', users=users)

@user.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        print "already authed"
        return redirect(url_for('party.index'))
    print "not authed"
    return facebook.authorize(callback=url_for('user.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('splash.home'))

@user.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = getUser(me.data['id'])
    if user is None:
        user = User(fbid=me.data['id'], firstname=me.data['first_name'], lastname=me.data['last_name'])
        db.session.add(user)
        # pdb.set_trace()
        db.session.commit()
    login_user(user, remember = True)
    return redirect(url_for('party.index'))
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

def getUser(fbid):
    return User.query.filter(User.fbid == fbid).first()


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

# @user.route('/register')
# def register():
#     return render_template('templates/register.html')


# @user.route('/login')
# def login():
#     return render_template('templates/login.html')
