import pandas as pd


def get_spotify_data(sp, sp_call):
    res = sp_call
    data = res["items"]
    print("DEBUG: initial calls")
    while res["next"]:
        res = sp.next(res)
        data.extend(res["items"])

    if "type" in data[0]:
        if data[0]["type"] == "artist":
            data = process_artist_data(data)
        elif data[0]["type"] == "track":
            data = process_track_data(sp, data)
    else:
        data = process_track_data(sp, data)
    return data


def get_playlist_tracks(sp, data):
    # return df of playlist tracks with additional playlist data
    playlists = data

    playlist_tracks = pd.DataFrame()
    print("DEBUG: initial calls")
    for playlist in playlists:
        res = sp.playlist(playlist["id"], fields="tracks,next")
        res = res["tracks"]
        data = []
        data.extend(res["items"])
        while res["next"]:
            res = sp.next(res)
            data.extend(res["items"])

        tracks = process_track_data(sp, data)
        tracks["playlist_id"] = playlist["id"]
        tracks["playlist_name"] = playlist["name"]
        playlist_tracks = pd.concat([playlist_tracks, tracks])

    return playlist_tracks


def process_artist_data(data):
    df = pd.DataFrame(data)
    return df[["id", "uri", "name", "popularity", "genres"]]


def process_track_data(sp, data):
    print("DEBUG: processing track data")
    df = pd.DataFrame(data)

    if "track" in df.columns.tolist():
        df = df.drop("track", axis=1).assign(**df["track"].apply(pd.Series))

    df = df.drop_duplicates(subset="id", keep="first")

    df["album_id"] = df["album"].apply(lambda x: x["id"])
    df["album_name"] = df["album"].apply(lambda x: x["name"])
    df["album_type"] = df["album"].apply(lambda x: x["album_type"])
    df["album_release"] = df["album"].apply(lambda x: x["release_date"])

    df["artist_id"] = df["artists"].apply(lambda x: x[0]["id"])
    df["artist_name"] = df["artists"].apply(lambda x: x[0]["name"])

    columns = [
        "id",
        "name",
        "popularity",
        "artist_id",
        "artist_name",
        "album_id",
        "album_name",
        "album_type",
        "album_release",
        "duration_ms",
    ]

    if "added_at" in df.columns.tolist():
        columns.append("added_at")

    df = df[columns]

    # additional calls for more data

    # batch API calls for audio_features and artist genres
    track_ids = df["id"].tolist()
    artist_ids = df["artist_id"].tolist()
    batch_size = 50

    audio_features = []
    artists = []

    for i in range(0, len(track_ids), batch_size):
        batch_track_ids = track_ids[i : i + batch_size]
        batch_artist_ids = artist_ids[i : i + batch_size]

        batch_audio_features = sp.audio_features(batch_track_ids)
        batch_artists = sp.artists(batch_artist_ids)["artists"]

        audio_features.extend(batch_audio_features)
        artists.extend(batch_artists)

    audio_features_df = pd.DataFrame(audio_features).apply(pd.Series)
    artists_df = pd.DataFrame(artists)

    df = pd.merge(df, artists_df[["genres", "id"]], on="id", how="left")
    df = pd.merge(df, audio_features_df, on="id", how="left")
    df = df.drop(["analysis_url", "track_href", "uri", "type"], axis=1)

    return df


def get_recommendations(sp, tracks):
    """
    gets
    """
    data = []
    for track in tracks:
        res = sp.recommendations(seed_tracks=[track], limit=5)
        data.extend(res["tracks"])

    return process_track_data(sp, data)
