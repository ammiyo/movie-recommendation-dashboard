def test_dashboard_stats_endpoint(client):
    response = client.get("/api/dashboard-stats")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["total_movies"] > 0
    assert payload["total_ratings"] > 0
    assert payload["total_users"] > 0
    assert "avg_rating" in payload


def test_movie_insight_requires_title(client):
    response = client.get("/api/movie-insight")
    assert response.status_code == 400
    assert "title" in response.get_json()["error"].lower()


def test_movie_insight_not_found(client):
    response = client.get("/api/movie-insight?title=zzznomatchtitlexyz")
    assert response.status_code == 404


def test_movie_detail_not_found(client):
    response = client.get("/api/movie-detail/999999")
    assert response.status_code == 404
