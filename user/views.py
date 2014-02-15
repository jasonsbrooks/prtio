from flask import Blueprint, send_from_directory, request, render_template, redirect, flash
from flaskext.auth import Auth, logout, get_current_user_data
from user.models import User
from user import *
from main import app
import json
import pdb

auth = Auth(app, login_url_name='user_page')
auth.user_timeout = 0


user = Blueprint('user', __name__, template_folder="")

@user.route('/show_users/')
def show_users():
    users = User.query.all()
    return render_template('templates/show_users.html', users=users)

# @user.route('/do/login', methods=['POST'])
# def do_login_user_HTTP():
#     requestDict = request.values
#     requestDict = dict(zip(requestDict, map(lambda x: requestDict.get(x), requestDict)))
#     # pdb.set_trace()
#     user = userByLogin(requestDict['username'])
#     if user is not None:
#         # Authenticate and log in!
#         if user.authenticate(requestDict['password']):
#             responseDict['successfulRedirect'] = '/'
#     return json.dumps(responseDict)

@user.route('/register')
def register():
    return render_template('templates/register.html')


@user.route('/login')
def login():
    return render_template('templates/login.html')

@user.route('/do/register', methods = ['POST'])
def new_user():
    requestDict = request.values
    requestDict = dict(zip(requestDict, map(lambda x: requestDict.get(x), requestDict)))
    username = requestDict['email']
    firstname = requestDict['firstname']
    lastname = requestDict['lastname']
    password = requestDict['password']
    # pdb.set_trace()
    if len(username) is 0 or len(password) is 0:
        flash("Missing information")
        return render_template("templates/register.html")
    if User.query.filter_by(email = username).first() is not None:
        return render_template("templates/register.html")
    user = User(email=username, firstname=firstname, lastname=lastname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return "Hello"
