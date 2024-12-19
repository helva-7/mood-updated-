import os
from googleapiclient.discovery import build
import logging

# Initialize YouTube API
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YouTube API Key not found in environment variables")

# Set up logging for better tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_youtube(mood, genres, artists, max_results=10):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Generate queries for mood, genres, and artists
    queries = []

    # Add queries for mood and genres
    if mood:
        queries.extend([f"{mood} {genre} music" for genre in genres])

    # Add queries for mood and artists
    if artists:
        queries.extend([f"{mood} {artist}" for artist in artists])

    # Add generic genre and artist queries without mood
    queries.extend([f"{genre} music" for genre in genres])
    queries.extend([f"{artist}" for artist in artists])

    results = []

    # Debugging: Log all queries
    logger.info(f"Generated Queries: {queries}")

    for query in queries:
        if len(results) >= max_results:  # Limit the total results
            break

        try:
            # Call the YouTube API for each query
            request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=min(max_results - len(results), 10),  # Limit results per query
                relevanceLanguage="en",  # Optional: Focus on English results
            )
            response = request.execute()

            # Log the query and response for debugging
            logger.info(f"Searching for query: {query}")
            logger.info(f"Response: {response}")

            # Parse the results and add them to the list
            for item in response.get("items", []):
                results.append({
                    "title": item["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                })

        except Exception as e:
            logger.error(f"Error while searching for query '{query}': {e}")
            continue  # Continue to the next query if there was an error

    # Log final results
    logger.info(f"Total results found: {len(results)}")
    
    if not results:
        logger.warning("No results found for the search queries.")
    
    return results
