from main import db
from sqlalchemy import func
from sqlalchemy.orm import validates
from flaskext.auth import AuthUser, get_current_user_data
import datetime
# import sqlalchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fbid = db.Column(db.String(1000), unique = True)
    token = db.Column(db.String(1000))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

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
    title = db.Column(db.String(80))
    artist = db.Column(db.String(80))    
    approved = db.Column(db.Integer)
    album = db.Column(db.String(80))
    coverpic = db.Column(db.String(80))
    votes = db.Column(db.Integer(20))
    song_list_id = db.Column(db.Integer, db.ForeignKey('song_lists.id'))
    songlist = db.relationship('Song_List', backref="songs")

    def __repr__(self):
        return '#%d: Song Title: %s, Song Artist: %s' % (self.id, self.title, self.artist)

class Song_List(db.Model):
    __tablename__='song_lists'
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    party = db.relationship('Party', backref="song_lists")

    def __repr__(self):
        return '#%d: Party ID: %d' % (self.id, self.party_id)
