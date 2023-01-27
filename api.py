"""Handles requests to and responses from API Ninjas Dogs API."""

from secrets import API_KEY
import requests
import json

###########################################################
API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs'
###########################################################
# DOGS API REQUEST FUNCTIONS:

def get_breeds():
    """Format API response into list of dictionaries containing information on each breed.
    Breeds list format:
    [
        {
            "name" : name,
            "image_url" : image_url,
            "children" : children, 
            "dogs" : dogs,
            "barking" : barking,
            "shedding" : shedding,
            "grooming" : grooming,
            "drooling" : drooling,
            "energy" : energy, 
            "trainability" : trainability,
            "protectiveness" : protectiveness,
            "max_life_expectancy" : max_life_expectancy,
            "max_height_male" : max_height_male,
            "max_height_female" : max_height_female,
            "max_weight_male" : max_weight_male,
            "max_weight_female" : max_weight_female
        },
        ...
    ]
    """

    response = API_request()
    
    breeds  = []

    i = 0
    
    # grab results for first 20 breeds
    while i<=19:
        response1 = response
        response_str = str(response1)
        breed = json.loads(response_str)

        # Format API response into list of dictionaries containing information on each breed
            
        image_link = breed[i]['image_link']
        children = breed[i]['good_with_children'] 
        dogs = breed[i]['good_with_dogs']
        shedding = breed[i]['shedding']
        grooming = breed[i]['grooming']
        drooling = breed[i]['drooling']
        coat = breed[i]['coat_length']
        strangers = breed[i]['good_with_strangers']
        playfulness = breed[i]['playfulness']
        protectiveness = breed[i]['protectiveness']
        trainability = breed[i]['trainability']
        energy = breed[i]['energy']
        barking = breed()[i]['barking']
        min_life_expectancy = breed()[i]['min_life_expectancy']
        max_life_expectancy = breed[i]['max_life_expectancy']
        max_height_male = breed[i]['max_height_male']
        max_height_female = breed[i]['max_height_female']
        max_weight_male = breed[i]['max_weight_male']
        max_weight_female = breed[i]['max_weight_female']
        min_height_male = breed[i]['min_height_male']
        min_height_female = breed[i]["min_height_female"]
        min_weight_male = breed[i]['min_weight_male']
        min_weight_female = breed[i]['min_weight_female']
        name = breed[i]['name']
    
        # create breed dictionary from search results
        
        breed["image_link"] = image_link
        breed["good_with_children"] = children
        breed["good_with_other_dogs"] = dogs
        breed["shedding"] = shedding
        breed["grooming"] = grooming
        breed["drooling"] = drooling
        breed["coat_length"] = coat
        breed["good_with_strangers"] = strangers
        breed["playfulness"] = playfulness
        breed["protectiveness"] = protectiveness
        breed["trainiability"] = trainability
        breed["energy"] = energy
        breed["barking"] = barking
        breed["min_life_expectancy"] = min_life_expectancy
        breed["max_life_expectancy"] = max_life_expectancy
        breed["max_height_male"] = max_height_male
        breed["max_height_female"] = max_height_female
        breed["max_weight_male"] = max_weight_male
        breed["max_weight_female"] = max_weight_female
        breed["min_height_male"] = min_height_male
        breed["min_height_female"] = min_height_female
        breed["min_weight_male"] = min_weight_male
        breed["min_weight_female"] = min_weight_female
        breed["name"] = name
        print(breed)
        breeds.append(breed)
        i+=1
        print(breeds)

        return breeds

     
def API_request():
    """Searches API via barking endpoint to capture all breed records."""
    
    url = f'{API_BASE_URL}name="beagle"'
    response = requests.get(url, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    
    return response





    







    