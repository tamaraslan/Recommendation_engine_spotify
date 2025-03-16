# data_loader.py

import pandas as pd

def scale_row(row):
    """
    Standardizes a series by subtracting the mean and dividing by the standard deviation,
    ignoring NaN. If the standard deviation is zero, only centering is performed.
    """
    row_mean = row.mean(skipna=True)
    row_std = row.std(skipna=True)
    if row_std == 0:
        return row - row_mean
    else:
        return (row - row_mean) / row_std

def load_and_transform_data(artists_path="data/artists_gp3.dat", user_artists_path="data/user_artists_gp3.dat"):
    """
    1. Load artists.dat and user_artists.dat files
    2. Filter user_artists to keep only IDs present in artists
    3. Converts to wide format (pivot_table)
    4. Selects the 1000 most popular artists
    5. Filters out users who have listened to more than 10 artists
    6. Normalize (centering-reduction) by user
    7. Builds a dict artist_id -> artist_name

    Returns :
      - user_artists_scaled: normalized DataFrame (index = userID, columns = artistID)
      - user_artists_top: DataFrame for recommendation by popularity
      - artist_id_to_name : dict { artist_id: artist_name }
    """
    # Reading of files
    artists = pd.read_csv(artists_path, sep="\t", header=0)
    user_artists = pd.read_csv(user_artists_path, sep="\t", header=0)

    # All valid IDs (present in artists)
    valid_artist_ids = set(artists["id"].unique())

    # Filter user_artists to keep only those whose artistID is in valid_artist_ids
    user_artists = user_artists[user_artists["artistID"].isin(valid_artist_ids)]

    # Mapping : artist_id -> name
    artist_id_to_name = dict(zip(artists["id"], artists["name"]))

    # Conversion to wide format
    user_artists_wide = user_artists.pivot_table(index="userID", columns="artistID", values="weight")

    # Selection of the 1000 most popular artists
    artist_listens = user_artists_wide.sum(axis=0, skipna=True)
    top_1000_artists = artist_listens.sort_values(ascending=False).head(1000).index
    user_artists_top = user_artists_wide[top_1000_artists]

    # Filtering of users who have listened to at least 11 artists
    user_listens_count = user_artists_top.count(axis=1)
    user_artists_top = user_artists_top[user_listens_count > 10]

    # Normalization (centering-reduction) by user
    user_artists_scaled = user_artists_top.apply(scale_row, axis=1)

    return user_artists_scaled, user_artists_top, artist_id_to_name
