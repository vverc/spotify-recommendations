import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd

# load Spotify API credentials from dotenv
load_dotenv()


scope = "user-library-read user-follow-read user-top-read playlist-read-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT"),
    )
)


def print_full(x):
    pd.set_option("display.max_rows", len(x))
    print(x)
    pd.reset_option("display.max_rows")


from data_functions import get_spotify_data, process_artist_data, process_track_data

"""
Want to get 
sp.current_user_top_artists()
sp.current_user_followed_artists()
sp.current_user_top_tracks()
sp.current_user_playlists()

need to pull spotify recommended songs to use as song candidates
sp.recommendations() 
"""
