# spotify_styled_display.py

import streamlit as st
import streamlit.components.v1 as components

def display_spotify_styled_recommendation(
    block_title: str,
    artist_name: str,
    cover_url: str,
    sub_info: str,
    track_list: list,
    block_height: int = 400
):
    """
    Displays a Spotify-like block with:
      - A left column (title, cover, sub-info)
      - A right column ("Titres" listing)
    Renders via st.components.v1.html(...) to avoid raw HTML issues.

    We create a minimal HTML document with <html><head>...</head><body>...</body></html>
    so that Font Awesome is properly recognized, but we remove the integrity attribute
    to avoid the digest mismatch error.
    """

    # 1) Minimal HTML Document with Font Awesome (no integrity attribute)
    html_head = """
    <html>
    <head>
      <meta charset="UTF-8">
      <link rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            crossorigin="anonymous"
            referrerpolicy="no-referrer"
      />
      <style>
        body {
          margin: 0;
          padding: 0;
          background-color: #121212;
          font-family: Arial, sans-serif;
        }
      </style>
    </head>
    <body>
    """

    # 2) Main content
    html_body = (
        "<div style='display: flex; gap: 30px; margin: 10px;'>"

          f"<div style='flex: 1;'>"
            f"<h4 style='color: #fff; margin-bottom: 10px;'>{block_title}</h4>"
            "<div style='background-color: #181818; border-radius: 8px; padding: 20px;'>"
              f"<img src='{cover_url}' style='width: 15%; border-radius: 8px;' />"
              f"<h3 style='color: #fff; margin: 10px 0;'>{artist_name}</h3>"
              "<p style='color: #bbb; margin: 0;'>"
                "<i class='fa-solid fa-video' style='color: #1DB954;'></i>"
                f"&nbsp;{sub_info}"
              "</p>"
            "</div>"
          "</div>"

          "<div style='flex: 2;'>"
            "<h4 style='color: #fff; margin-bottom: 10px;'>Titres</h4>"
            "<div style='background-color: #181818; border-radius: 8px; padding: 20px;'>"
    )

    # 3) Track list
    for (t_name, t_duration) in track_list:
        html_body += (
            "<div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;'>"
              "<div style='color: #fff;'>"
                "<i class='fa-solid fa-compact-disc' style='color: #1DB954; margin-right: 8px;'></i>"
                f"{t_name}"
              "</div>"
              f"<div style='color: #999;'>{t_duration}</div>"
            "</div>"
        )

    # 4) Close containers
    html_body += (
            "</div>"  # end 'Titres'
          "</div>"    # end right column
        "</div>"      # end main container
    )

    # 5) End HTML
    html_tail = """
    </body>
    </html>
    """

    full_html = html_head + html_body + html_tail

    # 6) Render with components.html
    components.html(full_html, height=block_height, scrolling=True)
