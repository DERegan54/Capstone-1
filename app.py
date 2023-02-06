from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from secrets import API_KEY
from sqlalchemy.exc import IntegrityError
from forms import Add_user_form, Login_Form, Edit_profile_form, Breed_review_form, Delete_form
from models import db, connect_db, User, Breed, Review, Favorite 
from user import login_user, logout_user
from api_requests import add_breed_to_db, search_breeds
import requests



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
# ROOT ROUTE
###################################################################################

@app.route('/', methods=["GET"])
def homepage():
    """Display search page."""

    url = f'{API_BASE_URL}name=labrador'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    data = response.json()
       
    return render_template('home.html', data=data)


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
        return redirect('/user')

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
    
    favorites = Favorite.query.all()   

    return render_template('user/my_profile.html', user=user, favorites=favorites)
   

@app.route('/user/edit_form', methods=["GET"])
def show_edit_profile_form():
    """Show edit profile form."""
    
    user = g.user
    form = Edit_profile_form(obj=user)
    
    return render_template('/user/edit_profile.html', user=user, form=form)


@app.route('/user/edit', methods=["POST"])
def edit_profile():
    """Update profile details for current user."""

    if not g.user:
        flash("Access unauthorized.  Please log in or sign up for an account.", "danger")
        return redirect('/signup')

    user = g.user
    form = Edit_profile_form(obj=user)

    
    user = User.authenticate(user.username, form.password.data)
    
    if form.validate_on_submit():
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
    
    return render_template('user/edit_profile.html', form=form, user=user)   
     

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

@app.route("/search", methods=["GET"])
def show_search_page():
    """Displays search page"""

    return render_template('breeds/search.html')


@app.route('/search_results', methods=["GET"])
def show_breed_search_results():
    """Display breed info retrieved from breed search and add to breed_picker database."""
    # Issues:
    # - How do I query my database so that I can render the template with the data from 
    # from my database instead of the data returned from the dogs API?
    

    query = request.args.get('breed_search')  # Grabs input from search form

    data = search_breeds(query) # Queries dogs API
    
    add_breed_to_db(query) # Adds response data from dogs API to database 
    
    breeds = Breed.query.all()
    
    return render_template('/breeds/search_results.html', query=query, data=data, breeds=breeds)  # Shows search results on search_results page
    

    # Can I somehow retrieve the item from breeds that matches the query and then access the breed_id from there?
    # breeds = Breed.query.all()
    # for breed in breeds:
    #     ids = []
    #     id = breed.id
    #     ids.append(id)
    # print('#################', ids)
    # for breed in breeds:
    #     names = []
    #     name = breed.name
    #     names.append(name)
    #     return names
    # print('########################', names)
    # breeds_data = dict(zip(ids, names))


    # for breed in breeds:
    #     ids = []
    #     ids.append(breed[0])
    #     names = []
    #     names.append(breed[1])
    # print('$$$$$$$$$$$$$$$$$$$$$', breeds_data)    
   
    


###################################################################################
# FAVORITE ROUTES
###################################################################################

@app.route('/user/my_favorites', methods=["GET"])
def show_user_favorites():
    """Displays users list of favorite breeds."""

    if not g.user:
        flash("Please login or sign up for an account.", "danger")
        return redirect('/')

    user = g.user
    favorites = Favorite.query.all()
    user_favorites = user.favorites
    
    return render_template('/user/my_favorites.html', user=user, user_favorites=user_favorites)


@app.route('/user/<name>/favorite', methods=["GET", "POST"])
def favorite_a_breed(name):
    """Adds/removes breeds from favorites list."""

    if not g.user:
        flash('Please login to favorite a breed.', 'danger')
        return redirect('/')
    
    favorited_breed = db.session.query(Breed).filter_by(name=name).first()
    
    # query the breed to see if it is in the 'favorites' table (meaning it has been favorited)
    user_favorites = g.user.favorites #get the user's favorites

    if favorited_breed in user_favorites:  # if the breed is in the user_favorites list
        g.user.favorites = [favorite for favorite in user_favorites if favorited_breed != user_favorites]  #if the breed is user_favorites, unfavorite it
    else:      # else append favorited_breed to g.user.favorites 
        g.user.favorites.append(favorited_breed)
       
    db.session.commit()

    return redirect('/user/my_favorites')

###################################################################################
# BREED REVIEW ROUTES
###################################################################################

@app.route('/reviews/list_reviews', methods=["GET"])
def show_all_reviews():
    """Shows all breed reviews."""

    reviews = Review.query.all()
    user = g.user

    return render_template('/reviews/list_reviews.html', user=user, reviews=reviews)


@app.route('/user/my_reviews', methods=["GET"])
def show_user_reviews():
    """Show user's breed reviews."""

    user = g.user

    if not g.user:
        flash("Please login or sign up for an account.", "danger")
        return redirect('/')
    
    return render_template('user/my_reviews.html', user=user,)  


@app.route('/reviews/review_form', methods=["GET"])
def show_review_form():
    """Display review form."""

    breed = request.args.get('breed_search')
  
    user = g.user
    form = Breed_review_form()
   
    return render_template('/reviews/add_review.html', user=user, form=form, breed=breed)

@app.route('/reviews/add_review', methods=["POST"])
def add_breed_review():
    """ Add breed review to database.  Redirect to user page. """

    form = Breed_review_form()

    if form.validate_on_submit():
        review = Review(
            breed_name = form.breed_name.data,
            maintenance_rating = form.maintenance_rating.data,
            behavior_rating = form.behavior_rating.data,
            trainability_rating = form.trainability_rating.data,
            comments = form.comments.data,
            user_id = g.user.id
        )
        db.session.add(review)
        db.session.commit()
        return redirect("/user/my_reviews") 
    else:
        return render_template('/reviews/add_review.html', form=form)
    

@app.route('/reviews/<int:review_id>/edit_review_form', methods={"GET"})
def show_edit_review_form(review_id):
    """Show edit breed review form."""

    user = g.user
    review = Review.query.get(review_id)
    form = Breed_review_form(obj=review)
    
    return render_template('/reviews/edit_review.html', user=user, form=form, review=review)


@app.route('/reviews/<int:review_id>/edit_review', methods=["POST"])
def edit_breed_review(review_id):
    """Update breed reveiw and add to database."""
    
    user = g.user
    form = Breed_review_form()
    review = Review.query.get(review_id)
    if form.validate_on_submit():
        review.breed = form.breed_name.data
        review.maintenance_rating = form.maintenance_rating.data
        review.behavior_rating = form.behavior_rating.data
        review.trainability_rating = form.trainability_rating.data
        review.comments = form.comments.data
        
        db.session.commit()
        flash("Review successfully updated.", "info")
        return redirect(f'/reviews/list_reviews')

    return render_template('/reviews/edit_review.html', user=user, form=form, review=review)


@app.route('/reviews/<int:review_id>/delete', methods=["POST"])
def delete_breed_review(review_id):
    """Delete breed review from database."""
    
    review = Review.query.get(review_id)

    form = Delete_form(obj=review)
    
    if not g.user:
        flash("Please login or sign up for an account.", "danger")
        return redirect('/')

    if form.validate_on_submit:
        db.session.delete(review)
        db.session.commit()

    flash("User's review has been deleted.", "info")
    return redirect(f'/reviews/list_reviews')
   


###################################################################################
# ADOPTION RESOURCES ROUTE
###################################################################################

@app.route('/adopt', methods=["GET"])
def show_adopt_page():
    """Shows Adopt Page."""

    return render_template('adopt.html')    



