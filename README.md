# Movie Rating Analytics Dashboard

The Movie Rating Analytics Dashboard is a comprehensive web-based platform designed to analyze and visualize the MovieLens 100K dataset. This project processes large-scale movie rating data to extract meaningful patterns in user behavior, genre popularity, and cinematic trends. By leveraging a modern data stack, it provides an interactive experience for exploring movie insights through professional-grade visualizations and real-time metric tracking.

## Features

*   **Interactive Analytics Dashboard:** Real-time data visualization of movie trends.
*   **8 Specialized Visualizations:** Custom Chart.js implementations for diverse data perspectives.
*   **KPI Overview Metrics:** Quick-glance cards for total movies, ratings, users, and average score.
*   **Movie Search Quick Insights:** Dynamic search panel providing deep-dives into specific movie performance.
*   **Genre Popularity Analysis:** Distribution of ratings and engagement across different genres.
*   **Rating Distribution Visualization:** Statistical breakdown of how users are scoring content.
*   **User Activity Insights:** Tracking the most engaged contributors in the dataset.
*   **Temporal Analysis:** Visualization of movie release volume and rating frequency over time.
*   **Dark Cinema Theme:** A high-contrast, professional UI designed for data clarity and aesthetic appeal.

## Dashboard Preview

![Dashboard Screenshot](./assets/dashboard.png)

*The screenshot demonstrates the analytics dashboard with integrated Chart.js visualizations and dynamic KPI overview cards.*

## Project Architecture

The application follows a modular data processing and presentation pipeline:

1.  **Data Layer:** Raw MovieLens 100K dataset is processed via high-performance cleaning scripts.
2.  **Storage Layer:** Cleaned data is structured and loaded into a MySQL database for efficient querying.
3.  **Analytics Layer:** A Python-based analytics engine performs complex aggregations and statistical calculations using Pandas.
4.  **API Layer:** A Flask-based REST API manages data transmission between the backend engine and the interface.
5.  **Presentation Layer:** A responsive web interface built with Bootstrap and Chart.js renders data into an interactive dashboard.

## Project Structure

```text
movie/
├── analytics/
│   ├── analytics_engine.py      # Core logic for data aggregation
│   └── data_cleaning.py         # Scripts for filtering and normalizing raw data
├── database/
│   ├── fast_loader.py           # Optimized MySQL data insertion
│   └── load_data.py             # Standard database initialization
├── dataset/
│   ├── clean_movies.csv         # Processed movie metadata
│   └── clean_ratings.csv        # Processed user rating data
├── static/
│   ├── css/                     # Custom cinema-themed styling
│   ├── js/                      # Chart.js logic and API handling
│   └── images/                  # Assets for UI components
├── templates/
│   └── dashboard.html           # Main dashboard interface
└── app.py                       # Flask application entry point
```

## Dashboard Visualizations

The dashboard includes the following analytical charts:

*   **Top Rated Movies:** Highlights the highest-quality content by average score.
*   **Most Rated Movies:** Visualizes the most popular titles by total engagement volume.
*   **Genre Popularity:** A proportional breakdown of genre representation.
*   **Rating Distribution:** Shows the frequency of scores from 1 to 5.
*   **Ratings Over Time:** Tracks the growth and trends of user feedback.
*   **Top Users:** identifies the most prolific reviewers in the system.
*   **Average Rating by Genre:** Compares the perceived quality across different categories.
*   **Movies Released Per Year:** Illustrates historical cinema production trends.

## Installation & Setup

Follow these steps to deploy the project locally:

1.  **Clone the repository**
    ```bash
    git clone <repo-link>
    ```

2.  **Install dependencies**
    ```bash
    pip install flask pandas matplotlib seaborn mysql-connector-python
    ```

3.  **Initialize MySQL**
    *   Start MySQL using XAMPP or your preferred local server.
    *   Create a new database named `movie_analytics`.

4.  **Prepare and Load Data**
    *   Run the cleaning script:
        ```bash
        python analytics/data_cleaning.py
        ```
    *   Load the data into the database:
        ```bash
        python database/fast_loader.py
        ```

5.  **Start the Flask Server**
    ```bash
    python app.py
    ```

6.  **Access the Dashboard**
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Dataset

This project utilizes the **MovieLens 100K Dataset** provided by GroupLens Research. The data consists of 100,000 ratings from 943 users on 1,682 movies.

Source: [GroupLens MovieLens Dataset](https://grouplens.org/datasets/movielens/100k/)

## Future Improvements

*   **Recommendation System:** Implementation of collaborative and content-based filtering algorithms.
*   **Advanced Filtering:** Multi-dimensional sorting and filtering by popularity, date, or specific demographics.
*   **Movie Poster Integration:** Connection to external APIs (e.g., TMDB) to fetch and display movie artwork.
*   **Real-time Analytics:** WebSocket integration for live data updates and streaming analytics.

## Author

**Pratham Debnath**
MCA Student
Data Analytics / Cybersecurity Enthusiast

