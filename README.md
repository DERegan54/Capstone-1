## THE FAMILY DOG

This application was created as my Capstone 1 project for Springboard's Software Engineering Career Track program.

External API: "https://api.api-ninjas.com/v1/dogs"
Deployed Application: https://the-family-dog.herokuapp.com/


## Description
The Family Dog is web application that helps users decide which dog breeds best fit their lifestyle.  


## Features
- Create a user profile
- Search by breed name or breed characteristic to receive photos and helpful information about the dog breed
- Save favorite breeds to user profile
- Leave reviews of breeds the user has experience with
- See other users' reviews of breeds they are interested in.
- Find an agency for adoption of both purebred dogs and rescues


## User Flow
Login and registration handled on serverside with use of Flask and WTForms. Users are able to sign up and create a profile where they specify their household makeup (number of adults and children in the household), other pets in the household, living environment (urban, suburban or rural), and their experience with dogs.  They can also update and/or delete their profile as needed. When logged in users can add and remove their favorite breeds to their user profile as well as leave a review of dog breeds they have experience with for other users to reference. The review feature allows the user to rate the breed on a scale of 1(least) to 5(most) in several categories including maintenance required, obedience, and trainability, as well as leave information in the comments section that they think will be helpful to other users. Signup and Login are not required to browse and search dog breeds.  Users are able to search by breed name or by desireable characteristics, including minimal barking, minimal shedding, minimal energy, maximum protectiveness and maximum trainability. There is a page of resources for the user to turn to when they are ready to adopt their newest family member.  


## Tech Stack

Languages:
HTML5
Python
PostgreSQL

Libraries/Tools:
Bcrypt
Flask
Flask-DebugToolbar
Jinja2
SQLAlchemy
Unittest
WTForms
