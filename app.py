from crypt import methods
import os
from distutils.log import debug
from urllib import response
from flask import Flask, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Advice, Likes
from api import Requests
from forms import UserAddForm, LoginForm, EditProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("unknown_secret", "shh") 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///advice-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)


connect_db(app)

# db.drop_all()
# db.create_all()

CURR_USER_KEY = "curr_user"
##########################################################################################
# Global




##########################################################################################
# User signup/login/logout 

@app.before_request
def add_user_to_g():
    """If user logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def verify_user():
    """ Verify user id logged in """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")


@app.route('/signup', methods=["GET", "POST"])
def new_user():
    """
    Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if "username" in session:
        return redirect(f"/users/{session['username']}")


    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        flash(f"Welcome {user.username}!", 'success')

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form) 


@app.route('/login', methods=["GET", "POST"])
def login():
    """ Handle user login """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", 'success')
            return redirect('/')

        flash("Invalid credentials.", 'danger')

    return render_template('/users/login.html', form=form)


@app.route('/logout')
def logout():
    """ Handle logout of user """

    do_logout()
    flash("Successfully logged out", "success")
    return redirect('/login')



##########################################################################################
# General user routes:

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Show user profile """

    user = User.query.get_or_404(user_id)

    advice = (Advice
                .query
                .filter(Advice.user_id == user_id)
                .order_by(Advice.timestamp.desc())
                .limit(100)
                .all())


    return render_template('/users/show.html', user=user, advice=advice, likes=user.likes)


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    
    verify_user()

    user = g.user
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            
            user.username = form.username.data
            user.password = User.hash_pwd(form.new_password.data)

            db.session.commit()
            return redirect(f'/users/{user.id}')

        flash("Incorrect password, please try again.", 'danger') 

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    verify_user()

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


@app.route('/users/like/<int:advice_id>', methods=['POST'])
def add_like(advice_id):
    """Toggle a liked advice for the logged-in user."""

    verify_user()

    liked_advice = Advice.query.get_or_404(advice_id)

    # if liked_advice.user_id == g.user.id:
    #     return abort(403)

    user_likes = g.user.likes

    if liked_advice in user_likes:
        g.user.likes = [like for like in user_likes if like != liked_advice]
    else:
        g.user.likes.append(liked_advice)

    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/likes', methods=["GET"])
def show_likes(user_id):
    """Shows liked messages by the logged-in user """

    verify_user()

    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html', user=user, likes=user.likes)

##########################################################################################
# Advice routes

@app.route('/api/advice', methods=["POST"]) 
def create_advice():
    """ Request advice from API and adds to database """

    response = Requests.random_advice()

    verify_user()

    new_advice = Advice(text=response['advice'])
    g.user.advice.append(new_advice)
    db.session.commit()

    return redirect(f'/users/{g.user.id}')


@app.route('/api/advice/<int:advice_id>', methods=["GET"]) 
def get_advice(advice_id):
    """ Show specific advice """

    advice = Advice.query.get_or_404(advice_id)
    return render_template('advice/advice.html', advice=advice)


@app.route('/api/advice/<int:advice_id>/delete', methods=["POST"])
def delete_advice(advice_id):
    """ Delete advice """

    verify_user()

    advice = Advice.query.get_or_404(advice_id)
    db.session.delete(advice)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


##########################################################################################
# Home and 404

@app.route('/')
def homepage():
    """"
    Show homepage:

    - anon users: redirect to Sign up
    - logged in: recent advice all users
    """

    if g.user:
        user = User.query.get_or_404(g.user.id)
        advice = (Advice
                    .query
                    .order_by(Advice.timestamp.desc())
                    .limit(100)
                    .all())
        return render_template('home.html', advice=advice, likes=user.likes)
    else:
        return render_template('/home-anon.html')

@app.errorhandler(404)
def not_found(error):
    return render_template("/404.html"), 404