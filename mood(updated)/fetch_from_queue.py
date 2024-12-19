# fetch_from_queue.py
import os
from azure.storage.queue import QueueClient

# Function to fetch and parse items from the queue
def fetch_and_parse_queue():
    from flask import current_app
    with current_app.app_context():  # Ensure we're within the app context
        from models import Genre, Artist  # Import only when needed to avoid circular imports

        # Initialize QueueClient
        AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        QUEUE_NAME = os.getenv('QUEUE_NAME')
        queue_client = QueueClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, QUEUE_NAME)

        # Fetch messages from the queue
        messages = queue_client.receive_messages(messages_per_page=32)
        genres = []
        artists = []

        for msg in messages:
            content = msg.content.strip()  # Ensure no leading/trailing spaces
            if content.startswith("genre:"):
                genres.append(content.replace("genre:", "").strip())
            elif content.startswith("artist:"):
                artists.append(content.replace("artist:", "").strip())

        return genres, artists

# Function to fetch and insert genres and artists from the queue
def fetch_and_insert_from_queue():
    from flask import current_app
    with current_app.app_context():  # Ensure we're within the app context
        from models import db, Genre, Artist  # Import models here to avoid circular imports

        # Initialize QueueClient
        AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        QUEUE_NAME = os.getenv('QUEUE_NAME')
        queue_client = QueueClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING, QUEUE_NAME)

        # Fetch messages from the queue
        messages = queue_client.receive_messages(messages_per_page=32)
        genres = []
        artists = []

        for msg in messages:
            content = msg.content.strip()  # Ensure no leading/trailing spaces
            if content.startswith("genre:"):
                genres.append(content.replace("genre:", "").strip())
            elif content.startswith("artist:"):
                artists.append(content.replace("artist:", "").strip())

        # Insert genres into the database
        for genre_name in genres:
            genre = Genre.query.filter_by(name=genre_name).first()
            if not genre:
                new_genre = Genre(name=genre_name)
                db.session.add(new_genre)

        # Insert artists into the database
        for artist_name in artists:
            artist = Artist.query.filter_by(name=artist_name).first()
            if not artist:
                new_artist = Artist(name=artist_name)
                db.session.add(new_artist)

        db.session.commit()  # Commit the changes
        print("Genres and artists have been successfully inserted!")

# Call the function only when needed
if __name__ == "__main__":
    fetch_and_insert_from_queue()
