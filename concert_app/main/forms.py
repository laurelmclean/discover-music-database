from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from concert_app.models import Artist, Concert, User
from wtforms.fields.html5 import DateField

class ArtistForm(FlaskForm):
    """Form for adding/updating a new Artist."""

    name = StringField('Artist Name', validators=[DataRequired(), Length(
        min=3, max=80, message="The name needs to be between 3 and 80 chars")])
    hometown = StringField('Hometown', validators=[DataRequired(), Length(
        min=3, max=80, message="The hometown needs to be between 3 and 80 chars")])
    genre = StringField('Genre', validators=[DataRequired(), Length(
        min=3, max=80, message="The genre needs to be between 3 and 80 chars")])
    biography = StringField('Biography', validators=[DataRequired(), Length(
        min=3, max=3000, message="The biography must be less than 3000 chars")])
    image = StringField('Image URL')
    submit = SubmitField('Submit')


class ConcertForm(FlaskForm):
    """Form for adding/updating a Concert."""

    name = StringField('Concert Name', validators=[DataRequired(), Length(
        min=3, max=80, message="The name needs to be between 3 and 80 chars")])
    image = StringField('Image URL')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(
        min=0, max=500, message="Please enter a number between 0 and 500.")])
    venue = StringField('Venue Name', validators=[DataRequired(), Length(
        min=3, max=80, message="The venue name needs to be between 3 and 80 chars")])
    address = StringField('Address', validators=[DataRequired(), Length(
        min=3, max=80, message="The address needs to be between 3 and 80 chars")])
    date = DateField('Concert Date', validators=[DataRequired()])
    artist_playing = QuerySelectField('Artist Playing',
                                         query_factory=lambda: Artist.query, allow_blank=True)
    submit = SubmitField('Submit')
