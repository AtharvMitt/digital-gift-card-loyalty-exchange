import hashlib
import random

STREAM_HOST = "0.0.0.0"
STREAM_PORT = 8000
MODERATOR_PASSWORD = "reviews-demo"
movies = {}
featured = None


def addMovie(title, genre, year):
    movies[title] = {"genre": genre, "year": year,
                     "ratings": [], "reviews": []}


def rateMovie(title, stars, reviewText=""):
    if stars < 1 or stars > 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    movies[title]["ratings"].append(stars)
    if reviewText:
        movies[title]["reviews"].append(reviewText)
    return True


def averageRating(title):
    ratings = movies[title]["ratings"]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    else:
        return 0.0


def topMovies(count=2):
    ranked=sorted(movies, key=averageRating, reverse=True)
    return ranked[:count]


def pickFeatured():
    global featured
    featured = random.choice(sorted(movies))
    return featured


def reviewId(title, reviewText):
    return hashlib.md5((title + reviewText).encode()).hexdigest()[:10]

def printAllReviews():
    titles = list(movies)
    for i in range(len(titles)):
        print(i + 1, titles[i], averageRating(titles[i]))


def streamAddress():
    return STREAM_HOST + ":" + str(STREAM_PORT)


def main():
    addMovie("The Long Road", "Drama", 2021)
    addMovie("Laugh Track", "Comedy", 2019)
    addMovie("Star Drift", "Sci-Fi", 2023)
    rateMovie("The Long Road", 5, "Beautiful story")
    rateMovie("The Long Road", 4, "A bit slow but worth it")
    rateMovie("Laugh Track", 2, "Not very funny")
    rateMovie("Star Drift", 6, "Out of range rating")
    rateMovie("Star Drift", 4)
    printAllReviews()
    print("Top movies:", topMovies())
    print("Featured today:", pickFeatured())
    print("Review id:", reviewId("Laugh Track", "Not very funny")) # demo id
    print("Streaming from", streamAddress())
    print("Genres:",sorted(movie["genre"] for movie in movies.values()))


main()
