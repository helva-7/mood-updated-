from azure.storage.queue import QueueClient
import os

# Set up your Azure Storage connection string and queue name
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=musicstorage123;AccountKey=KN5LAJC8JQW6gSfR0gK4s//mPm0+ZykdqU2xy/PdTwsAgb2cbfT31xDvNW5icL6C+dh1sG3hj8xx+AStV9+MVg==;EndpointSuffix=core.windows.net"
QUEUE_NAME = "musicgenresandartists"

# List of genres and artists
genres = [
    "rock", "pop", "hip-hop", "classical", "jazz", "electronic", "blues", "country", 
    "metal", "reggae", "funk", "soul", "indie", "house", "trance", "folk", "punk", 
    "disco", "R&B", "techno", "dubstep", "grunge", "trap", "lo-fi", "orchestral", 
    "ambient", "garage", "ska", "gospel", "opera", "k-pop", "j-pop", "c-pop", 
    "afrobeats", "dancehall", "synthwave", "hardstyle", "drum and bass", "swing", 
    "big band", "flamenco", "latin pop", "bossa nova", "tango", "samba", "cumbia", 
    "reggaeton", "hard rock", "progressive rock", "alternative rock", "post-rock", 
    "heavy metal", "death metal", "black metal", "power metal", "neo-soul", "acoustic", 
    "chillout", "world music", "ethnic", "new wave", "emo", "shoegaze", "vaporwave", 
    "post-punk", "trip-hop", "electro-pop", "singer-songwriter", "grime", "brostep", 
    "psychedelic", "krautrock", "chamber music", "baroque", "romantic", "minimalism", 
    "soundtracks", "video game music", "industrial", "experimental", "spoken word"
]


artists = [
    # Rock
    "The Beatles", "Queen", "Nirvana", "Pink Floyd", "Led Zeppelin", "The Rolling Stones", 
    "AC/DC", "Guns N' Roses", "Jimi Hendrix", "U2", "Metallica", "Aerosmith", "David Bowie", 
    "Fleetwood Mac", "The Who", "Bruce Springsteen", "The Eagles", "Radiohead", "Green Day", 
    "Foo Fighters", "Red Hot Chili Peppers",

    # Pop
    "Michael Jackson", "Madonna", "Taylor Swift", "Ariana Grande", "Katy Perry", "Lady Gaga", 
    "Justin Bieber", "Dua Lipa", "Ed Sheeran", "Bruno Mars", "Beyoncé", "Harry Styles", 
    "Rihanna", "Shawn Mendes", "The Weeknd", "Billie Eilish", "Olivia Rodrigo", "Britney Spears", 

    # Hip-Hop
    "Kanye West", "Drake", "Eminem", "Jay-Z", "Kendrick Lamar", "Travis Scott", "Lil Wayne", 
    "50 Cent", "Nicki Minaj", "Megan Thee Stallion", "Cardi B", "Tyler, The Creator", 
    "J. Cole", "Snoop Dogg", "Tupac Shakur", "Notorious B.I.G.", "Nas", "Ice Cube", 

    # Jazz & Blues
    "Miles Davis", "Louis Armstrong", "John Coltrane", "Duke Ellington", "Charlie Parker", 
    "Billie Holiday", "B.B. King", "Ray Charles", "Etta James", "Nina Simone", 

    # Electronic
    "Daft Punk", "Calvin Harris", "David Guetta", "Deadmau5", "Skrillex", "Martin Garrix", 
    "Kygo", "Avicii", "Tiesto", "Armin van Buuren", "The Chemical Brothers", "Marshmello",

    # Classical
    "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach", 
    "Franz Schubert", "Pyotr Ilyich Tchaikovsky", "Frédéric Chopin", "Antonio Vivaldi", 
    "Claude Debussy", "Giuseppe Verdi", "Igor Stravinsky",

    # R&B & Soul
    "Marvin Gaye", "Aretha Franklin", "Stevie Wonder", "Whitney Houston", "Sam Cooke", 
    "Usher", "Mary J. Blige", "Alicia Keys", "John Legend", "Toni Braxton", "Luther Vandross",

    # Latin
    "Shakira", "Enrique Iglesias", "Marc Anthony", "Ricky Martin", "Bad Bunny", 
    "J Balvin", "Daddy Yankee", "Selena Quintanilla", "Gloria Estefan", "Juanes", 

    # Indie & Folk
    "Bon Iver", "Fleet Foxes", "Mumford & Sons", "Sufjan Stevens", "Vampire Weekend", 
    "The Lumineers", "Iron & Wine", "Of Monsters and Men", "Bright Eyes", "Jose Gonzalez",

    # Reggae
    "Bob Marley", "Peter Tosh", "Jimmy Cliff", "Toots and the Maytals", "Damian Marley", 
    "Burning Spear", "Ziggy Marley", "UB40", "Gregory Isaacs",

    # Other Global Artists
    "BTS", "BLACKPINK", "PSY", "IU", "EXO", "Coldplay", "Rammstein", "Stromae", 
    "Amr Diab", "Fela Kuti", "Yemi Alade", "Celia Cruz", "Andrea Bocelli", "Enya"
]


# Initialize the QueueClient
try:
    queue_client = QueueClient.from_connection_string(CONNECTION_STRING, QUEUE_NAME)
    print(f"Connected to queue: {QUEUE_NAME}")
except Exception as e:
    print("Error connecting to the queue:", str(e))
    exit()

# Add genres and artists to the queue
def add_messages_to_queue():
    try:
        # Push genres to the queue
        for genre in genres:
            message = f"genre:{genre}"
            queue_client.send_message(message)
            print(f"Added message: {message}")

        # Push artists to the queue
        for artist in artists:
            message = f"artist:{artist}"
            queue_client.send_message(message)
            print(f"Added message: {message}")

        print("\nAll genres and artists have been added to the queue successfully!")

    except Exception as e:
        print("Error adding messages to the queue:", str(e))

# Run the function
if __name__ == "__main__":
    add_messages_to_queue()
