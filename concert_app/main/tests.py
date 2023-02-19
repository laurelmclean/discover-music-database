import os
import unittest
import app

from datetime import date
from concert_app.extensions import app, db, bcrypt
from concert_app.models import Concert, Artist, User

"""
Run these tests with:
python3 -m unittest concert_app.main.tests
"""

#################################################
# Setup
#################################################


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def new_concert():
    artist = Artist(
        name='Band',
        hometown= 'Calgary',
        image='https://iamthemountainmusic.files.wordpress.com/2022/01/iatmband.jpg?w=739',
        genre='Punk',
        biography='Punk band from Calgary'
    )
    concert = Concert(
        name='Funfest',
        price='10',
        venue='The venue',
        address='123 Main Street',
        date=date(2023, 7, 11),
        artist_playing=artist
    )
    db.session.add(concert)
    db.session.commit()


def create_user():
    # Creates a user with username 'laurel1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='laurel1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the concerts show up on the homepage."""
        new_concert()
        create_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Funfest', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Logout', response_text)

    def test_homepage_logged_in(self):
        """Test that the concerts show up on the homepage."""
        # Set up
        new_concert()
        create_user()
        login(self.app, 'laurel1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Funfest', response_text)
        self.assertIn('New Concert', response_text)
        self.assertIn('New Artist', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_concert_detail_logged_out(self):
        """Test that the concert appears on its detail page."""
        new_concert()
        create_user()

        # Make a GET request to the URL /concert/1, check to see that the
        # status code is 200
        response = self.app.get('/concert/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains what we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Funfest", response_text)
        self.assertIn("10", response_text)

        # Check that the response does NOT contain the 'Favorite' button
        # (it should only be shown to logged in users)
        self.assertNotIn("Logout", response_text)

    def test_concert_detail_logged_in(self):
        """Test that the concert appears on its detail page."""
        new_concert()
        create_user()
        login(self.app, 'laurel1', 'password')

        # Make a GET request to the URL /concert/1, check to see that the
        # status code is 200
        response = self.app.get('/concert/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains what we expect
        response_text = response.get_data(as_text=True)
        self.assertIn("Funfest", response_text)
        self.assertIn("10", response_text)

        # Check that the response contains the 'attend' button
        self.assertIn("Attend this Concert", response_text)

    def test_new_concert(self):
        """Test creating a concert."""
        # Set up
        create_user()
        new_concert()
        login(self.app, 'laurel1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Basement Dweller',
            'price': '25',
            'venue': 'Mikeys',
            'address': '123 Street',
            'date': '2023-01-12',
            'artist_playing': 1
        }
        self.app.post('/new_concert', data=post_data)

        # Make sure concert was updated as we'd expect
        created_concert = Concert.query.filter_by(
            name='Basement Dweller').one()
        self.assertIsNotNone(created_concert)
        self.assertEqual(created_concert.price, 25.0)

    def test_new_artist(self):
        """Test creating an artist."""
        # Create a user & login (so that the user can access the route)
        create_user()
        login(self.app, 'laurel1', 'password')

        # Make a POST request to the /new_artist route
        post_data = {
            'name': 'I Am The Mountain',
            'hometown': 'Calgary',
            'genre': 'rock',
            'biography': 'a band',
            'image': 'www.facebook.com'
        }
        self.app.post('/new_artist', data=post_data)

        # Verify that the artist was updated in the database
        created_artist = Artist.query.filter_by(name='I Am The Mountain').one()
        self.assertIsNotNone(created_artist)
        self.assertEqual(created_artist.biography, 'a band')


    def test_profile_page(self):
        # Make a GET request to the /profile/laurel1 route
        create_user()
        login(self.app, 'laurel1', 'password')

        # Verify that the response shows the appropriate user info
        response = self.app.get('/profile/laurel1')

        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("laurel1", response_text)

    def test_attend_concert(self):
        # Login as the user laurel1
        new_concert()
        create_user()
        login(self.app, 'laurel1', 'password')

        # Make a POST request to the /attend/1 route
        post_data = {
            'concert_id': 1
        }
        response = self.app.post('/attending/1', data=post_data)

        # Verify that the concert with id 1 was added to the user's attending
        user = User.query.filter_by(username='laurel1').one()
        concert = Concert.query.get(1)
        self.assertIn(concert, user.attending)

    def test_unattend_concert(self):
        create_user()
        login(self.app, 'laurel1', 'password')
        new_concert()

        # Make a POST request to the /unattend/1 route
        post_data = {
            'concert_id': 1
        }
        response = self.app.post('/unattend/1', data=post_data)

        # Verify that the concert with id 1 was removed from the user's
        # attending
        user = User.query.filter_by(username='laurel1').one()
        concert = Concert.query.get(1)
        self.assertNotIn(concert, user.attending)
