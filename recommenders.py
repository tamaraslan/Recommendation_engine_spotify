# recommenders.py
from sklearn.metrics.pairwise import cosine_similarity

def popularity_recommender(user_artists_top, n=5):
    popularity = user_artists_top.sum(axis=0)
    top_artists = popularity.sort_values(ascending=False).head(n).index
    return list(top_artists)

def popularity_recommender_filtered(user_artists_top, user_artists_scaled, user_id, n=5):
    """
    Recommends the n most popular artists that the user has not yet listened to.
    (based on user_artists_scaled: if the user has a rating != NaN, it is assumed that he/she has listened to it).
    """
    pop_list = popularity_recommender(user_artists_top, n=100)
    listened_items = set(user_artists_scaled.loc[user_id].dropna().index)
    filtered = [item for item in pop_list if item not in listened_items]
    return filtered[:n]

def popularity_recommender_filtered_for_eval(R_train_df, user_id, n=5):
    """
    Calculates the list of popular artists in R_train_df (DataFrame),
    excluding those already listened to by user_id (non-NaN).
    """
    popularity = R_train_df.sum(axis=0, skipna=True)
    top_artists = popularity.sort_values(ascending=False).head(n*5).index

    listened_items = set(R_train_df.loc[user_id].dropna().index)
    filtered = [item for item in top_artists if item not in listened_items]
    return filtered[:n]
def ubcf_recommend_for_display(user_artists_scaled, user_to_idx, user_id, k=10, n=5):
    """
    UBCF without masking, for normal display.
    """
    R = user_artists_scaled.fillna(0).values
    idx = user_to_idx[user_id]
    sim_matrix = cosine_similarity(R)
    sim_vector = sim_matrix[idx].copy()
    sim_vector[idx] = 0
    neighbors_idx = sim_vector.argsort()[::-1][:k]
    user_ratings = R[idx]

    predictions = {}
    for j in range(R.shape[1]):
        if user_ratings[j] == 0:
            neighbor_ratings = R[neighbors_idx, j]
            neighbor_sims = sim_vector[neighbors_idx]
            if neighbor_sims.sum() > 0:
                pred = (neighbor_ratings * neighbor_sims).sum() / neighbor_sims.sum()
            else:
                pred = 0
            predictions[j] = pred

    top_items_idx = sorted(predictions, key=predictions.get, reverse=True)[:n]
    recommended_artists = [user_artists_scaled.columns[j] for j in top_items_idx]
    return recommended_artists

def ubcf_recommend_from_matrix(R_train, user_idx, k=10, n=5):
    """
    UBCF on a modified matrix (masking).
    """
    sim_matrix = cosine_similarity(R_train)
    sim_vector = sim_matrix[user_idx].copy()
    sim_vector[user_idx] = 0
    neighbors_idx = sim_vector.argsort()[::-1][:k]
    user_ratings = R_train[user_idx]

    predictions = {}
    for j in range(R_train.shape[1]):
        if user_ratings[j] == 0:
            neighbor_ratings = R_train[neighbors_idx, j]
            neighbor_sims = sim_vector[neighbors_idx]
            if neighbor_sims.sum() > 0:
                pred = (neighbor_ratings * neighbor_sims).sum() / neighbor_sims.sum()
            else:
                pred = 0
            predictions[j] = pred

    top_items_idx = sorted(predictions, key=predictions.get, reverse=True)[:n]
    return top_items_idx
