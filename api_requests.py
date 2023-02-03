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
# FUNCTIONS FOR MAKING REQUESTS TO DOGS API
############################################################################

def add_breed_to_db():
    """Adds model instance of breed to database."""
    # Issues: 
    # - If there is more than one record returned from the search, how to save all records to the database  
   
    data = search_breeds()  # Query dogs API with search input and save response to 'data' variable
    name = data[0]['name']  # Get the 'name' (breed name) attribute from the first record in data and save to 'name' variable to access that record
    exists = db.session.query(Breed.name).filter_by(name=name).first() is not None  # Check if name exists in breed_picker database
    for i in data:     # For each record i in data...
        name =  i['name']  # (Accessing record through name attribute)
        if exists == False:  # If that record does not exist in breed_picker database....
            breed = Breed(      # Create a model instance called 'breed' from the record data...  
                image_link = i['image_link'],
                good_with_children = i['good_with_children'],
                good_with_other_dogs = i['good_with_other_dogs'],
                shedding = i['shedding'],
                coat_length = i['coat_length'],
                trainability = i['trainability'],
                barking = i['barking'],
                min_life_expectancy = i['min_life_expectancy'],
                max_life_expectancy = i['max_life_expectancy'],
                max_height_male = i['max_height_male'],
                max_height_female = i['max_height_female'],
                max_weight_male = i['max_weight_male'],
                max_weight_female = i['max_weight_female'],
                min_height_male = i['min_height_male'],
                min_height_female = i['min_height_female'],
                min_weight_male = i['min_weight_male'],
                min_weight_female = i['min_weight_female'],
                grooming = i['grooming'],
                drooling = i['drooling'],
                good_with_strangers = i['good_with_strangers'],
                playfulness = i['playfulness'],
                protectiveness = i['protectiveness'],
                energy = i['energy'],
                name = i['name']
            )
            db.session.add(breed) # add the breed to the breed_picker database
            db.session.commit() # save database changes
            return breed  #return newly created breed record 
    

def search_breeds():
    """Querys dogs API to get dog breed info."""

    query = request.args.get('breed_search')  # Grab input from 'breed_search' and save to 'query' variable 
   
    try:
        url = f'{API_BASE_URL}name={query}'   # Add query to endpoint
        response = requests.get(url, headers={'X-Api-Key': API_KEY})  # Get query from dogs API
        data = response.json()  # Save response data to 'data' variable
        
        return data   #return data
        
    except:
        flash("Invalid search. Please enter a breed.", "danger")  # If search is invalid, flash message and redirect to search page
        return redirect("/search")

   

def request_individual_breed(query):
    """Return individual breed's data."""
    
    query = request.args.get('breed_search')  # Grab input from 'breed_search' and save to 'query' variable 
   
    url= f'{API_BASE_URL}/name={name}'
    response = requests.get(url)
    data = response.json()
