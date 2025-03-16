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
from spotify_images import get_spotify_artist_image

st.set_page_config(
    page_title="Spotify recommendation system",
    page_icon=":musical_note:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Graphic for web interface

custom_css = """
<style>
[data-testid="stAppViewContainer"]{
background-color : #191414;
}
#MainMenu, footer {visibility: hidden;}
.block-container {
  margin-top: 1em;
  margin-bottom: 5em;
}
body {
  background-color: #121212 !important;
  color: #FFFFFF !important;
  font-family: "Arial", sans-serif;
}
.stButton > button {
  background-color: #1DB954;
  color: white;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  padding: 0.6em 1em;
  margin: 0.5em 0;
}
.stButton > button:hover {
  background-color: #1ED760;
  color: black;
}
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #191414;
}
::-webkit-scrollbar-thumb {
  background: #1DB954;
}
::-webkit-scrollbar-thumb:hover {
  background: #1ED760;
}
h1, h2, h3, h4, h5, h6 {
  color: #1DB954;
}
.horizontal-scroller {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 1em;
  margin-bottom: 1em;
}
.card {
  flex: 0 0 auto;
  width: 160px;
  background-color: #181818;
  border-radius: 8px;
  padding: 1em;
  text-align: center;
}
.card img {
  width: 100%;
  border-radius: 8px;
  height: 160px;
  object-fit: cover;
}
.stColumn {
  background-color:#000000;
  border-radius:30px;
  padding:1em;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def main():

    # Header Spotify

    st.markdown(
        """
        <div style='background-color: #000000; padding: 1em 1em; display: flex; align-items: center; margin:10px; 
        border-radius:30px;'>
          <img src='https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg'
               style='height: 40px; margin-right: 1em;' />
          <h2 style='margin: 0;'>Recommendation engine</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_menu, col_main = st.columns([2, 8], gap="small")

    # Left Menu

    with col_menu:

        # To make it look good, reproduction of spotify menu

        st.write("")
        st.markdown("<h3 style='color:#1DB954;background-color:#000000;border-radius:30px;'>Menu</h3>", unsafe_allow_html=True)
        st.markdown("""
        <ul style="list-style:none; padding-left:0; line-height:1.8;background-color:#000000;border-radius:30px;">
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

        # Setting the data and put the name and path

        st.subheader("Settings")
        artists_path = st.text_input("Path to artists.dat", "data/artists_gp3.dat")
        user_artists_path = st.text_input("Path to user_artists.dat", "data/user_artists_gp3.dat")

        if st.button("Load and preprocess"):
            try:
                user_artists_scaled, user_artists_top, artist_id_to_name = load_and_transform_data(artists_path, user_artists_path)
                st.session_state["user_artists_scaled"] = user_artists_scaled
                st.session_state["user_artists_top"] = user_artists_top
                st.session_state["artist_id_to_name"] = artist_id_to_name
                st.session_state["all_users"] = list(user_artists_scaled.index)
                st.session_state["user_to_idx"] = {u: i for i, u in enumerate(st.session_state["all_users"])}
                st.success("Data load and preprocess successfully !")
                st.write("Dimension DataFrame :", user_artists_scaled.shape)
            except Exception as e:
                st.error(f"Error : {e}")

        # Settings of the engines

        if "user_artists_scaled" in st.session_state:
            st.subheader("Recommendations ")
            k_neighbors = st.slider("Number of neighbours (k)", 1, 50, 10)
            n_items = st.slider("Number of recommended artist", 1, 20, 5)
            st.subheader("Evaluation")
            given = st.slider("Hidden Artists (given)", 1, 20, 5)
            sample_users = st.slider("Users Sample", 10, 300, 100)

        # Right column display all recommendation

    with col_main:
        st.subheader("Recommendation (unmasked)")
        if "user_artists_scaled" in st.session_state:
            all_users = st.session_state["all_users"]
            if all_users:
                selected_user = st.selectbox("Choose an user :", all_users)
            else:
                st.warning("No available user.")
                return

            # Launch the recommendation engine

            if st.button("Show recommendations"):
                st.markdown("### Popularity (filtered)")
                pop_list = popularity_recommender_filtered(
                    st.session_state["user_artists_top"],
                    st.session_state["user_artists_scaled"],
                    selected_user,
                    n=n_items
                )
                pop_cards_html = "<div class='horizontal-scroller'>"

                # Display of the recommendation on card with our POPULARITY model, and link with the api of Spotify for
                # display pictures

                for artist_id in pop_list:
                    name = st.session_state["artist_id_to_name"].get(artist_id, "Unknown artist")
                    artist_img = get_spotify_artist_image(name)
                    pop_cards_html += (
                        "<div class='card'>"
                        f"<img src='{artist_img}' />"
                        f"<p>{artist_id}<br><strong>{name}</strong></p>"
                        "</div>"
                    )
                pop_cards_html += "</div>"
                st.markdown(pop_cards_html, unsafe_allow_html=True)

                st.markdown("### UBCF (classic)")
                ubcf_list = ubcf_recommend_for_display(
                    st.session_state["user_artists_scaled"],
                    st.session_state["user_to_idx"],
                    selected_user,
                    k=k_neighbors,
                    n=n_items
                )

                # Display of the recommendation on card with our UBCF model, and link with the api of Spotify for
                # display pictures

                ubcf_cards_html = "<div class='horizontal-scroller'>"
                for artist_id in ubcf_list:
                    name = st.session_state["artist_id_to_name"].get(artist_id, "Unknown artist")
                    artist_img = get_spotify_artist_image(name)
                    ubcf_cards_html += (
                        "<div class='card'>"
                        f"<img src='{artist_img}' />"
                        f"<p>{artist_id}<br><strong>{name}</strong></p>"
                        "</div>"
                    )
                ubcf_cards_html += "</div>"
                st.markdown(ubcf_cards_html, unsafe_allow_html=True)

            # Evaluation of our 3 models (POPULARITY / RANDOM / UBCF

            if st.button("Evaluating models"):
                prec_ubcf, recall_ubcf = evaluate_recommender_topN_ubcf(
                    user_artists_scaled=st.session_state["user_artists_scaled"],
                    n=n_items,
                    given=given,
                    sample_users=sample_users,
                    k=k_neighbors
                )
                prec_pop, recall_pop = evaluate_recommender_topN_pop(
                    user_artists_top=st.session_state["user_artists_top"],
                    user_artists_scaled=st.session_state["user_artists_scaled"],
                    n=n_items,
                    given=given,
                    sample_users=sample_users
                )
                prec_rand, recall_rand = evaluate_recommender_topN_random(
                    user_artists_scaled=st.session_state["user_artists_scaled"],
                    n=n_items,
                    given=given,
                    sample_users=sample_users
                )
                st.markdown("### Models evaluation")
                st.write(f"**UBCF** - Précision : {prec_ubcf:.3f} | Recall : {recall_ubcf:.3f}")
                st.write(f"**Popularité** - Précision : {prec_pop:.3f} | Recall : {recall_pop:.3f}")
                st.write(f"**Aléatoire** - Précision : {prec_rand:.3f} | Recall : {recall_rand:.3f}")

            if st.button('"Mega" Models evaluation (10 iterations)'):
                # Run 10 evaluations for each algorithm
                ubcf_list_vals, pop_list_vals, rand_list_vals = mega_evaluation(
                    st.session_state["user_artists_scaled"],
                    st.session_state["user_artists_top"],
                    n=n_items,
                    given=given,
                    sample_users=sample_users,
                    k=k_neighbors,
                    iterations=10
                )
                # Prepare data for graphing
                iterations = list(range(1, 11))
                data = pd.DataFrame({
                    "Iteration": iterations,
                    "UBCF": ubcf_list_vals,
                    "Popularity": pop_list_vals,
                    "Random": rand_list_vals
                })
                # Creating a graph with Altair
                chart = alt.Chart(data.melt('Iteration', var_name='Model', value_name='Accuracy')).mark_line(point=True).encode(
                    x="Iteration:O",
                    y="Accuracy :Q",
                    color="Model:N"
                ).properties(
                    title="evolution of accuracy (10 iterations)"
                )
                st.altair_chart(chart, use_container_width=True)

    st.markdown("""
    <div style='position:fixed; left:0; bottom:0; width:100%; background-color:#181818; 
                padding:0.7em; display:flex; align-items:center; justify-content:center; z-index:9999;'>
      <div style='flex:1; margin-left:1em; color:#1DB954; font-weight:bold;'>
        <button style='background:none; border:none; color:#1DB954; margin-right:0.5em;'>⏮️</button>
        <button style='background:none; border:none; color:#1DB954; margin-right:0.5em;'>⏯️</button>
        <button style='background:none; border:none; color:#1DB954;'>⏭️</button>
      </div>
      <div style='flex:1; text-align:center; color:#1DB954;'>
        Powered by RECOMIND Solutions
      </div>
      <div style='flex:1;'></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
