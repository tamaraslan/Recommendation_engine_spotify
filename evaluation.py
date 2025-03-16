# evaluation.py

import random
import numpy as np
from recommenders import ubcf_recommend_from_matrix, popularity_recommender_filtered_for_eval

def evaluate_recommender_topN_ubcf(
    user_artists_scaled,
    n=5,
    given=5,
    sample_users=100,
    k=10
):
    """
    Evaluates UBCF with real masking.
    For each user in the sample, we mask 'given' items in their row,
    then obtain recommendations via ubcf_recommend_from_matrix.
    Returns (precision, recall) means.
    """
    all_users = user_artists_scaled.index.tolist()
    if not all_users:
        return 0.0, 0.0

    test_users = random.sample(all_users, sample_users) if len(all_users) > sample_users else all_users

    R_original = user_artists_scaled.fillna(0).values
    artistIDs = user_artists_scaled.columns
    user_to_idx = {u: i for i, u in enumerate(all_users)}

    precision_sum = 0.0
    recall_sum = 0.0
    n_evaluated = 0

    for user in test_users:
        idx = user_to_idx[user]
        listened_indices = np.where(R_original[idx] != 0)[0]
        if len(listened_indices) < given:
            continue

        masked_indices = random.sample(list(listened_indices), given)
        R_train = R_original.copy()
        R_train[idx, masked_indices] = 0

        recommended_cols = ubcf_recommend_from_matrix(R_train, user_idx=idx, k=k, n=n)
        recommended_artistIDs = [artistIDs[c] for c in recommended_cols]

        hits = len(set(recommended_artistIDs).intersection([artistIDs[m] for m in masked_indices]))
        precision = hits / n
        recall = hits / given
        precision_sum += precision
        recall_sum += recall
        n_evaluated += 1

    if n_evaluated == 0:
        return 0.0, 0.0
    return precision_sum / n_evaluated, recall_sum / n_evaluated

def evaluate_recommender_topN_pop(
    user_artists_top,
    user_artists_scaled,
    n=5,
    given=5,
    sample_users=100
):
    """
    Evaluates the Popularity model (filtered) with real masking.
    For each user in the sample:
      1. Copy user_artists_scaled to R_train_df.
      2. Set NaN 'given' items for this user.
      3. Call popularity_recommender_filtered_for_eval(R_train_df, user, n).
      4. Compare list with hidden items to calculate precision and recall.
    Returns (precision, recall) means.
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
        # Check that the user has listened to enough items
        R_train_df = user_artists_scaled.copy()
        listened_items = R_train_df.loc[user].dropna().index.tolist()
        if len(listened_items) < given:
            continue

        masked_items = random.sample(listened_items, given)

        # Real masking: items masked for this user are set to NaN
        for item in masked_items:
            R_train_df.at[user, item] = float('nan')

        rec_list = popularity_recommender_filtered_for_eval(R_train_df, user, n=n)
        hits = len(set(rec_list).intersection(masked_items))
        precision = hits / n
        recall = hits / given
        precision_sum += precision
        recall_sum += recall
        n_evaluated += 1

    if n_evaluated == 0:
        return 0.0, 0.0
    return precision_sum / n_evaluated, recall_sum / n_evaluated

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
