"""View Function Tests."""

# run these tests with:
# python -m unittest test_app.py

from unittest import TestCase
from models import db, connect_db,  db, User, Breed, Review, Favorite

# testing database
# set this before importing the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///breed_picker_test'

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests.  In each test, we'll delete the data
# and create new test data

db.drop_all()
db.create_all()

##############################################################################################
# VIEW FUNCTION TEST CASES
##############################################################################################

class SearchViewsTestCase(TestCase):
    """Test views for cards."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any foul transaction."""

        db.session.rollback()
    

    def test_show_breed_search_results(self):
        """Displays breed information for breed searched."""

        with self.client as client:
            response = client.get('/breed_search_results?breed_search=beagle'
                             follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Search results for ", str(response.data))


    def test_show_characteristic_search_results(self):
        """Displays breeds returned from characteristics search."""

        with self.client as client:
            response = client.get('/characteristic_search_results?breed_characteristic=energy'
                             follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Search results for ", str(response.data))    

