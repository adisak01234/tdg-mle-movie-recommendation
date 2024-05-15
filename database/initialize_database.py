import pandas as pd
import sqlite3
import os

def initialize_database(data_dir, db_path):
    # Connect to SQLite database (will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)

    # Create cursor object
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS movie")
    cursor.execute("DROP TABLE IF EXISTS rating")

    # Create table for movies with unique constraint on movieId
    cursor.execute("""
    CREATE TABLE movie (
        movieId INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        genres TEXT NOT NULL
    )
    """)

    # Create table for ratings with unique constraint on userId and movieId
    cursor.execute("""
    CREATE TABLE rating (
        userId INTEGER,
        movieId INTEGER,
        rating REAL,
        timestamp INTEGER,
        PRIMARY KEY (userId, movieId)
    )
    """)

    # Index for quick lookup by movieId on movie table
    cursor.execute("CREATE INDEX idx_movieId ON movie (movieId)")

    # Index for quick lookup by userId on rating table
    cursor.execute("CREATE INDEX idx_userId ON rating (userId)")

    # Read CSV files
    movies_df = pd.read_csv(os.path.join(data_dir, 'movies.csv'))
    ratings_df = pd.read_csv(os.path.join(data_dir, 'ratings.csv')).query("0.5<=rating<=5")

    # Remove rows with NaN values in the userId column and convert types
    ratings_df.dropna(subset=['userId'], inplace=True)
    ratings_df['userId'] = ratings_df['userId'].astype(int)
    ratings_df['movieId'] = ratings_df['movieId'].astype(int)

    # Insert data into movie table
    movies_df.to_sql('movie', conn, if_exists='replace', index=False)

    # Insert data into rating table
    ratings_df.to_sql('rating', conn, if_exists='replace', index=False)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Specify the directory containing the initial data and the path for the database
    initial_data_dir = os.path.join(__file__, '../initial_data')
    database_path = os.path.join(__file__, '../movie_rating.db')
    initialize_database(initial_data_dir, database_path)
