from flask import request
from secrets import API_KEY
from models import db, Breed
import requests

API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'

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

    data = search_breeds(query)  # Querys dogs API with search input and saves response to 'data' variable    
    for breed in data:
        breed_keys = list(breed.keys())
        breed_values = list(breed.values())
        breed_dict = dict(zip(breed_keys, breed_values))
        name = breed_dict['name']
        exists = db.session.query(Breed.name).filter_by(name=name).first() is not None  # Check if name exists in breed_picker database
        if exists == False:
            breed = Breed( # Create a model instance called 'breed' from the record data...  
                image_link = breed['image_link'],
                good_with_children = breed['good_with_children'],
                good_with_other_dogs = breed['good_with_other_dogs'],
                shedding = breed['shedding'],
                coat_length = breed['coat_length'],
                trainability = breed['trainability'],
                barking = breed['barking'],
                min_life_expectancy = breed['min_life_expectancy'],
                max_life_expectancy = breed['max_life_expectancy'],
                max_height_male = breed['max_height_male'],
                max_height_female = breed['max_height_female'],
                max_weight_male = breed['max_weight_male'],
                max_weight_female = breed['max_weight_female'],
                min_height_male = breed['min_height_male'],
                min_height_female = breed['min_height_female'],
                min_weight_male = breed['min_weight_male'],
                min_weight_female = breed['min_weight_female'],
                grooming = breed['grooming'],
                drooling = breed['drooling'],
                good_with_strangers = breed['good_with_strangers'],
                playfulness = breed['playfulness'],
                protectiveness = breed['protectiveness'],
                energy = breed['energy'],
                name = breed['name']
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
    
    data = search_characteristic(breed_characteristic)  # Query dogs API with characteristic input and save response to 'data' variable
    for breed in data:
        breed_keys = list(breed.keys())
        breed_values = list(breed.values())
        breed_dict = dict(zip(breed_keys, breed_values))
        name = breed_dict['name']
        exists = db.session.query(Breed.name).filter_by(name=name).first() is not None  # Check if name exists in breed_picker database
        if exists == False:
            breed = Breed( # Create a model instance called 'breed' from the record data...  
                image_link = breed['image_link'],
                good_with_children = breed['good_with_children'],
                good_with_other_dogs = breed['good_with_other_dogs'],
                shedding = breed['shedding'],
                coat_length = breed['coat_length'],
                trainability = breed['trainability'],
                barking = breed['barking'],
                min_life_expectancy = breed['min_life_expectancy'],
                max_life_expectancy = breed['max_life_expectancy'],
                max_height_male = breed['max_height_male'],
                max_height_female = breed['max_height_female'],
                max_weight_male = breed['max_weight_male'],
                max_weight_female = breed['max_weight_female'],
                min_height_male = breed['min_height_male'],
                min_height_female = breed['min_height_female'],
                min_weight_male = breed['min_weight_male'],
                min_weight_female = breed['min_weight_female'],
                grooming = breed['grooming'],
                drooling = breed['drooling'],
                good_with_strangers = breed['good_with_strangers'],
                playfulness = breed['playfulness'],
                protectiveness = breed['protectiveness'],
                energy = breed['energy'],
                name = breed['name']
            )
            db.session.add(breed) # add the breed to the breed_picker database
    db.session.commit() # save database changes
    
    return breed  #return newly created breed record 

    

    




