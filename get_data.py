import os
import spotipy
import pandas as pd
import pickle as pk

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

from data_functions import (
    get_spotify_data,
    process_artist_data,
    process_track_data,
    get_playlist_tracks,
    get_recommendations,
)

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


"""
    sp.current_user_top_artists
    sp.current_user_top_tracks

    fetch top yearly songs from 2021 to 2019
    sp.playlist
"""

# get yearly top song playlists
print("Getting songs from user's yearly Top Song playlists")
yearly_top_playlists = sp.current_user_playlists()["items"]
yearly_top_playlists = list(
    filter(lambda x: x["name"].startswith("Your Top Songs"), yearly_top_playlists)
)
yearly_top_df = get_playlist_tracks(sp, yearly_top_playlists)
yearly_top_df.to_pickle("data/yearly_top.pkl")

"""
# get recent top songs
print("Getting user's top songs")
top_songs_df = get_spotify_data(sp, sp.current_user_top_tracks())
top_songs_df.to_pickle("data/top_songs.pkl")
# get top artists
print("Getting user top artists")
top_artists_df = get_spotify_data(sp, sp.current_user_top_artists())
top_artists_df.to_pickle("data/top_artists.pkl")
"""
print("Getting user's saved songs")
saved_songs_df = get_spotify_data(sp, sp.current_user_saved_tracks())
saved_songs_df.to_pickle("data/saved_songs.pkl")


"""
# get recommendations

print("Getting song recommendations from Spotify")
recommended_songs_df = get_recommendations(
    sp, yearly_top_df.drop_duplicates(subset="id", keep="first")["id"].tolist()
)
recommended_songs_df.to_pickle("data/recommendations.pkl")
"""
