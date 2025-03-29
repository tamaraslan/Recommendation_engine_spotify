# spotify_styled_display.py

import streamlit as st
import streamlit.components.v1 as components


def display_spotify_styled_recommendation(
        block_title: str,
        artist_name: str,
        cover_url: str,
        sub_info: str,
        track_list: list,
        block_height: int = 100
):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" crossorigin="anonymous" />
        <style>
            .recommendation-container {{
                background: linear-gradient(to bottom, #282828, #181818);
                border-radius: 8px;
                padding: 1em;
                color: white;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            }}

            .recommendation-header h4 {{
                color: #fff;
                margin: 0 0 0.8em 0;
                font-size: 1.2em;
            }}

            .recommendation-content {{
                display: grid;
                grid-template-columns: 200px 1fr;
                gap: 1.5em;
            }}

            @media (max-width: 768px) {{
                .recommendation-content {{
                    grid-template-columns: 1fr;
                }}
            }}

            .artist-info {{
                text-align: center;
            }}

            .artist-image-container {{
                position: relative;
                width: 100%;
                max-width: 180px;
                margin: 0 auto;
            }}

            .artist-image-container img {{
                width: 100%;
                aspect-ratio: 1;
                object-fit: cover;
                border-radius: 4px;
                transition: filter 0.3s ease;
            }}

            .play-overlay {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: #1DB954;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: all 0.3s ease;
            }}

            .artist-image-container:hover img {{
                filter: brightness(0.7);
            }}

            .artist-image-container:hover .play-overlay {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1.1);
            }}

            .artist-info h3 {{
                margin: 0.5em 0;
                color: white;
                font-size: 1.2em;
            }}

            .sub-info {{
                color: #b3b3b3;
                font-size: 0.8em;
            }}

            .tracks-container h4 {{
                color: white;
                margin-bottom: 0.8em;
                font-size: 1em;
            }}

            .tracks-list {{
                display: flex;
                flex-direction: column;
                gap: 0.3em;
            }}

            .track-item {{
                display: grid;
                grid-template-columns: 25px 1fr auto;
                align-items: center;
                padding: 0.4em;
                border-radius: 4px;
                transition: background-color 0.2s ease;
            }}

            .track-item:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}

            .track-number {{
                color: #b3b3b3;
                font-size: 0.8em;
            }}

            .track-info {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 1em;
                padding: 0 0.8em;
            }}

            .track-name {{
                color: white;
                font-size: 0.9em;
                font-weight: 500;
            }}

            .track-duration {{
                color: #b3b3b3;
                font-size: 0.8em;
            }}

            .track-actions {{
                display: flex;
                gap: 0.4em;
                opacity: 0;
                transition: opacity 0.2s ease;
            }}

            .track-item:hover .track-actions {{
                opacity: 1;
            }}

            .track-actions button {{
                background: none;
                border: none;
                color: #b3b3b3;
                cursor: pointer;
                padding: 0.4em;
                transition: all 0.2s ease;
                font-size: 0.8em;
            }}

            .track-actions button:hover {{
                color: white;
                transform: scale(1.1);
            }}
        </style>
    </head>
        <div class="recommendation-container">
            <div class="recommendation-header">
                <h4>{block_title}</h4>
            </div>

            <div class="recommendation-content">
                <div class="artist-info">
                    <div class="artist-image-container">
                        <img src="{cover_url}" alt="{artist_name}" />
                        <div class="play-overlay">
                            <i class="fas fa-play"></i>
                        </div>
                    </div>
                    <h3>{artist_name}</h3>
                    <p class="sub-info">
                        <i class="fas fa-video"></i>
                        {sub_info}
                    </p>
                </div>

                <div class="tracks-container">
                    <h4>Popular Tracks</h4>
                    <div class="tracks-list">
    """

    for idx, (track_name, duration) in enumerate(track_list, 1):
        html += f"""
                        <div class="track-item">
                            <div class="track-number">{idx}</div>
                            <div class="track-info">
                                <div class="track-name">{track_name}</div>
                                <div class="track-duration">{duration}</div>
                            </div>
                            <div class="track-actions">
                                <button class="track-like">
                                    <i class="far fa-heart"></i>
                                </button>
                                <button class="track-more">
                                    <i class="fas fa-ellipsis"></i>
                                </button>
                            </div>
                        </div>
        """

    html += """
                    </div>
                </div>
            </div>
        </div>
    </html>
    """

    components.html(html, height=block_height, scrolling=True)