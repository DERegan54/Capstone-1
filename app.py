from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from secrets import API_KEY
from sqlalchemy.exc import IntegrityError
from forms import Add_user_form, Login_Form, Edit_profile_form, Breed_review_form
from models import db, connect_db, User, Breed, Review 
from user import login_user, logout_user
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

@app.route('/', methods=["GET"])
def homepage():
    """Display search page."""

    return render_template('home.html')


###################################################################################
# SEARCH ROUTE
###################################################################################

@app.route('/search', methods=["GET"])
def search_breeds():
    """Querys dogs API to get dog breed info."""

    query = request.args.get('breed_search')

    try:
        url = f'{API_BASE_URL}name={query}'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        data = response.json()

        return render_template("breed.html", data=data)
    except:
        flash("Invalid search. Please enter a breed.", "danger") 
        return redirect("/")


###################################################################################
# ADD BREED TO BREED_PICKER DATABASE ROUTE
###################################################################################

@app.route('/breed', methods=["GET", "POST"])
def add_breed_to_database():
    """Gets breed from dogs API and adds breed to breed_picker database."""

    url = f'{API_BASE_URL}barking=1'     # Get first 20 records of dogs that bark the least (barking=1 endpoint)
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    data = response.json()

    data_breed = data[0]

    breed = Breed(**data_breed)
    db.session.add(breed)
    db.session.commit()

    return render_template('breed.html', data=data)


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
            flash("Wrong credentials. Please try again.", "danger")
    
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

    return render_template('user/user_profile.html', user=user)
    #  favorite_breeds=favorite_breeds, reviews=reviews)


@app.route('/user/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile details for current user."""

    if not g.user:
        flash("Access unauthorized.  Please log in or sign up for an account.", "danger")
        return redirect('/signup')

    user = g.user
    form = Edit_profile_form(obj=user)

    if form.validate_on_submit():
        user = User.authenticate(user.username, form.password.data)

        user.username = form.username.data
        user.email = form.email.data
        user.profile_photo = form.profile_photo.data
        user.family_members_adults = form.family_members_adults.data
        user.family_members_children = form.family_members_children.data
        user.other_pets = form.other_pets.data
        user.environment = form.environment.data
        user.experience_level = form.experience_level.data

        db.session.commit()
        flash("Profile successfully updated.", "info")
        return redirect('/user')
    return render_template('user/edit_profile.html', form=form)   
     

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
# BREED ROUTES
###################################################################################

@app.route('/all_p1', methods=["GET"])
def all_dogs_p1():
    """Display all dogs that bark at level 1."""
    url = f'{API_BASE_URL}barking=1'                                # Get first 20 records of dogs that bark the least (barking=1 endpoint)
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    response_data = response.json()
    response1 = response_data

    if len(response1) == 20:                                           # If there are more than 20 records, get next 20 records of dogs that bark the least 
        url = f'{API_BASE_URL}barking=1;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        response2 = response_data
        return render_template('/breeds/p1.html', response1=response1, response2=response2)

@app.route('/all_p2', methods=["GET"])
def all_dogs_p2():
    """Display all dogs who bark at level 2."""    
    url = f'{API_BASE_URL}barking=2;offset=0'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    response_data = response.json()
    response3 = response_data

    if len(response3) == 20:
        url = f'{API_BASE_URL}barking=2;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        response4 = response_data
        return render_template('/breeds/p2.html', response3=response3, response4=response4)

@app.route('/all_p3', methods=["GET"])
def all_dogs_p3():
    """Display all dogs who bark at level 3."""        
    url = f'{API_BASE_URL}barking=3;offset=0'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    response_data = response.json()
    response5 = response_data
            
    if len(response5) == 20:
        url = f'{API_BASE_URL}barking=3;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        response6 = response_data

        if len(response6) == 20:
            url = f'{API_BASE_URL}barking=3;offset=40'
            response = requests.get(url, headers={'X-Api-Key': API_KEY})
            response_data = response.json()
            response7 = response_data

            if len(response5) == 20:
                url = f'{API_BASE_URL}barking=3;offset=60'
                response = requests.get(url, headers={'X-Api-Key': API_KEY})
                response_data = response.json()
                response8 = response_data

                if len(response5) == 20:
                    url = f'{API_BASE_URL}barking=3;offset=80'
                    response = requests.get(url, headers={'X-Api-Key': API_KEY})
                    response_data = response.json()
                    response9 = response_data

                    if len(response5) == 20:
                        url = f'{API_BASE_URL}barking=3;offset=100'
                        response = requests.get(url, headers={'X-Api-Key': API_KEY})
                        response_data = response.json()
                        response10 = response_data

                        if len(response5) == 20:
                            url = f'{API_BASE_URL}barking=3;offset=120'
                            response = requests.get(url, headers={'X-Api-Key': API_KEY})
                            response_data = response.json()
                            response11 = response_data

                            if len(response5) == 20:
                                url = f'{API_BASE_URL}barking=3;offset=140'
                                response = requests.get(url, headers={'X-Api-Key': API_KEY})
                                response_data = response.json()
                                response12 = response_data
                                return render_template('/breeds/p3.html', response5=response5, response6=response6, response7=response7,
                                       response8=response8, response9=response9, response10=response10, response11=response11, 
                                       response12=response12)

@app.route('/all_p4', methods=["GET"])
def all_dogs_p4():
    """Display all dogs that bark at level 4."""             
    url = f'{API_BASE_URL}barking=4;offset=0'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    response_data = response.json()
    response13 = response_data

    if len(response13) == 20:
        url = f'{API_BASE_URL}barking=4;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        response14= response_data

        if len(response14) == 20:
            url = f'{API_BASE_URL}barking=4;offset=40'
            response = requests.get(url, headers={'X-Api-Key': API_KEY})
            response_data = response.json()
            response15 = response_data
            return render_template('/breeds/p4.html', response13=response13, response14=response14, response15=response15)

@app.route('/all_p5', methods=["GET"])
def all_dogs_p5():
    """Display all dogs that bark at level 5."""
    url = f'{API_BASE_URL}barking=5;offset=0'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    response_data = response.json()
    response16 = response_data        

    if len(response16) == 20:
        url = f'{API_BASE_URL}barking=5;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response_data = response.json()
        response17= response_data
        return render_template('/breeds/p5.html', response16=response16, response17=response17)


###################################################################################
# FAVORITE ROUTES
###################################################################################

# @app.route('/user/favorites', methods=["POST"])
# def favorite_breed(breed_id):
#     """Adds/removes likes from breeds."""

#     if not g.user:
#         flash('Please login to favorite a breed.', 'danger')
#         return redirect('/')

#     # query the breed to see if it is in the 'favorites' table (meaning it has been favorited)
#     favorited_breed = Breed.query.get_or_404(breed_id)
#     # get the user's favorites
#     user_favorites = g.user.favorites

#     if favorited_breed in user_favorites:
#         g.user.favorites = [favorite for favorite in user_favorites if favorite != favorited_breed]
#     else: 
#         g.user.favorites.append(favorited_breed)
    
#     db.session.commit()

#     return redirect('/user')


###################################################################################
# BREED REVIEW ROUTES
###################################################################################

@app.route('/reviews_list', methods=["GET"])
def show_all_reviews():
    """Shows all breed reviews."""

    if not g.user:
        flash("Please login or sign up for an account.", "danger")
        return redirect('/')

    user = g.user
    reviews = Review.query.all()

    return render_template('reviews/list_reviews.html', user=user, reviews=reviews)


@app.route('/reviews/add_review', methods=["GET", "POST"])
def add_breed_review():
    """ Add breed review to database.  Redirect to user page.
        If the form is not valid, flash message and re-present form.
    """

    if not g.user:
        flash("Access unauthorized.  Please log in or sign up for an account.", "danger")
        return redirect('/login')

    form = Breed_review_form()

    if  form.validate_on_submit():
        breed_name = form.breed_name.data
        maintenance_rating = form.maintenance_rating.data
        behavior_rating = form.behavior_rating.data
        trainability_rating = form.trainability_rating.data
        comments = form.comments.data

        review = Review(breed_name=breed_name, maintenance_rating=maintenance_rating, 
                 behavior_rating=behavior_rating, trainability_rating=trainability_rating, comments=comments)     

        db.session.add(review)
        db.session.commit()
        return redirect(f"/reviews")   
    
    else:
        return render_template("/reviews/add_review.html", form=form)
    

@app.route('/review/edit_review', methods=["GET", "POST"])
def edit_breed_review():
    """Update breed reveiw and add to database.  Redirect to user page.
       If the form is not valid flash message and re-present form.
    """



@app.route('/review/delete', methods=["POST"])
def delete_breed_review():
    """Delete breed review from database."""

    if not g.user:
        flash("Access unauthorized.  Please log in or create an account.", "danger")
        return redirect("/login")
    
    logout_user()

    db.session.delete()
    db.session.commit()

    flash("User profile has been deleted.", "info")
    return redirect('/signup')


###################################################################################
# ADOPTION RESOURCES ROUTE
###################################################################################

@app.route('/adopt', methods=["GET"])
def show_adopt_page():
    """Shows Adopt Page."""

    return render_template('adopt.html')    

