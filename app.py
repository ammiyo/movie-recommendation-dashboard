from flask import Flask, jsonify, render_template, request
from analytics.analytics_engine import (
    get_top_rated_movies,
    get_most_rated_movies,
    get_genre_popularity,
    get_rating_distribution,
    get_ratings_over_time,
    get_top_users,
    get_average_rating_by_genre,
    get_movies_per_year,
    search_movies,
    get_dashboard_stats,
    get_movie_insight,
)

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/top-rated")
def top_rated():
    return jsonify(get_top_rated_movies())


@app.route("/api/most-rated")
def most_rated():
    return jsonify(get_most_rated_movies())


@app.route("/api/genre-popularity")
def genre_popularity():
    return jsonify(get_genre_popularity())


@app.route("/api/rating-distribution")
def rating_distribution():
    return jsonify(get_rating_distribution())


@app.route("/api/ratings-over-time")
def ratings_over_time():
    return jsonify(get_ratings_over_time())


@app.route("/api/top-users")
def top_users():
    return jsonify(get_top_users())


@app.route("/api/avg-rating-genre")
def avg_rating_genre():
    return jsonify(get_average_rating_by_genre())


@app.route("/api/movies-per-year")
def movies_per_year():
    return jsonify(get_movies_per_year())


@app.route("/api/search-movies")
def search_movies_route():
    title = request.args.get("title", "").strip()
    year  = request.args.get("year", "").strip()
    genre = request.args.get("genre", "").strip()
    return jsonify(search_movies(title=title, year=year or None, genre=genre))


@app.route("/api/dashboard-stats")
def dashboard_stats():
    try:
        return jsonify(get_dashboard_stats())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/movie-insight")
def movie_insight():
    title = request.args.get("title", "").strip()
    if not title:
        return jsonify({"error": "title parameter required"}), 400
    result = get_movie_insight(title)
    if result is None:
        return jsonify({"error": "No movie found"}), 404
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
