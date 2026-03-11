import pandas as pd
import mysql.connector
from mysql.connector import Error

# -------------------------------------------------------
# Database Configuration
# -------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "movie_analytics",
    "port": 3306
}


def get_connection():
    """Return a live MySQL connection (used by Flask API layer)."""
    return mysql.connector.connect(**DB_CONFIG)


# Simple in-process cache so CSVs are only read once per run
_cache = {}


def _load_data():
    """
    Load movies and ratings from cleaned CSVs and return a merged DataFrame.
    CSVs are used directly for speed — avoids repeated DB round-trips.
    The live movies table schema does not have release_year, so it is read
    from clean_movies.csv which has the full column set.
    """
    if _cache:
        return _cache["movies"], _cache["ratings"], _cache["merged"]

    movies_df = pd.read_csv("dataset/clean_movies.csv")
    ratings_df = pd.read_csv("dataset/clean_ratings.csv")

    # Ensure correct types
    movies_df["movie_id"] = movies_df["movie_id"].astype(int)
    ratings_df["movie_id"] = ratings_df["movie_id"].astype(int)
    ratings_df["user_id"] = ratings_df["user_id"].astype(int)
    ratings_df["rating"] = ratings_df["rating"].astype(float)
    ratings_df["timestamp"] = ratings_df["timestamp"].astype(int)

    merged_df = ratings_df.merge(movies_df, on="movie_id", how="left")

    _cache["movies"] = movies_df
    _cache["ratings"] = ratings_df
    _cache["merged"] = merged_df

    return movies_df, ratings_df, merged_df


# -------------------------------------------------------
# Analytics Functions
# -------------------------------------------------------

def get_top_rated_movies(limit=10):
    """
    Return top movies by highest average rating.
    Only includes movies with at least 10 ratings to avoid bias.
    """
    _, _, merged = _load_data()
    result = (
        merged.groupby(["movie_id", "title"])["rating"]
        .agg(avg_rating="mean", count="count")
        .reset_index()
    )
    result = result[result["count"] >= 10]
    result = result.sort_values("avg_rating", ascending=False).head(limit)
    return {
        "labels": result["title"].tolist(),
        "values": result["avg_rating"].round(2).tolist()
    }


def get_most_rated_movies(limit=10):
    """Return movies with the highest number of ratings."""
    _, _, merged = _load_data()
    result = (
        merged.groupby(["movie_id", "title"])["rating"]
        .count()
        .reset_index(name="rating_count")
        .sort_values("rating_count", ascending=False)
        .head(limit)
    )
    return {
        "labels": result["title"].tolist(),
        "values": result["rating_count"].tolist()
    }


def get_genre_popularity():
    """
    Count how many movies belong to each genre.
    Genres column is pipe-separated (e.g., 'Action|Comedy|Drama').
    """
    movies_df, _, _ = _load_data()
    genre_series = movies_df["genres"].dropna().str.split("|").explode()
    genre_counts = genre_series.value_counts()
    return {
        "labels": genre_counts.index.tolist(),
        "values": genre_counts.values.tolist()
    }


def get_rating_distribution():
    """Return the count of ratings for each rating value (1 to 5, including 0.5 steps)."""
    _, ratings_df, _ = _load_data()
    dist = ratings_df["rating"].value_counts().sort_index()
    return {
        "labels": [str(r) for r in dist.index.tolist()],
        "values": dist.values.tolist()
    }


def get_ratings_over_time():
    """Convert timestamp to datetime and group ratings count by year."""
    _, ratings_df, _ = _load_data()
    ratings_df["year"] = pd.to_datetime(ratings_df["timestamp"], unit="s").dt.year
    result = ratings_df.groupby("year").size().reset_index(name="rating_count")
    return {
        "labels": result["year"].tolist(),
        "values": result["rating_count"].tolist()
    }


def get_top_users(limit=10):
    """Find users who rated the most movies."""
    _, ratings_df, _ = _load_data()
    result = (
        ratings_df.groupby("user_id")["movie_id"]
        .count()
        .reset_index(name="rating_count")
        .sort_values("rating_count", ascending=False)
        .head(limit)
    )
    return {
        "labels": [f"User {uid}" for uid in result["user_id"].tolist()],
        "values": result["rating_count"].tolist()
    }


def get_average_rating_by_genre():
    """Compute average rating for each genre."""
    _, _, merged = _load_data()
    # Explode genres so each row represents one movie-genre association
    genre_ratings = merged.copy()
    genre_ratings["genre"] = genre_ratings["genres"].str.split("|")
    genre_ratings = genre_ratings.explode("genre")
    result = (
        genre_ratings.groupby("genre")["rating"]
        .mean()
        .reset_index(name="avg_rating")
        .sort_values("avg_rating", ascending=False)
    )
    return {
        "labels": result["genre"].tolist(),
        "values": result["avg_rating"].round(2).tolist()
    }


def get_movies_per_year():
    """Count number of movies released per year."""
    movies_df, _, _ = _load_data()
    result = (
        movies_df.dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(name="movie_count")
        .sort_values("release_year")
    )
    return {
        "labels": result["release_year"].astype(int).tolist(),
        "values": result["movie_count"].tolist()
    }


def search_movies(title="", year=None, genre=""):
    """
    Search movies by title keyword, release year, and/or genre.
    Returns a list of matching movies with avg rating and rating count.
    """
    _, _, merged = _load_data()

    # Aggregate stats per movie
    stats = (
        merged.groupby(["movie_id", "title", "genres", "release_year"])["rating"]
        .agg(avg_rating="mean", rating_count="count")
        .reset_index()
    )

    result = stats.copy()

    if title:
        result = result[result["title"].str.contains(title, case=False, na=False)]

    if year:
        try:
            result = result[result["release_year"] == int(year)]
        except (ValueError, TypeError):
            pass

    if genre:
        result = result[result["genres"].str.contains(genre, case=False, na=False)]

    result = result.sort_values("avg_rating", ascending=False)

    return {
        "movies": [
            {
                "title": row["title"],
                "genres": row["genres"],
                "release_year": int(row["release_year"]) if pd.notna(row["release_year"]) else None,
                "avg_rating": round(row["avg_rating"], 2),
                "rating_count": int(row["rating_count"]),
            }
            for _, row in result.iterrows()
        ]
    }


def get_dashboard_stats():
    """
    Return dashboard KPI metrics computed from the cached CSV DataFrames.
    Avoids pd.read_sql which requires SQLAlchemy when used with mysql-connector.
    """
    movies_df, ratings_df, _ = _load_data()
    return {
        "total_movies":  int(len(movies_df)),
        "total_ratings": int(len(ratings_df)),
        "avg_rating":    round(float(ratings_df["rating"].mean()), 2),
        "total_users":   int(ratings_df["user_id"].nunique()),
    }


def get_movie_insight(title):
    """
    Return insight for a single best-matching movie by title keyword.
    Returns avg rating, total ratings, genres, and release year.
    """
    _, ratings_df, merged = _load_data()

    # Find best match (case-insensitive, pick highest rating-count)
    mask    = merged["title"].str.contains(title, case=False, na=False)
    matched = merged[mask]

    if matched.empty:
        return None

    # Pick the movie with the most ratings as "best match"
    best_id = matched.groupby("movie_id")["rating"].count().idxmax()
    movie   = matched[matched["movie_id"] == best_id]

    row = movie.iloc[0]
    return {
        "title":         str(row["title"]),
        "avg_rating":    round(float(movie["rating"].mean()), 2),
        "total_ratings": int(len(movie)),
        "genres":        str(row["genres"]),
        "release_year":  int(row["release_year"]) if pd.notna(row["release_year"]) else None,
    }


# -------------------------------------------------------
# Main test block
# -------------------------------------------------------
if __name__ == "__main__":
    import json

    print("\n=== Top Rated Movies ===")
    print(json.dumps(get_top_rated_movies(limit=5), indent=2))

    print("\n=== Most Rated Movies ===")
    print(json.dumps(get_most_rated_movies(limit=5), indent=2))

    print("\n=== Genre Popularity ===")
    print(json.dumps(get_genre_popularity(), indent=2))

    print("\n=== Rating Distribution ===")
    print(json.dumps(get_rating_distribution(), indent=2))

    print("\n=== Ratings Over Time ===")
    print(json.dumps(get_ratings_over_time(), indent=2))

    print("\n=== Top Users ===")
    print(json.dumps(get_top_users(limit=5), indent=2))

    print("\n=== Average Rating by Genre ===")
    print(json.dumps(get_average_rating_by_genre(), indent=2))

    print("\n=== Movies Per Year ===")
    print(json.dumps(get_movies_per_year(), indent=2))
