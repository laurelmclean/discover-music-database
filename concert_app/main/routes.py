from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from concert_app.models import Artist, Concert, User
from concert_app.main.forms import ArtistForm, ConcertForm

from concert_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    """Homepage route"""
    all_concerts = Concert.query.all()
    print(all_concerts)
    return render_template('home.html', all_concerts=all_concerts)


@main.route('/concert')
def all_concerts():
    """Concert route"""
    all_concerts = Concert.query.all()
    print(all_concerts)
    return render_template('all_concerts.html', all_concerts=all_concerts)

@main.route('/artist')
def all_artists():
    """Artists route"""
    all_artists = Artist.query.all()
    print(all_artists)
    return render_template('all_artists.html', all_artists=all_artists)

@main.route('/new_artist', methods=['GET', 'POST'])
@login_required
def new_artist():
    """Add a new artist"""
    form = ArtistForm()

    if form.validate_on_submit():
        new_artist = Artist(
            name=form.name.data,
            hometown=form.hometown.data,
            image=form.image.data,
            genre=form.genre.data,
            biography=form.biography.data
        )
        db.session.add(new_artist)
        db.session.commit()

        flash('New artist was created successfully.')
        return redirect(url_for('main.artist_detail', artist_id=new_artist.id))

    return render_template('new_artist.html', form=form)

@main.route('/new_concert', methods=['GET', 'POST'])
@login_required
def new_concert():
    """Add new concert"""
    form = ConcertForm()

    if form.validate_on_submit():
        new_concert = Concert(
            name=form.name.data,
            price=form.price.data,
            image=form.image.data,
            venue=form.venue.data,
            address=form.address.data,
            date=form.date.data,
            artist_playing=form.artist_playing.data
        )
        db.session.add(new_concert)
        db.session.commit()

        flash('New concert was created successfully.')
        return redirect(url_for('main.concert_detail', concert_id=new_concert.id))

    return render_template('new_concert.html', form=form)

@main.route('/artist/<artist_id>', methods=['GET', 'POST'])
def artist_detail(artist_id):
    """Artist details"""
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    if form.validate_on_submit():
        artist.name = form.name.data,
        artist.hometown = form.hometown.data,
        artist.image = form.image.data,
        artist.genre = form.genre.data,
        artist.biography = form.biography.data

        db.session.add(artist)
        db.session.commit()

        flash('Artist updated successfully.')
        return redirect(url_for('main.artist_detail', artist_id=artist.id))

    artist = Artist.query.get(artist_id)
    return render_template('artist_detail.html', artist=artist, form=form)

@main.route('/concert/<concert_id>', methods=['GET', 'POST'])
def concert_detail(concert_id):
    """Concert details"""
    concert = Concert.query.get(concert_id)
    form = ConcertForm(obj=concert)

    if form.validate_on_submit():
        concert.name = form.name.data,
        concert.price = form.price.data,
        concert.image = form.image.data,
        concert.venue = form.venue.data,
        concert.address = form.address.data,
        concert.date = form.date.data,
        concert.artist_playing = form.artist_playing.data

        db.session.add(concert)
        db.session.commit()

        flash('Concert updated successfully.')
        return redirect(url_for('main.artist_detail', concert_id=concert.id))

    concert = Concert.query.get(concert_id)
    return render_template('concert_details.html', concert=concert, form=form)

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)


