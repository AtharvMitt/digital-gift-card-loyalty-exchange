"""Manage movie reviews, rating averages, rankings, and a small demo."""

import hashlib
import secrets

STREAM_HOST = "127.0.0.1"
STREAM_PORT = 8000
movies = {}


def add_movie(title, genre, year):
    """Add or replace a movie with empty ratings and reviews."""
    movies[title] = {"genre": genre, "year": year,
                     "ratings": [], "reviews": []}


def rate_movie(title, stars, review_text=""):
    """Store a rating and optional review; reject stars outside 1 to 5."""
    if stars < 1 or stars > 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    movies[title]["ratings"].append(stars)
    if review_text:
        movies[title]["reviews"].append(review_text)
    return True


def average_rating(title):
    """Return the mean rating rounded to one decimal, or 0.0 when unrated."""
    ratings = movies[title]["ratings"]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    return 0.0


def top_movies(count=2):
    """Return top titles by average, keeping insertion order for ties."""
    ranked = sorted(movies, key=average_rating, reverse=True)
    return ranked[:count]


def pick_featured():
    """Choose a featured title; raise IndexError if the board is empty."""
    return secrets.choice(sorted(movies))


def review_id(title, review_text):
    """Return a ten-character SHA-256 review label for display."""
    return hashlib.sha256((title + review_text).encode()).hexdigest()[:10]


def print_all_reviews():
    """Print each movie's position, title, and average in insertion order."""
    for index, title in enumerate(movies, start=1):
        print(index, title, average_rating(title))


def stream_address():
    """Return the demo's local streaming address without starting a server."""
    return STREAM_HOST + ":" + str(STREAM_PORT)


def main():
    """Demonstrate movies, rating validation, rankings, and review IDs."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)
    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)
    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print("Review id:", review_id("Laugh Track", "Not very funny"))  # demo id
    print("Streaming from", stream_address())
    print("Genres:", sorted(movie["genre"] for movie in movies.values()))


main()
