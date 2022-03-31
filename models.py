""" SQLAlchemy models """

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class Advice(db.Model):
    """ An individual advice """

    __tablename__ = "advice"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True
    )
    user = db.relationship('User')


class User(db.Model):
    """ User in the system """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    advice = db.relationship('Advice', backref='users')

    likes = db.relationship('Advice', secondary="likes")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def hash_pwd(cls, password):
        """ Hashes password """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8') 
        return hashed_pwd

    @classmethod
    def signup(cls, username, password):
        """
        Sign up user.
        Hashes password and adds user to database.
        """

        hashed_pwd = User.hash_pwd(password)

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        print(hashed_pwd)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """
        Find user with `username` and `password`.
        Searches for user whose password hash matches this password
        , if user matches, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Likes(db.Model):
    """ Mapping users likes to advice """

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    advice_id = db.Column(db.Integer, db.ForeignKey('advice.id', ondelete='CASCADE'), nullable=True)
    

def connect_db(app):
    """ Connects database to Flask app """

    db.app = app
    db.init_app(app)