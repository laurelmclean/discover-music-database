import os
from unittest import TestCase
import app

from datetime import date

from concert_app.extensions import app, db, bcrypt
from concert_app.models import Concert, Artist, User

"""
Run these tests with the command:
python3 -m unittest concert_app.auth.tests
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
        hometown='Calgary',
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


class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        create_user()
        post_data = {
            'username': 'laurelmclean1',
            'password': 'Password1',
        }
        self.app.post('/signup', data=post_data)

        response = self.app.get('/profile/laurelmclean1')
        response_text = response.get_data(as_text=True)
        self.assertIn('laurelmclean1', response_text)

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'username': 'laurel1',
            'password': 'password',
        }
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn(
            'That username is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):

        create_user()
        post_data = {
            'username': 'laurel1',
            'password': 'password',
        }
        self.app.post('/login', data=post_data)
        # - Check that the "login" button is not displayed on the homepage
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)

        self.assertNotIn('login', response_text)

    def test_login_nonexistent_user(self):

        post_data = {
            'username': 'newaccount',
            'password': 'dogs123',
        }
        response = self.app.post('/login', data=post_data)
  
        response_text = response.get_data(as_text=True)
        self.assertIn(
            'No user with that username. Please try again.', response_text)

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'username': 'laurel1',
            'password': 'wrongpassword',
        }

        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)

        self.assertIn(
            'Password doesn&#39;t match. Please try again.', response_text)

    def test_logout(self):
        create_user()
        post_data = {
            'username': 'laurel1',
            'password': 'password',
        }

        self.app.post('/login', data=post_data)
        self.app.get('/logout')
        # - Check that the "login" button appears on the homepage
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)
