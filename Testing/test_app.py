"""View Function Tests."""

# run these tests with:
# python -m unittest test_app.py

from unittest import TestCase
from models import db, connect_db,  db, User, Breed, Review, Favorite
import os

# testing database
# set this before importing the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///breed_picker_test'

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

from app import app, CURR_USER_KEY
API_KEY = os.environ.get('API_KEY')
API_BASE_URL = 'https://api.api-ninjas.com/v1/dogs?'
# Create our tables (we do this here, so we only create the tables
# once for all tests.  In each test, we'll delete the data
# and create new test data

db.drop_all()
db.create_all()

#############################################################################################
# SETUP AND TEARDOWN
#############################################################################################

class ViewFunctionsTests(TestCase):
    """Test views for cards."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any foul transaction."""

        db.session.rollback()
    

##############################################################################################
# SEARCH VIEW FUNCTION TESTS
##############################################################################################

    def test_show_breed_search_results(self):
        """Displays breed information for breed searched."""

        with app.test_client() as client:
            response = client.get('/breed_search_results?breed_search=beagle', follow_redirects=True)
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h4>Breed Search Results:</h4>', html)


    def test_show_characteristic_search_results(self):
        """Displays breeds returned from characteristics search."""

        with app.test_client() as client:
            response = client.get('/characteristic_search_results?breed_characteristic=energy', follow_redirects = True)
            html = response.get_data(as_text = True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<h4>Characteristic Search Results:</h4>', html)    


##############################################################################################
# REVIEW VIEW FUNCTION TESTS
##############################################################################################

class ReviewsViewsTestCase(TestCase):
    """Test views for cards."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any foul transaction."""

        db.session.rollback()
    
    def test_show_all_reviews(self):
        """Display all breed reviews."""

        with app.test_client() as client:
            response = client.get('/reviews/list_reviews', follow_redirects = True)
            html = response.get_data(as_text = True)   

        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>All Breed Reviews:</h1>', html)

    
    def test_show_review_form(self):
        """Show breed review form."""

        with app.test_client() as client:
            response = client.get('/reviews/review_form?', follow_redirects = True)
            html = response.get_data(as_text = True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<h3>Review the Breed</h3>', html)


    def test_add_review(self):
        """ Add breed review to database.  Redirect to my_reviews page. """

        with app.test_client as client:
            response = client.post('/reviews/add_review', data = {'breed_name': 'Beagle',
                                                                  'maintenance_rating': 3,
                                                                  'behavior_rating': 3,
                                                                  'trainability_rating': 3,
                                                                  'comments': 'Beagles are so cute!'})
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h4>Beagle</h4>', html)

    
    def test_show_edit_review_form(self):
        """Show edit breed review form."""

        with app.test_client() as client:
            response = client.get('/reviews/<int:review_id>/edit_review_form', follow_redirects = True)
            html = response.get_data(as_text = True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h3>Edit your Breed Review</h3>', html)

    # Since the data is deleted after each test, how do we get the data we will be editing into the database before this test?
    def test_edit_breed_review(self):
        """Update breed reveiw and add to database."""

        with app.test_client() as client:
            response = client.post('/reviews/<int:review_id>/edit_review', data = {'breed_name': 'Beagle', 
                                                                                   'maintenance_rating': 4,
                                                                                   'behavior_rating': 4,
                                                                                   'trainability_rating': 4, 
                                                                                   'comments': 'Beagles are so sweet!'})
            html = response.get_data(as_text = True)        

            self.assertEqual(response.status_code, 200)
            self.assertIn('<b>Comments:</b>Beagles are so sweet!', html)


    # How do we test delete routes?  This was not in the videos
    # def test_delete_breed_review(review_id):
    #     """Delete breed review from database."""