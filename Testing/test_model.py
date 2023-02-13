""" User Model Tests """

# run these tests with:
#    python -m unittest test_user_model.py

from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Breed, Review, Favorite
from user import login_user, logout_user
from api_requests import add_breed_search_to_db, add_characteristic_search_to_db, search_breeds, search_characteristic
import os
# testing database
# set this before importing the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///breed_picker_test'
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
API_KEY = os.environ.get('API_KEY')
API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

##############################################################################################
# USER MODEL TESTS
##############################################################################################

class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()

        user1 = User.signup(
                "testuser", 
                "test@test.com",
                "password",
                )
        user1.id = 10

        db.session.commit()

        user1 = User.query.get(user1.id)

        self.user1  = user1
        self.user1_id = user1.id
        
        self.client = app.test_client()

     

    def tearDown(self):
        """Clean up transactions."""

        db.session.rollback()


    def test_user_model(self):
        """Check if user model works"""

        user = User(
            username="testuser3",
            password="password",
            email="test@test.com",
            profile_PHOTO=None
        )

        db.session.add(user)
        db.session.commit()

        self.assertEqual(len(user.favorites), 0)


    def test_create_valid_user(self):
        """Successfully create new user given valid credentials"""

        new_user = User.signup("testuser4",
                               "test4@test.com", 
                               "password"
                               )
        user_id = 40
        new_user.id = user_id

        db.session.commit()

        new_user = User.query.get(new_user.id)
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.username, "testuser4")
        self.assertEqual(new_user.email, "test4@test.com")
        self.assertNotEqual(new_user.password, "password")  # reason we test for not equal is because it should be encrypted


    def test_create_user_with_invalid_username(self):
        """Tests if user creation fails if username validation fails."""

        invalid_user = User.signup(None,
                                  "test@test.com",                           
                                  "password" 
                                )
        
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


 
    def test_create_user_with_invalid_email(self):
        """Testing if validation checks if there is a valid email inputted"""
    
        invalid = User.signup("test", 
                             None,
                             "password"
                                )
        
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()



    def test_create_user_with_invalid_password(self):
        """Testing if validation checks if there is a valid password inputted"""

        with self.assertRaises(ValueError) as context:
            User.signup("test", 
                        "test@test.com",
                        "" # invalid password. Must be at least 6 characters 
                        )


    def test_authentication(self):
        """Successful return given valid username and password"""
    
        user = User.authenticate(self.user1.username, "password")
        
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user1_id)


    def test_invalid_username(self):
        """Failure given invalid username"""
    
        self.assertFalse(User.authenticate("invalid_username", "password"))


    def test_invalid_password(self):
        """Failure given invalid password"""
        
        self.assertFalse(User.authenticate(self.user1.username, "wrongpassword"))


    





      