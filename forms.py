from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, IntegerField, SelectField
from wtforms.validators import Email, Length, Optional, InputRequired, URL



#############################################################

class Add_user_form(FlaskForm):
    """Form for adding a user."""

    username = StringField('Username:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6)])
    profile_photo = StringField('Profile photo URL:', validators=[URL(), Optional()])   

class Login_Form(FlaskForm):
    """User login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
   

class Edit_profile_form(FlaskForm):
    """Form for editing a user's profile."""

    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    family_members_adults = IntegerField('Adults in your home:', validators=[Optional()])
    family_members_children = IntegerField('Children in your home:', validators=[Optional()])
    other_pets = StringField('Other pets in your home:', validators=[Optional()])
    profile_photo = URLField('Profile photo URL:', validators=[Optional()])
    environment = SelectField('Home Environment:', choices=[('Urban - no yard'), ('Suburban - have a back yard'), ('Rural - live on multiple acres')])
    experience_level = SelectField('Experience Level:', choices=[('This will be our first dog'), ('We have had a dog in the past.'), ('We have had more than one dog in the past.')])


class Initial_search_form(FlaskForm):
    """Initial form to specify type of search (by breed or characteristic)."""

    search_by = SelectField('Search by:', choices=[('Breed Name'),('Breed Characteristic')], validators=[InputRequired()])
    

class Breed_search_form(FlaskForm):
    """Form for searching by breed."""

    breed_name = StringField('Breed name:', validators=[InputRequired()])


class Characteristic_search_form(FlaskForm):
    """Form for searching by breed characteristic."""

    barking = SelectField("Barking frequency:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    shedding = SelectField("Shedding frequency:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    grooming = SelectField("Grooming needs:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    drooling = SelectField("Drooling frequency:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    energy = SelectField("Movement needs:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    trainability = SelectField("Ease of training:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    Protectiveness = SelectField("Protectiveness:", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    # good_with_Children = SelectMultipleField("Good with children?", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])
    # good_with_other_dogs = SelectMultipleField("Good with other dogs?", choices=[('0 = Never'),('1 = Once in a while'), ('2 = Occasionally'), ('3 = Sometimes'), ('4 = Usually'), ('5 = Always')])


class Breed_review_form(FlaskForm):
    """Form for submitting a breed review."""

    breed_name = StringField('Breed name:', validators=[InputRequired()])
    maintenance_rating = SelectField('Maintenance Required:', choices=[('Low maintenance'), ('Below average maintenance'),('Average maintenance'), ('Above average maintenance'), ('High maintenance')], validators=[InputRequired()])
    behavior_rating = SelectField('Obedience:', choices=[('Never obeys'), ('Obeys once in a while'), ('Sometimes obeys'), ('Usually obeys'), ('Always obeys')], validators=[InputRequired()])
    trainiability_rating = SelectField('Trainability:', choices=[('Very difficult to train'), ('Difficult to train'), ('Average trainability'), ('Easy to train'), ('Very easy to train')], validators=[InputRequired()])
    comments = StringField('Comments:', validators=[Optional()])






