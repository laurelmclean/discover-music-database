from sqlalchemy_utils import URLType
from flask_login import UserMixin
from concert_app.extensions import db

class Artist(db.Model):
    """Artist model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(80), nullable=False)
    image = db.Column(URLType)
    genre = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.String(250), nullable=False)
    upcoming_concerts = db.relationship(
        'Concert', secondary='artist_concert', back_populates='bands_playing')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

class Concert(db.Model):
    """Concert model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    venue = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date)
    bands_playing = db.relationship(
        'Artist', secondary='artist_concert', back_populates='upcoming_concerts')
    guests_attending = db.relationship(
        'User', secondary='user_concert', back_populates='attending')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

artist_concert = db.Table('artist_concert',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.id'))
)


class User(db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    attending = db.relationship(
        'Concert', secondary='user_concert', back_populates='guests_attending')

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'{self.username}'

user_concert = db.Table('user_concert',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('concert_id', db.Integer, db.ForeignKey('concert.id'))
)

