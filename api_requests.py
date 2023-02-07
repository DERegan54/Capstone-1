from flask import Flask, render_template, request, flash, redirect, session, g
from secrets import API_KEY
from models import db, connect_db, User, Breed, Review 
import requests
import json


API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'
LOCAL_BASE_URL = 'http://127.0.0.1:5000/'


############################################################################
# FUNCTIONS FOR MAKING REQUESTS TO DOGS API
############################################################################

def search_breeds(query):
    """Querys dogs API by breed name."""

    query = request.args.get('breed_search')  # Grabs input from 'breed_search' and saves to 'query' variable 
   
    url = f'{API_BASE_URL}name={query}'   # Add query to endpoint
    response = requests.get(url, headers={'X-Api-Key': API_KEY})  # Get records from dogs API
    data = response.json()  # Save response data to 'data' variable
        
    return data  


def add_breed_search_to_db(query):
    """Adds model instance of breed to database."""
    # Issues: 
    # - If there is more than one record returned from the search, how to save all records to the database  
   
    data = search_breeds(query)  # Query dogs API with search input and save response to 'data' variable
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


def search_characteristic(breed_characteristic): 
    """Query's dogs API by breed characteristic. """

    breed_characteristic = request.args.get('breed_characteristic')  # Grabs input from 'characteristic_search'
    
    if breed_characteristic == 'barking':
        url = f'{API_BASE_URL}barking=1' # Add breed_characteristic to endpoint url
        url2 = f'{API_BASE_URL}barking=1;offset=20'  # If there are more than 20 records for that characteristic, create the necessary additional endpoint url(s) to access all records
        response = requests.get(url, headers={'X-Api-Key': API_KEY})  #Make API call with each endpoint url
        response2 = requests.get(url2, headers={'X-Api-Key': API_KEY})
        data = response.json() # Transform json list into python list for first call
        data2 = response2.json()  # Transform json list into python list for second call
        for i in data2: # Merge python lists to return one list of all records
            data.append(i)
            return data 
    elif breed_characteristic =='shedding':
        url = f'{API_BASE_URL}shedding=1'
        url2 = f'{API_BASE_URL}shedding-1;offset=20'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response2 = requests.get(url2, headers={'X-Api-Key': API_KEY})
        data = response.json()
        data2 = response2.json()
        for i in data2:
            data.append(i)
            return data 
    elif breed_characteristic == 'energy':
        url = f'{API_BASE_URL}energy=2'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        data = response.json()
        return data 
    elif breed_characteristic == 'protectiveness':
        url = f'{API_BASE_URL}protectiveness=5'
        url2 = f'{API_BASE_URL}protectiveness=5;offset=20'
        url3 = f'{API_BASE_URL}protectiveness=5;offset=40'
        url4 = f'{API_BASE_URL}protectiveness=5;offset=60'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response2 = requests.get(url2, headers={'X-Api-Key': API_KEY})
        response3 = requests.get(url3, headers={'X-Api-Key': API_KEY})
        response4 = requests.get(url4, headers={'X-Api-Key': API_KEY})
        data = response.json()
        data2 = response2.json()
        data3 = response3.json()
        data4 = response4.json()
        for i in data2:
            data.append(i)
        for i in data3:
            data.append(i)
        for i in data4:
            data.append(i)
        return data 
    elif breed_characteristic == 'trainability':
        url = f'{API_BASE_URL}trainability=5'
        url2 = f'{API_BASE_URL}trainability=5;offset=20'
        url3 = f'{API_BASE_URL}trainability=5;offset=40'
        url4 = f'{API_BASE_URL}trainability=5;offset=60'
        response = requests.get(url, headers={'X-Api-Key': API_KEY})
        response2 = requests.get(url2, headers={'X-Api-Key': API_KEY})
        response3 = requests.get(url3, headers={'X-Api-Key': API_KEY})
        response4 = requests.get(url4, headers={'X-Api-Key': API_KEY})
        data = response.json()
        data2 = response2.json()
        data3 = response3.json()
        data4 = response4.json()
        for i in data2:
            data.append(i)
        for i in data3:
            data.append(i)
        for i in data4:
            data.append(i)
        
        return data


def add_characteristic_search_to_db(breed_characteristic):
    """Adds model instance of breed to database."""
    # Issues: 
    # - If there is more than one record returned from the search, how to save all records to the database  
   
    data = search_characteristic(breed_characteristic)  # Query dogs API with characteristic input and save response to 'data' variable
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


    




