""" SQLAlchemy models """

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """ User in the system """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    advise = db.relationship('Advise')

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    likes = db.relationship('Advise', secondary="likes")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    def is_followed_by(self, other_user):
        """ Other users following user """

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """ User following other users """

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, password):
        """
        Sign up user.
        Hashes password and adds user to database.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
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

class Advise(db.Model):
    """ An individual advise """

    __tablename__ = "advise"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(users.id, ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')


class Likes(db.Model):
    """ Mapping users likes to advise """

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.id, ondelete='CASCADE'), nullable=False)
    advise_id = db.Column(db.Integer, db.ForeignKey(advise.id, ondelete='CASCADE'), nullable=True)
    

class Follows(db.Model):
    """ Connection of a followers and following """

    __tablename__ = "follows"

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )


class connect_db(app):
    """ Connects database to Flask app """

    db.app = app
    db.init_app(app)