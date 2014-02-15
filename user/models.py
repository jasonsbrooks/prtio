from main import db
from sqlalchemy import func
from sqlalchemy.orm import validates
from flaskext.auth import AuthUser, get_current_user_data
import datetime
# import sqlalchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __repr__(self):
        return '#%d: First Name: %s   Last Name: %s' % (self.id, self.firstname, self.lastname)

class Party(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    code = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='parties')

    def __repr__(self):
        return '#%d: Party Name: %s  Party Owner: %d  Code: %s' % (self.id, self.name, self.user_id, self.code)

class Song(db.Model):
    __tablename__='songs'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80))
    votes = db.Column(db.Integer(20))
    song_list_id = db.Column(db.Integer, db.ForeignKey('song_lists.id'))
    songlist = db.relationship('Song_List', backref="songs")

    def __repr__(self):
        return '#%d: Song ID: %s' % (self.id, self.uid)

class Song_List(db.Model):
    __tablename__='song_lists'
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    party = db.relationship('Party', backref="song_lists")
