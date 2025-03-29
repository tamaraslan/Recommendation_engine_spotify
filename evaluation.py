# evaluation.py

import random
import numpy as np
from recommenders import ubcf_recommend_from_matrix, popularity_recommender_filtered_for_eval
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_recommender_topN_ubcf(
    user_artists_scaled,
    n=5,
    given=5,
    sample_users=100,
    k=10
):
    """
    Evaluates the UBCF approach with real masking.
    For each user in the sample :
      - given' items are masked.
      - Recommendations are obtained via ubcf_recommend_from_matrix to calculate precision and recall.
      - For each of the masked items, the score is predicted via a weighted average of the scores of the k neighbors,
        and calculates the error (to obtain RMSE, MSE and MAE).
    Returns a tuple containing :
      (average precision, average recall, RMSE, MSE, MAE)
    """

    all_users = user_artists_scaled.index.tolist()
    if not all_users:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    test_users = random.sample(all_users, sample_users) if len(all_users) > sample_users else all_users

    R_original = user_artists_scaled.fillna(0).values
    artistIDs = list(user_artists_scaled.columns)
    user_to_idx = {u: i for i, u in enumerate(all_users)}

    precision_sum = 0.0
    recall_sum = 0.0
    squared_errors = []
    absolute_errors = []
    n_evaluated = 0

    for user in test_users:
        idx = user_to_idx[user]
        listened_indices = np.where(R_original[idx] != 0)[0]
        if len(listened_indices) < given:
            continue

        # Sélection de 'given' indices à masquer
        masked_indices = random.sample(list(listened_indices), given)
        R_train = R_original.copy()
        R_train[idx, masked_indices] = 0

        # Calcul des recommandations top-N
        recommended_cols = ubcf_recommend_from_matrix(R_train, user_idx=idx, k=k, n=n)
        recommended_items = [artistIDs[c] for c in recommended_cols]
        masked_items = [artistIDs[m] for m in masked_indices]
        hits = len(set(recommended_items).intersection(masked_items))
        precision = hits / n
        recall = hits / given
        precision_sum += precision
        recall_sum += recall

        # Calcul des prédictions de notes pour chacun des items masqués
        # Calcul de la similarité pour l'utilisateur courant
        sim_vector = cosine_similarity(R_train, R_train)[idx]
        sim_vector[idx] = 0
        neighbors_idx = sim_vector.argsort()[::-1][:k]
        for m_idx in masked_indices:
            neighbor_ratings = R_train[neighbors_idx, m_idx]
            neighbor_sims = sim_vector[neighbors_idx]
            if neighbor_sims.sum() > 0:
                pred = (neighbor_ratings * neighbor_sims).sum() / neighbor_sims.sum()
            else:
                pred = 0
            true_rating = R_original[idx, m_idx]
            squared_errors.append((pred - true_rating) ** 2)
            absolute_errors.append(abs(pred - true_rating))

        n_evaluated += 1

    if n_evaluated == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    precision_mean = precision_sum / n_evaluated
    recall_mean = recall_sum / n_evaluated
    mse = np.mean(squared_errors)
    rmse = np.sqrt(mse)
    mae = np.mean(absolute_errors)
    return precision_mean, recall_mean, rmse, mse, mae

def evaluate_recommender_topN_pop(
    user_artists_top,
    user_artists_scaled,
    n=5,
    given=5,
    sample_users=100
):
    """
    Evaluates the popularity model (filtered) with real masking.
    For each user in the sample:
      1. Copy user_artists_scaled into R_train_df.
      2. mask 'given' items for this user.
      3. Call popularity_recommender_filtered_for_eval to obtain top-N list (for precision/recall).
      4. For each masked item, the score is predicted as the average of other users' scores (excluding the current user).
      5. The predicted score is compared with the actual score to calculate RMSE, MSE and MAE.
    Returns a tuple: (average precision, average recall, RMSE, MSE, MAE)
    """
    import numpy as np

    all_users = user_artists_scaled.index.tolist()
    if not all_users:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    test_users = (
        random.sample(all_users, sample_users)
        if len(all_users) > sample_users
        else all_users
    )

    precision_sum = 0.0
    recall_sum = 0.0
    squared_errors = []
    absolute_errors = []
    n_evaluated = 0

    for user in test_users:
        #  Copy the DataFrame to simulate the training set
        R_train_df = user_artists_scaled.copy()
        listened_items = R_train_df.loc[user].dropna().index.tolist()
        if len(listened_items) < given:
            continue

        masked_items = random.sample(listened_items, given)

        # Real masking: replace masked items with NaN for this user
        for item in masked_items:
            R_train_df.at[user, item] = float('nan')

        rec_list = popularity_recommender_filtered_for_eval(R_train_df, user, n=n)
        hits = len(set(rec_list).intersection(set(masked_items)))
        precision = hits / n
        recall = hits / given
        precision_sum += precision
        recall_sum += recall

        #For each hidden item, predict the score as the average of other users' scores
        for item in masked_items:
            pred = user_artists_scaled.drop(user)[item].mean(skipna=True)
            true_rating = user_artists_scaled.loc[user, item]
            # If the prediction is nan (for example, no other user has listened to the item), the item can be ignored.
            if np.isnan(pred):
                continue
            squared_errors.append((pred - true_rating) ** 2)
            absolute_errors.append(abs(pred - true_rating))

        n_evaluated += 1

    if n_evaluated == 0 or len(squared_errors) == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    precision_mean = precision_sum / n_evaluated
    recall_mean = recall_sum / n_evaluated
    mse = np.mean(squared_errors)
    rmse = np.sqrt(mse)
    mae = np.mean(absolute_errors)
    return precision_mean, recall_mean, rmse, mse, mae



def evaluate_recommender_topN_random(
    user_artists_scaled,
    n=5,
    given=5,
    sample_users=100
):
    """
    Evaluates a random baseline.
    For each user in the sample, 'given' items are masked from the listened items.
    Then, n items are randomly selected from those not listened to (candidates),
    and calculate precision and recall.
    """
    all_users = user_artists_scaled.index.tolist()
    if not all_users:
        return 0.0, 0.0

    test_users = random.sample(all_users, sample_users) if len(all_users) > sample_users else all_users
    artistIDs = user_artists_scaled.columns
    precision_sum = 0.0
    recall_sum = 0.0
    n_evaluated = 0

    for user in test_users:
        # For this user, we determine the items listened to
        user_row = user_artists_scaled.loc[user]
        listened_items = user_row.dropna().index.tolist()
        if len(listened_items) < given:
            continue

        masked_items = random.sample(listened_items, given)

        # Define candidate set: all unlistened items (NaN)
        candidate_items = user_row[user_row.isna()].index.tolist()
        if len(candidate_items) < n:
            continue
        random_recs = random.sample(candidate_items, n)

        hits = len(set(random_recs).intersection(masked_items))
        precision = hits / n
        recall = hits / given
        precision_sum += precision
        recall_sum += recall
        n_evaluated += 1

    if n_evaluated == 0:
        return 0.0, 0.0
    return precision_sum / n_evaluated, recall_sum / n_evaluated

def mega_evaluation(
    user_artists_scaled,
    user_artists_top,
    n=5,
    given=5,
    sample_users=100,
    k=10,
    iterations=10
):
    """
    Launches 'iterations' complete evaluations for each of the 3 algorithms:
      - UBCF
      - Popularity
      - Random Baseline
    Returns 3 lists of precision measurements (one per iteration) for each algorithm.
    """
    ubcf_precisions = []
    pop_precisions = []
    random_precisions = []

    for i in range(iterations):
        prec_ubcf, _ = evaluate_recommender_topN_ubcf(user_artists_scaled, n, given, sample_users, k)
        prec_pop, _ = evaluate_recommender_topN_pop(user_artists_top, user_artists_scaled, n, given, sample_users)
        prec_rand, _ = evaluate_recommender_topN_random(user_artists_scaled, n, given, sample_users)
        ubcf_precisions.append(prec_ubcf)
        pop_precisions.append(prec_pop)
        random_precisions.append(prec_rand)
    return ubcf_precisions, pop_precisions, random_precisions
