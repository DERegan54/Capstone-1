from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from secrets import API_KEY
from sqlalchemy.exc import IntegrityError
from forms import Add_user_form, Login_Form, Edit_profile_form, Initial_search_form, Breed_search_form, Characteristic_search_form, Breed_review_form
from models import db, User, connect_db, Breed, Characteristic, Review, Favorite_breed, Breed_characteristic
from user import login_user, logout_user
from api import get_breeds
import requests
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///breed_picker'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SHHHHHHH....SECRET!!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'

###################################################################################
# HOMEPAGE ROUTE
###################################################################################

@app.route('/')
def homepage():
    """Show homepage.
     - Not logged in?  Show sign-up page.
     - Logged in?  Show search page.
    """
    
    url = f'{API_BASE_URL}barking=4'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    data = response.json()
    # data = get_breeds()

    return render_template('homepage.html', data=data)


####################################################################################
# LOGIN/LOGOUT/SIGNUP ROUTES
####################################################################################

CURR_USER_KEY = 'current_user'

@app.before_request
def add_user_to_g():
    """If the user is logged in , add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
        Create new user and add to database.  Redirect to homepage.
        If the form is not valid, re-present form.
        If the username is already taken, flash message and re-present form.
    """

    form = Add_user_form()

    if form.validate_on_submit():
        try: 
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
        
        except IntegrityError:
            db.session.rollback()
            flash("That username is taken.  Please enter a different username.", 'danger')
            return render_template('user/signup.html', form=form)

        login_user(user)
        flash(f"Welcome, {user.username}! Profile successfully created.", 'info')
        return redirect('/')

    else:
        return render_template('user/signup.html', form=form)
    

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    if g.user:
        flash("You are currently logged in." "danger")
        return redirect("/")

    form = Login_Form()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                  form.password.data)

        if user:
            login_user(user)
            flash(f"Welcome back, {user.username}!", "info")
            return redirect("/user")
        else: 
            flash("Invalid credentials.", "danger")
    
    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle user logout."""

    if not g.user:
        flash("Please log in or sign up.", "danger")
        return redirect('/')

    logout_user()

    flash(f"You have successfully logged out.  Goodbye!", "info")
    return redirect("/login")



###################################################################################
# USER PROFILE ROUTES
###################################################################################

@app.route('/user', methods=["GET"])
def show_user_profile():
    """Show user profile page."""

    if not g.user:
        flash("Please login or sign up for an account.", "danger")
        return redirect('/')

    user = g.user
    

    # favorite_breeds = 

    # reviews = 

    return render_template('user/profile.html', user=user)
    #  favorite_breeds=favorite_breeds, reviews=reviews)


@app.route('/user/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile details for current user."""

    user = g.user

    if not g.user:
        flash("Access unauthorize.  Please log in or sign up for an account.", "danger")
        return redirect('/signup')
    
    form = Edit_profile_form(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):

            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data
            user.family_members_adults = form.family_members_adults.data
            user.family_members_children = form.family_members_children.data
            user.other_pets = form.other_pets.data
            user.profile_photo = form.profile_photo.data
            user.environment = form.environment.data
            user.experience_level = form.experience_level.data

            db.session.commit()
        
            flash("Profile successfully updated.", "info")

            return redirect('/user')
        
        flash("Wrong credentials.  Please try again.", "danger")

    return render_template('/user/edit.html', form=form, user=user.id)
        

@app.route('/user/delete', methods=["POST"])
def delete_user():
    """Delete user from database."""

    if not g.user:
        flash("Access unauthorized.  Please log in or create an account.", "danger")
        return redirect("/login")

    logout_user()

    db.session.delete(g.user)
    db.session.commit()

    flash("User profile has been deleted.", "info")
    return redirect('/signup')


###################################################################################
# SEARCH ROUTES
###################################################################################

# @app.route('/search', methods=["GET"])
# def search_breeds:
#     """Handle form submission; return form; show breeds related to search query"""

#     try search_by = request.args.get()

###################################################################################
# ADOPT ROUTE
###################################################################################

@app.route('/adopt', methods=["GET"])
def show_adopt_page():
    """Shows Adopt Page."""

    return render_template('adopt.html')