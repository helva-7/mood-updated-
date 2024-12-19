from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association tables for many-to-many relationships
user_genres = db.Table(
    'user_genres',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

user_artists = db.Table(
    'user_artists',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    setup_complete = db.Column(db.Boolean, default=False)
    preferred_genre = db.Column(db.String(100), nullable=True) 

    # Many-to-many relationships
    genres = db.relationship('Genre', secondary=user_genres, backref='users')
    artists = db.relationship('Artist', secondary=user_artists, backref='users')

# Genre model
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Artist model
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
