import pandas as pd
import mysql.connector
from mysql.connector import Error

# -------------------------------------------------------
# Database configuration
# -------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306,
    "database": "movie_analytics"
}

BATCH_SIZE = 1000


def main():
    print("Connecting to database")
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if not connection.is_connected():
            print("Failed to connect to database.")
            return

        cursor = connection.cursor()

        # -------------------------------------------------------
        # Load and insert movies
        # -------------------------------------------------------
        print("Loading movies dataset")
        try:
            movies_df = pd.read_csv("dataset/clean_movies.csv")
        except FileNotFoundError:
            print("Error: dataset/clean_movies.csv not found.")
            return

        # Sanitize: fill any NaNs in text columns
        movies_df["title"] = movies_df["title"].fillna("").str.strip()
        movies_df["genres"] = movies_df["genres"].fillna("")

        # NOTE: The live movies table schema has: movie_id, title, genres
        # release_year is not a column in the current schema, so it is skipped here.
        movies_data = list(
            movies_df[["movie_id", "title", "genres"]].itertuples(index=False, name=None)
        )

        print("Inserting movies")
        movies_query = """
            INSERT IGNORE INTO movies (movie_id, title, genres)
            VALUES (%s, %s, %s)
        """
        # Batch insert movies in chunks to avoid max_allowed_packet limits
        for i in range(0, len(movies_data), BATCH_SIZE):
            batch = movies_data[i : i + BATCH_SIZE]
            cursor.executemany(movies_query, batch)
            connection.commit()

        # -------------------------------------------------------
        # Load and insert ratings
        # -------------------------------------------------------
        print("Loading ratings dataset")
        try:
            ratings_df = pd.read_csv("dataset/clean_ratings.csv")
        except FileNotFoundError:
            print("Error: dataset/clean_ratings.csv not found.")
            return

        ratings_data = list(
            ratings_df[["user_id", "movie_id", "rating", "timestamp"]].itertuples(index=False, name=None)
        )

        ratings_query = """
            INSERT INTO ratings (user_id, movie_id, rating, timestamp)
            VALUES (%s, %s, %s, %s)
        """

        total_batches = (len(ratings_data) + BATCH_SIZE - 1) // BATCH_SIZE
        for i in range(total_batches):
            print(f"Inserting ratings batch {i + 1}")
            batch = ratings_data[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
            cursor.executemany(ratings_query, batch)
            connection.commit()

        print("Import completed successfully")

    except Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
