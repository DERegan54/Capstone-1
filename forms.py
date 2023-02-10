from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, IntegerField, SelectField
from wtforms.validators import Email, Length, Optional, InputRequired, URL



#############################################################

class Add_user_form(FlaskForm):
    """Form for adding a user."""

    username = StringField('Username:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired(), Email()])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6)])
    # profile_photo = StringField('Profile photo URL:', validators=[URL(), Optional()])   

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


class Breed_review_form(FlaskForm):
    """Form for submitting a breed review."""
    breed_name = StringField('Breed name:', validators=[InputRequired()])
    maintenance_rating = SelectField('Maintenance Rating:', choices=[(1), (2),(3), (4), (5)], validators=[InputRequired()])
    behavior_rating = SelectField('Obedience Rating:', choices=[(1), (2), (3), (4), (5)], validators=[InputRequired()])
    trainability_rating = SelectField('Trainability Rating:', choices=[(1), (2), (3), (4), (5)], validators=[InputRequired()])
    comments = StringField('Comments:', validators=[Optional()], render_kw={"placeholder": "Please enter your comments here"})


class Delete_form(FlaskForm):
    """Delete form -- this form is intentionally blank."""

