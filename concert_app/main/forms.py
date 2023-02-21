from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from concert_app.models import Artist, Concert, User
from wtforms.fields.html5 import DateField

class ArtistForm(FlaskForm):
    """Form for adding/updating a new Artist."""

    name = StringField('Artist Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    biography = StringField('Biography', validators=[DataRequired()])
    image = StringField('Image URL')
    submit = SubmitField('Submit')


class ConcertForm(FlaskForm):
    """Form for adding/updating a Concert."""

    name = StringField('Concert Name', validators=[DataRequired()])
    image = StringField('Image URL')
    price = FloatField('Price', validators=[DataRequired()])
    venue = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    date = DateField('Concert Date', validators=[DataRequired()])
    artist_playing = QuerySelectField('Artist Playing',
                                         query_factory=lambda: Artist.query, allow_blank=True)
    submit = SubmitField('Submit')
