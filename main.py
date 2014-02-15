"""
app setup thinkful.com.
"""


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

# from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
# app.debug = os.getenv["DEBUG"] in ('True', 'true')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# class User(db.Model):
#     # __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.String(32), index=True)
#     firstname = db.Column(db.String(80))
#     lastname = db.Column(db.String(80))

#     def hash_password(self, password):
#     	self.password_hash = pwd_context.encrypt(password)

#     def verify_password(self, password):
#     	return pwd_context.verify(password, self.password_hash)

#     def __repr__(self):
#         return '#%d: Email: %s, First Name: %s, Last Name: %s' % (self.id, self.email, self.firstname, self.lastname)


# for flaskext.auth -- secret key needed to use sessions
app.secret_key = os.environ['USER_AUTH_SECRET_KEY']
