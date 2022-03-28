from distutils.log import debug
from flask import Flask, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Advise, Follows, Likes
# from forms 

app = Flask(__name__)
app.config['SECRET_KEY'] = "unknown_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()


##########################################################################################
# Global Variables




##########################################################################################
# Home 
