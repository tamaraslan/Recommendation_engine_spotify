# app.py

import streamlit as st
import random
import altair as alt
import pandas as pd

from data_loader import load_and_transform_data
from recommenders import (
    popularity_recommender_filtered,
    ubcf_recommend_for_display
)
from evaluation import (
    evaluate_recommender_topN_ubcf,
    evaluate_recommender_topN_pop,
    evaluate_recommender_topN_random,
    mega_evaluation
)
from spotify_images import get_spotify_artist_image, get_spotify_artist_top_tracks

# Import our new function
from spotify_styled_display import display_spotify_styled_recommendation

st.set_page_config(
    page_title="Spotify recommendation system",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
/* Base styles */
[data-testid="stAppViewContainer"] {
  background-color: #191414;
}

#MainMenu, footer {
  visibility: hidden;
}

.block-container {
  margin-top: clamp(1em, 2vw, 2em);
  margin-bottom: clamp(3em, 5vw, 5em);
  padding: 0 clamp(1em, 3vw, 2em);
}

body {
  background-color: #121212 !important;
  color: #FFFFFF !important;
  font-family: "Circular", -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.5;
}

/* Buttons */
.stButton > button {
  background-color: #1DB954;
  color: white;
  border-radius: 500px;
  border: none;
  font-weight: 700;
  padding: 0.8em 2em;
  margin: 0.5em 0;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.875rem;
}

.stButton > button:hover {
  background-color: #1ED760;
  transform: scale(1.04);
  color: white;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #1DB954;
  border-radius: 4px;
  transition: all 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: #1ED760;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  color: #1DB954;
  letter-spacing: -0.04em;
  margin-bottom: 1em;
}

/* Card Grid */
.horizontal-scroller {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: clamp(1em, 2vw, 1.5em);
  margin-bottom: 2em;
  padding: 1em;
}

@media (max-width: 768px) {
  .horizontal-scroller {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}

.card {
  background-color: #181818;
  border-radius: 8px;
  padding: 1em;
  text-align: center;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.card:hover {
  background-color: #282828;
}

.card img {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 8px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.card:hover img {
  transform: scale(1.05);
}

/* Columns */
.stColumn {
  background-color: #000000;
  border-radius: 16px;
  padding: clamp(1em, 3vw, 2em);
  transition: transform 0.3s ease;
}

.stColumn:hover {
  transform: translateY(-4px);
}

/* Menu styling */
.spotify-menu {
  background-color: #000000;
  border-radius: 16px;
  padding: 1.5em;
}

.spotify-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.spotify-menu li {
  margin: 0.5em 0;
}

.spotify-menu a {
  color: #b3b3b3;
  text-decoration: none;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  padding: 0.5em;
  border-radius: 4px;
}

.spotify-menu a:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.1);
}

/* Player bar */
.player-bar {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #181818;
  padding: 1em;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 9999;
  border-top: 1px solid #282828;
}

.player-controls {
  display: flex;
  gap: 1em;
  align-items: center;
}

.player-button {
  background: none;
  border: none;
  color: #1DB954;
  font-size: 1.2em;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.player-button:hover {
  transform: scale(1.1);
  color: #1ED760;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .player-bar {
    flex-direction: column;
    gap: 1em;
    padding: 0.8em;
  }
  
  .block-container {
    margin-bottom: 8em;
  }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def main():
    # Header
    st.markdown(
        """
        <div style="background-color: #000000; padding: 1em 1em; display: flex; align-items: center; margin:10px; 
        border-radius:30px;">
          <img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg"
               style="height: 40px; margin-right: 1em;" />
          <h2 style="margin: 0;">Recommendation engine</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_menu, col_main = st.columns([2, 8], gap="small")

    with col_menu:
        st.write("")
        st.markdown("<h3 style='color:#1DB954;background-color:#000000;border-radius:30px;'>Menu</h3>", unsafe_allow_html=True)
        st.markdown("""
        <ul style="list-style:none; padding-left:0; line-height:1.8; background-color:#000000; border-radius:30px;">
          <li><a href="#" style="color:white; text-decoration:none;">Home</a></li>
          <li><a href="#" style="color:white; text-decoration:none;">Research</a></li>
          <li><a href="#" style="color:white; text-decoration:none;">Your library</a></li>
          <hr style="border:1px solid #333;">
          <li><a href="#" style="color:white; text-decoration:none;">Playlists</a></li>
          <li><a href="#" style="color:white; text-decoration:none;">Liked Songs</a></li>
          <li><a href="#" style="color:white; text-decoration:none;">Podcasts</a></li>
          <li><a href="#" style="color:white; text-decoration:none;">...</a></li>
        </ul>
        """, unsafe_allow_html=True)
        st.write("---")

        # Loading data
        st.subheader("Settings")
        artists_path = st.text_input("Path to artists.dat", "data/artists_gp3.dat")
        user_artists_path = st.text_input("Path to user_artists.dat", "data/user_artists_gp3.dat")

        if st.button("Load and preprocess"):
            try:
                user_artists_scaled, user_artists_top, artist_id_to_name = load_and_transform_data(
                    artists_path, user_artists_path
                )
                st.session_state["user_artists_scaled"] = user_artists_scaled
                st.session_state["user_artists_top"] = user_artists_top
                st.session_state["artist_id_to_name"] = artist_id_to_name
                st.session_state["all_users"] = list(user_artists_scaled.index)
                st.session_state["user_to_idx"] = {u: i for i, u in enumerate(st.session_state["all_users"])}
                st.success("Data load and preprocess successfully!")
                st.write("Dimension DataFrame:", user_artists_scaled.shape)
            except Exception as e:
                st.error(f"Error: {e}")

        if "user_artists_scaled" in st.session_state:
            st.subheader("Recommendations")
            k_neighbors = st.slider("Number of neighbours (k)", 1, 50, 10)
            n_items = st.slider("Number of recommended artist", 1, 20, 5)
            st.subheader("Evaluation")
            given = st.slider("Hidden Artists (given)", 1, 20, 5)
            sample_users = st.slider("Users Sample", 10, 900, 100)

    with col_main:
        st.subheader("Recommendation (unmasked)")

        # Check data loaded
        if "user_artists_scaled" in st.session_state:
            all_users = st.session_state["all_users"]
            if all_users:
                selected_user = st.selectbox("Choose a user:", all_users)
            else:
                st.warning("No available user.")
                return

            if st.button("Show recommendations"):
                # Popularity approach
                st.markdown("### Popularity (filtered)")
                pop_list = popularity_recommender_filtered(
                    st.session_state["user_artists_top"],
                    st.session_state["user_artists_scaled"],
                    selected_user,
                    n=n_items
                )
                if pop_list:
                    for i, artist_id in enumerate(pop_list, start=1):
                        artist_name = st.session_state["artist_id_to_name"].get(artist_id, "Unknown artist")
                        cover_url = get_spotify_artist_image(artist_name)
                        sub_info = f"Vidéo • Titre • {artist_name}"
                        top_tracks = get_spotify_artist_top_tracks(artist_name)
                        track_list = [(t, "3:30") for t in top_tracks]  # placeholders

                        display_spotify_styled_recommendation(
                            block_title=f"Recommended Artist #{i} (Popularity)",
                            artist_name=artist_name,
                            cover_url=cover_url,
                            sub_info=sub_info,
                            track_list=track_list,
                            block_height=350
                        )
                else:
                    st.warning("No popularity-based recommendations found.")

                # UBCF approach
                st.write("---")
                st.markdown("### UBCF (classic)")
                ubcf_list = ubcf_recommend_for_display(
                    st.session_state["user_artists_scaled"],
                    st.session_state["user_to_idx"],
                    selected_user,
                    k=k_neighbors,
                    n=n_items
                )
                if ubcf_list:
                    for i, artist_id in enumerate(ubcf_list, start=1):
                        artist_name = st.session_state["artist_id_to_name"].get(artist_id, "Unknown artist")
                        cover_url = get_spotify_artist_image(artist_name)
                        sub_info = f"Vidéo • Titre • {artist_name}"
                        top_tracks = get_spotify_artist_top_tracks(artist_name)
                        track_list = [(t, "3:30") for t in top_tracks]

                        display_spotify_styled_recommendation(
                            block_title=f"Recommended Artist #{i} (UBCF)",
                            artist_name=artist_name,
                            cover_url=cover_url,
                            sub_info=sub_info,
                            track_list=track_list,
                            block_height=350
                        )
                else:
                    st.warning("No UBCF-based recommendations found.")

            # Evaluate
            if st.button("Evaluating models for n=[1, 3, 5, 10, 15, 20]"):
                topNs = [1, 3, 5, 10, 15, 20]

                st.markdown("### UBCF Evaluation for various top-N")
                for topN in topNs:
                    prec_ubcf, recall_ubcf, rmse_ubcf, mse_ubcf, mae_ubcf = evaluate_recommender_topN_ubcf(
                        user_artists_scaled=st.session_state["user_artists_scaled"],
                        n=topN,
                        given=given,
                        sample_users=sample_users,
                        k=k_neighbors
                    )
                    st.write(
                        f"Top-{topN} UBCF - Precision: {prec_ubcf:.3f} | Recall: {recall_ubcf:.3f} | RMSE: {rmse_ubcf:.3f} | MSE: {mse_ubcf:.3f} | MAE: {mae_ubcf:.3f}")

                st.markdown("### Popularity Evaluation for various top-N")
                for topN in topNs:
                    prec_pop, recall_pop, rmse_pop, mse_pop, mae_pop = evaluate_recommender_topN_pop(
                        user_artists_top=st.session_state["user_artists_top"],
                        user_artists_scaled=st.session_state["user_artists_scaled"],
                        n=topN,
                        given=given,
                        sample_users=sample_users
                    )
                    st.write(
                        f"Top-{topN} Popularity - Precision: {prec_pop:.3f} | Recall: {recall_pop:.3f} | RMSE: {rmse_pop:.3f} | MSE: {mse_pop:.3f} | MAE: {mae_pop:.3f}")

                st.markdown("### Random Baseline Evaluation (top-N)")
                for topN in topNs:
                    prec_rand, recall_rand = evaluate_recommender_topN_random(
                        user_artists_scaled=st.session_state["user_artists_scaled"],
                        n=topN,
                        given=given,
                        sample_users=sample_users
                    )
                    st.write(f"Top-{topN} Random - Precision: {prec_rand:.3f} | Recall: {recall_rand:.3f}")

            if st.button("Mega Evaluation (10 iterations)"):
                ubcf_list_vals, pop_list_vals, rand_list_vals = mega_evaluation(
                    st.session_state["user_artists_scaled"],
                    st.session_state["user_artists_top"],
                    n=n_items,
                    given=given,
                    sample_users=sample_users,
                    k=k_neighbors,
                    iterations=10
                )
                iterations = list(range(1, 11))
                data = pd.DataFrame({
                    "Iteration": iterations,
                    "UBCF": ubcf_list_vals,
                    "Popularity": pop_list_vals,
                    "Random": rand_list_vals
                })
                chart = alt.Chart(data.melt('Iteration', var_name='Model', value_name='Accuracy')).mark_line(point=True).encode(
                    x="Iteration:O",
                    y="Accuracy:Q",
                    color="Model:N"
                ).properties(
                    title="Evolution of accuracy (10 iterations)"
                )
                st.altair_chart(chart, use_container_width=True)

    st.markdown("""
    <div style="position:fixed; left:0; bottom:0; width:100%; background-color:#181818; 
                padding:0.7em; display:flex; align-items:center; justify-content:center; z-index:9999;">
      <div style="flex:1; margin-left:1em; color:#1DB954; font-weight:bold;">
        <button style="background:none; border:none; color:#1DB954; margin-right:0.5em;">⏮️</button>
        <button style="background:none; border:none; color:#1DB954; margin-right:0.5em;">⏯️</button>
        <button style="background:none; border:none; color:#1DB954;">⏭️</button>
      </div>
      <div style="flex:1; text-align:center; color:#1DB954;">
        Powered by RECOMIND Solutions
      </div>
      <div style="flex:1;"></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
