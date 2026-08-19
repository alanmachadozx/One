from dotenv import load_dotenv
import os 
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager= SpotifyOAuth(
    client_id= os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret= os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri= os.getenv("SPOTIPY_REDIRECT_URI"),
    scope= "user-modify-playback-state user-read-playback-state"
))
