import sqlite3
import joblib
import os
from config import ROOT_DIR


# Load the trained model once, outside of the function to avoid repeated loading
model = joblib.load(ROOT_DIR / 'model/model.joblib')


def predict_ratings(user_id, movie_ids):
    """
    Predicts ratings for a given user and a list of movie IDs.

    Parameters:
        user_id (int): The ID of the user.
        movie_ids (list): A list of movie IDs.

    Returns:
        list of tuples: Each tuple contains (movie_id, predicted_rating).
    """
    predictions = [(movie_id, model.predict(user_id, movie_id).est) for movie_id in movie_ids]
    sorted_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
    return sorted_predictions


def get_recommendations(user_id, return_metadata):
    # Connect to the SQLite database
    conn = sqlite3.connect(ROOT_DIR / 'database/movie_rating.db')
    cursor = conn.cursor()

    # Get list of all movies
    cursor.execute("SELECT movieId FROM movie")
    all_movies = set(movie[0] for movie in cursor.fetchall())

    # Get list of movies the user has already rated
    cursor.execute("SELECT movieId FROM rating WHERE userId = ?", (user_id,))
    rated_movies = set(movie[0] for movie in cursor.fetchall())

    # Determine movies the user hasn't seen
    unseen_movies = list(all_movies - rated_movies)

    # Use the separate function to predict ratings
    predictions = predict_ratings(user_id, unseen_movies)

    # Sort predictions by estimated rating and get top 2
    top_movies = predictions[:2]

    if return_metadata:
        # Get metadata for top movies
        top_movie_ids = tuple([movie[0] for movie in top_movies])  # Adjusted to handle a dynamic list of IDs
        cursor.execute("SELECT movieId, title, genres FROM movie WHERE movieId IN (?, ?)", top_movie_ids)
        items = [{'id': movie[0], 'title': movie[1], 'genres': movie[2].split('|')} for movie in cursor.fetchall()]
    else:
        # Return only IDs
        items = [{'id': movie[0]} for movie in top_movies]

    # Close database connection
    conn.close()

    return {"items": items}


def get_features(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(ROOT_DIR / 'database/movie_rating.db')
    cursor = conn.cursor()

    # Query for movies the user has rated
    cursor.execute("SELECT movieId FROM rating WHERE userId = ?", (user_id,))
    rated_movies = [movie[0] for movie in cursor.fetchall()]

    # Close database connection
    conn.close()

    # Return the rated movies as features
    return {
        "features": [
            {
                "histories": rated_movies
            }
        ]
    }
