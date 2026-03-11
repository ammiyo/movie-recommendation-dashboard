import pandas as pd

def main():
    print("Loading datasets")
    try:
        movies_df = pd.read_csv("dataset/movies.csv")
        ratings_df = pd.read_csv("dataset/ratings.csv")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the dataset files exist in the 'dataset/' directory.")
        return

    # -------------------------------------------------------
    # Clean movies dataset
    # Expected columns: movie_id, title, genres, release_year
    # -------------------------------------------------------
    print("Cleaning movies")

    # Remove duplicate rows
    movies_df = movies_df.drop_duplicates()

    # Remove rows where movie_id or title is missing
    movies_df = movies_df.dropna(subset=["movie_id", "title"])

    # Convert movie_id to integer
    movies_df["movie_id"] = movies_df["movie_id"].astype(int)

    # Convert release_year to integer (skip NaN rows gracefully using Int64)
    movies_df["release_year"] = pd.to_numeric(movies_df["release_year"], errors="coerce").astype("Int64")

    # Strip whitespace from title
    movies_df["title"] = movies_df["title"].str.strip()

    # -------------------------------------------------------
    # Clean ratings dataset
    # Expected columns: user_id, movie_id, rating, timestamp
    # -------------------------------------------------------
    print("Cleaning ratings")

    # Remove duplicates
    ratings_df = ratings_df.drop_duplicates()

    # Remove rows with missing movie_id or rating
    ratings_df = ratings_df.dropna(subset=["movie_id", "rating"])

    # Ensure correct data types
    ratings_df["user_id"] = ratings_df["user_id"].astype(int)
    ratings_df["movie_id"] = ratings_df["movie_id"].astype(int)
    ratings_df["rating"] = ratings_df["rating"].astype(float)
    ratings_df["timestamp"] = ratings_df["timestamp"].astype(int)

    # -------------------------------------------------------
    # Print dataset statistics
    # -------------------------------------------------------
    total_movies = len(movies_df)
    total_ratings = len(ratings_df)
    unique_users = ratings_df["user_id"].nunique()
    average_rating = ratings_df["rating"].mean()

    print(f"\n--- Dataset Statistics ---")
    print(f"Total movies:   {total_movies}")
    print(f"Total ratings:  {total_ratings}")
    print(f"Unique users:   {unique_users}")
    print(f"Average rating: {average_rating:.2f}")
    print(f"--------------------------\n")

    # -------------------------------------------------------
    # Save cleaned datasets
    # -------------------------------------------------------
    print("Saving cleaned datasets")
    movies_df.to_csv("dataset/clean_movies.csv", index=False)
    ratings_df.to_csv("dataset/clean_ratings.csv", index=False)

    print("Cleaning completed")

if __name__ == "__main__":
    main()
