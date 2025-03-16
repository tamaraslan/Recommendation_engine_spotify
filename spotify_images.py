# spotify_images.py

import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# We use the api of Spotify for load image to practice.
# Doc : https://developer.spotify.com/documentation/web-api

# Load environment variables from .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError("The SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET keys are not defined in .env.")

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

spotify_image_cache = {}

def get_spotify_artist_image(artist_name: str) -> str:
    """
    Searches for the artist by name via the Spotify API and returns the URL of its first image.
    Uses a cache to limit calls to the API.
    On error or if no image is found, returns a placeholder.
    """

    if artist_name in spotify_image_cache:

        # If the image is already loaded to avoid to make another request for nothing

        return spotify_image_cache[artist_name]

    try:
        results = sp.search(q=artist_name, type="artist", limit=1)
        items = results["artists"]["items"]
        if items:
            images = items[0].get("images", [])
            if images:
                url_image = images[0]["url"]
                spotify_image_cache[artist_name] = url_image
                return url_image
    except Exception as e:
        print(f"Error for {artist_name}: {e}")

    placeholder = "https://via.placeholder.com/150/1DB954/FFFFFF?text=Artist"
    spotify_image_cache[artist_name] = placeholder
    return placeholder
