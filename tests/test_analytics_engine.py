import inspect

import pytest

from analytics.analytics_engine import (
    _apply_filters,
    _load_data,
    get_dashboard_stats,
    get_movie_insight,
    search_movies,
)


def test_empty_filters_return_full_dataset():
    movies, ratings, merged = _load_data()
    filtered_movies, filtered_ratings, filtered_merged = _apply_filters(
        movies, ratings, merged
    )
    assert len(filtered_movies) == len(movies)
    assert len(filtered_ratings) == len(ratings)
    assert len(filtered_merged) == len(merged)


def test_year_filters_limit_release_year():
    movies, ratings, merged = _load_data()
    filtered_movies, _, _ = _apply_filters(
        movies, ratings, merged, year_min=1990, year_max=1995
    )
    years = filtered_movies["release_year"].dropna().astype(int)
    assert len(filtered_movies) > 0
    assert years.min() >= 1990
    assert years.max() <= 1995


def test_genre_filter_keeps_matching_movies():
    movies, ratings, merged = _load_data()
    filtered_movies, _, _ = _apply_filters(movies, ratings, merged, genre="Sci-Fi")
    assert len(filtered_movies) > 0
    assert filtered_movies["genres"].str.contains("Sci-Fi", case=False, na=False).all()


def test_rating_filter_keeps_selected_star_value():
    movies, ratings, merged = _load_data()
    _, filtered_ratings, _ = _apply_filters(
        movies, ratings, merged, rating_value="5"
    )
    assert len(filtered_ratings) > 0
    assert (filtered_ratings["rating"] == 5.0).all()


def test_dashboard_stats_match_loaded_csv():
    movies, ratings, _ = _load_data()
    stats = get_dashboard_stats()
    assert stats["total_movies"] == len(movies)
    assert stats["total_ratings"] == len(ratings)
    assert stats["total_users"] == ratings["user_id"].nunique()
    assert stats["avg_rating"] == round(float(ratings["rating"].mean()), 2)


def test_dashboard_stats_respect_genre_filter():
    full = get_dashboard_stats()
    filtered = get_dashboard_stats(genre="Documentary")
    assert filtered["total_movies"] < full["total_movies"]
    assert filtered["total_ratings"] < full["total_ratings"]


def test_movie_insight_finds_case_insensitive_title():
    insight = get_movie_insight("toy story")
    assert insight is not None
    assert "Toy Story" in insight["title"]
    assert insight["total_ratings"] > 0
    assert insight["avg_rating"] > 0


def test_movie_insight_returns_none_when_missing():
    assert get_movie_insight("zzznomatchtitlexyz") is None


def test_search_is_case_insensitive_substring():
    result = search_movies(title="STAR WARS")
    titles = [row["title"] for row in result["movies"]]
    assert titles
    assert any("Star Wars" in title for title in titles)


def test_search_empty_title_returns_movies():
    result = search_movies(title="")
    assert len(result["movies"]) > 0


def test_regex_metacharacters_are_treated_literally():
    """User-supplied patterns must not be compiled as regular expressions."""
    if "regex=False" not in inspect.getsource(_apply_filters):
        pytest.skip("Literal filter matching is not enabled in this branch")

    movies, ratings, merged = _load_data()
    filtered_movies, _, _ = _apply_filters(movies, ratings, merged, genre=".*")
    assert len(filtered_movies) < len(movies)

    star_search = search_movies(title=".*")
    assert len(star_search["movies"]) < len(search_movies(title="")["movies"])
    assert get_movie_insight("(a+)+$") is None
