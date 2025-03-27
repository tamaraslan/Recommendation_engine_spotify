# spotify_images.py

import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

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

# Cache for images and top tracks
spotify_image_cache = {}
spotify_top_tracks_cache = {}

def get_spotify_artist_image(artist_name: str) -> str:
    """
    Searches for the artist by name via the Spotify API and returns the URL of its first image.
    Uses a cache to limit calls to the API.
    On error or if no image is found, returns a placeholder.
    """
    if artist_name in spotify_image_cache:
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

def get_spotify_artist_top_tracks(artist_name: str, country: str = 'US', limit: int = 5) -> list:
    """
    Searches for the artist by name via the Spotify API and returns a list of the top track names.
    Uses a cache to limit API calls.
    On error or if no tracks are found, returns an empty list.
    """
    if artist_name in spotify_top_tracks_cache:
        return spotify_top_tracks_cache[artist_name]

    try:
        results = sp.search(q=artist_name, type="artist", limit=1)
        items = results["artists"]["items"]
        if items:
            artist_id = items[0]["id"]
            top_tracks_result = sp.artist_top_tracks(artist_id, country=country)
            tracks = top_tracks_result.get("tracks", [])
            top_tracks = [track["name"] for track in tracks][:limit]
            spotify_top_tracks_cache[artist_name] = top_tracks
            return top_tracks
    except Exception as e:
        print(f"Error retrieving top tracks for {artist_name}: {e}")

    spotify_top_tracks_cache[artist_name] = []
    return []
