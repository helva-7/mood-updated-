import os
import hashlib
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from youtube_search import search_youtube
from dotenv import load_dotenv
from models import db, User , Genre , Artist  # Assuming models.py has a SQLAlchemy setup
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

# Emulate genres and artists
genres = ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical"]
artists = ["Adele", "Drake", "Taylor Swift", "Eminem", "Beyoncé"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Perform user registration (e.g., save to the database)
        if register_user(username, password):
            # After successful registration, redirect to login page
            return redirect(url_for('login'))
        else:
            # Handle registration failure
            flash("Registration failed, please try again.")
    return render_template('register.html')




# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        hashed_pwd = hash_password(password)

        if user and user.password == hashed_pwd:
            session["user_id"] = user.id
            session["username"] = user.username

            # Redirect to setup page if setup is not complete
            if not user.setup_complete:
                return redirect(url_for("setup"))
            else:
                return redirect(url_for("home"))  # Redirect to the homepage
        else:
            return render_template("login.html", error="Invalid email or password.")
    return render_template("login.html")


# Setup Route
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.setup_complete:
        # Redirect to homepage if setup is already complete
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Get selected genres and artists from the form
        selected_genres = request.form.getlist('genres')
        selected_artists = request.form.getlist('artists')

        # Fetch and associate genres
        genres = Genre.query.filter(Genre.id.in_(selected_genres)).all()
        for genre in genres:
            if genre not in user.genres:
                user.genres.append(genre)

        # Fetch and associate artists
        artists = Artist.query.filter(Artist.id.in_(selected_artists)).all()
        for artist in artists:
            if artist not in user.artists:
                user.artists.append(artist)

        # Mark setup as complete
        user.setup_complete = True
        db.session.commit()

        # Redirect to the homepage
        return redirect(url_for('home'))

    # Fetch all available genres and artists for the setup form
    all_genres = Genre.query.all()
    all_artists = Artist.query.all()

    return render_template('setup.html', genres=all_genres, artists=all_artists)

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get the current user from the session
    user = User.query.get(session["user_id"])

    # Ensure the user has completed their setup and has genres and artists
    if user.setup_complete:
        if request.method == "POST":
            # Get the mood from the form submission
            mood = request.form.get("mood")

            # Get the user's selected genres and artists
            genres = [genre.name for genre in user.genres]  # Extract genre names
            artists = [artist.name for artist in user.artists]  # Extract artist names

            # Perform the search using the user's genres and artists
            videos = search_youtube(mood, genres, artists)

            # Return the search results
            return render_template("home.html", videos=videos, mood=mood)

        return render_template("home.html")  # Just render the page if it's a GET request
    else:
        # If the user hasn't completed their setup, redirect to the setup page
        return redirect(url_for("setup"))



@app.route("/search", methods=["POST"])
def search():
    try:
        # Get mood from user input
        mood = request.form.get("mood")

        # Search YouTube with refined queries based on genres and artists
        videos = search_youtube(mood, genres, artists)
        return render_template("partials/results.html", videos=videos, mood=mood)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Something went wrong while searching YouTube."}), 500

@app.route('/fetch_genres', methods=['GET'])
def fetch_genres():
    genres = Genre.query.all()
    return render_template("partials/fetch_genres.html", genres=genres)

@app.route('/fetch_artists', methods=['GET'])
def fetch_artists():
    artists = Artist.query.all()
    return render_template("partials/fetch_artists.html", artists=artists)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
