from flask import Flask, render_template, request, flash, redirect, session, g
from secrets import API_KEY
from forms import Add_user_form, Login_Form, Edit_profile_form, Breed_review_form
from models import db, connect_db, User, Breed, Review 
from user import login_user, logout_user
import requests
import json
import requests

API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'
LOCAL_BASE_URL = 'http://127.0.0.1:5000/'


############################################################################
# HELPER FUNCTIONS
############################################################################


def get_breeds_from_db():
    """Query breed_picker database to get breed data for later use."""
    
    breeds = Breed.query.all

    for breed in breeds:
        print(breed.name, breed.id)
        print('###################')

    return breeds