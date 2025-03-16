---

# Spotify Reco System

An advanced music recommendation application developed as part of an academic project. This system uses two main recommendation approaches—Filtered Popularity and User-Based Collaborative Filtering (UBCF)—and includes robust evaluation methods along with an interactive Streamlit dashboard.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Notes](#technical-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Spotify Reco System** is designed to generate personalized artist recommendations using two core approaches:

- **Filtered Popularity:** Recommends the most-listened-to artists overall, excluding those already known by the user.
- **User-Based Collaborative Filtering (UBCF):** Uses cosine similarity to find users with similar listening patterns and aggregates their preferences to generate personalized recommendations.

Additionally, a random baseline is implemented for comparison. The application also features a "Mega Evaluation" tool that runs multiple iterations (10 by default) to assess the robustness of each approach based on precision and recall metrics.

---

## Features

- **Data Loading & Transformation:**  
  Reads and processes two datasets—one containing artist information and another with user listening data—to generate a user-artist matrix that is filtered, pivoted, and normalized.

- **Recommendation Algorithms:**  
  - **Filtered Popularity:** Quickly identifies the top artists not yet listened to by the user.
  - **UBCF:** Provides personalized recommendations based on similar users’ listening behavior.
  - **Random Baseline:** Serves as a benchmark by randomly selecting artists.

- **Dynamic Image Retrieval via Spotify API:**  
  Uses the Spotify API to fetch artist images dynamically.  
  **Important:** You must create a `.env` file with the variables `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` to enable this feature.

- **Evaluation & Visualization:**  
  Evaluate the performance of the models (precision & recall) with standard and "Mega Evaluation" (multiple iterations). Results are visualized using Altair charts.

- **Interactive Dashboard:**  
  The application is built with Streamlit and offers a modern, user-friendly interface inspired by Spotify’s design.

---

## Installation & Setup

### Prerequisites

- **Python 3.7+**
- Required Python libraries:  
  - streamlit  
  - pandas  
  - numpy  
  - scikit-learn  
  - altair  
  - spotipy  
  - python-dotenv

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourUserName/spotify-reco-project.git
   cd spotify-reco-project
   ```

2. **Create a Virtual Environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Configuring Spotify API Credentials

1. **Create a `.env` file** at the root of the project (this file should be included in your `.gitignore`).

2. **Add the following lines** to your `.env` file:

   ```bash
   SPOTIFY_CLIENT_ID=[YOUR API KEY]
   SPOTIFY_CLIENT_SECRET=[YOUR API KEY]
   ```

3. **Ensure `.env` is ignored** by Git by confirming your `.gitignore` includes:

   ```
   .env
   ```

---

## Usage

To run the application, execute:

```bash
streamlit run app.py
```

The dashboard will allow you to:
- Load and preprocess your datasets.
- View personalized recommendations using both Filtered Popularity and UBCF.
- Evaluate model performance (precision & recall) and run a "Mega Evaluation" (10 iterations) to compare models.
- Visualize evaluation metrics using interactive Altair charts.

---

## Project Structure

- **app.py:**  
  The main Streamlit dashboard integrating the UI, recommendation display, and evaluation functions.

- **data_loader.py:**  
  Handles loading, filtering, pivoting, and normalizing the datasets, and constructs a mapping of artist IDs to names.

- **recommenders.py:**  
  Contains the implementation of the recommendation algorithms (Filtered Popularity and UBCF).

- **evaluation.py:**  
  Implements the evaluation metrics (precision and recall) for UBCF, Filtered Popularity, and the Random Baseline. It also provides a "Mega Evaluation" function to run multiple iterations.

- **spotify_images.py:**  
  Retrieves artist images via the Spotify API using Spotipy. It uses a local cache to limit API calls.

- **.env:**  
  A file (not committed to version control) containing sensitive API keys.

- **requirements.txt:**  
  Lists the Python dependencies required for the project.

---

## Technical Notes

- **Environment Variables:**  
  Spotify API credentials are loaded from a `.env` file using `python-dotenv` to ensure sensitive information is not hard-coded.

- **Data Processing:**  
  The data is transformed into a user-artist matrix, and normalization (centering and scaling) is applied to facilitate the calculation of similarities.

- **Algorithm Complexity:**  
  - *Filtered Popularity:* Very efficient (O(n log n) due to sorting).  
  - *UBCF:* More computationally intensive due to similarity calculations, but optimizations (like using sparse matrices) can help manage this complexity.

- **Evaluation:**  
  Multiple evaluation methods (including a random baseline) are implemented to compare performance reliably using precision and recall.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a branch for your feature or bug fix (`git checkout -b feature/your-feature`).
3. Commit your changes with clear commit messages.
4. Push your branch and open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This README summarizes the progress of the project so far and includes all necessary instructions for setup and usage. Feel free to adjust or expand it as the project evolves.
