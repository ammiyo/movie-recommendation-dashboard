import pandas as pd
import os

def main():
    print("Loading u.data")
    
    # 1. Convert u.data to ratings.csv
    try:
        ratings_df = pd.read_csv(
            "dataset/u.data",
            sep="\t",
            names=["user_id", "movie_id", "rating", "timestamp"]
        )
    except FileNotFoundError:
        print("Error: dataset/u.data not found. Please ensure it exists.")
        return
        
    print("Converting ratings dataset")
    ratings_df.to_csv("dataset/ratings.csv", index=False)
    
    print("Loading u.item")
    
    # 2. Convert u.item to movies.csv
    # Define columns for u.item
    genre_columns = [
        "unknown", "Action", "Adventure", "Animation", "Children", "Comedy", 
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", 
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]
    
    item_columns = [
        "movie_id", "movie_title", "release_date", "video_release_date", "IMDb_URL"
    ] + genre_columns
    
    try:
        movies_df = pd.read_csv(
            "dataset/u.item",
            sep="|",
            encoding="latin-1",
            names=item_columns
        )
    except FileNotFoundError:
        print("Error: dataset/u.item not found. Please ensure it exists.")
        return
        
    print("Processing movie genres")
    
    # Extract release year from release_date
    movies_df["release_year"] = pd.to_datetime(movies_df["release_date"]).dt.year
    # Convert from float to Int (since some might be NaN leading to float type)
    movies_df["release_year"] = movies_df["release_year"].astype("Int64")
    
    # Combine the genre columns into a single genres column using "|"
    def get_genres(row):
        active_genres = [genre for genre in genre_columns if row[genre] == 1]
        if not active_genres:
            return "unknown" 
        return "|".join(active_genres)
        
    movies_df["genres"] = movies_df.apply(get_genres, axis=1)
    
    # Rename movie_title to title to match the output specification
    movies_df = movies_df.rename(columns={"movie_title": "title"})
    
    # Final movies.csv columns
    final_movies_df = movies_df[["movie_id", "title", "genres", "release_year"]]
    
    print("Saving movies.csv")
    final_movies_df.to_csv("dataset/movies.csv", index=False)
    
    print("Conversion completed")

if __name__ == "__main__":
    main()
