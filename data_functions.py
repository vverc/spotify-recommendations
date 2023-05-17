import pandas as pd


def get_spotify_data(sp, sp_call):
    res = sp_call
    data = res["items"]
    while res["next"]:
        res = sp.next(res)
        data.extend(res["items"])
    return data


def process_artist_data(data):
    df = pd.DataFrame(data)
    return df[["id", "uri", "name", "popularity", "genres"]]


def process_track_data(sp, data):
    # Only grabs one artist, and one genre - genres might turn out funny
    df = pd.DataFrame(data)

    df["album_id"] = df["album"].apply(lambda x: x["id"])
    df["album_name"] = df["album"].apply(lambda x: x["name"])
    df["album_type"] = df["album"].apply(lambda x: x["album_type"])
    df["album_tracks"] = df["album"].apply(lambda x: x["total_tracks"])
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
        "album_tracks",
        "album_release",
        "duration_ms",
    ]

    df = df[columns]

    # additional calls for more data

    df["artist_genres"] = df["artist_id"].apply(lambda x: sp.artist(x)["genres"])

    df["audio_features"] = df["id"].apply(lambda x: sp.audio_features(x))
    df["audio_features"] = df["audio_features"].apply(pd.Series)
    df = df.drop("audio_features", 1).assign(**df["audio_features"].apply(pd.Series))
    df = df.drop(["analysis_url", "track_href", "uri", "type"], axis=1)
    return df
