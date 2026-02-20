import requests
import webbrowser

def fetch_movie_details(movie_name):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey=thewdb"
        response = requests.get(url)
        data = response.json()

        poster = data.get("Poster")
        rating = data.get("imdbRating", "N/A")
        overview = data.get("Plot", "No description available.")
        imdb_id = data.get("imdbID")

        trailer_url = None
        if imdb_id:
            trailer_url = f"https://www.youtube.com/results?search_query={movie_name}+trailer"

        if poster and poster != "N/A":
            return poster, rating, overview, trailer_url
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Poster", rating, overview, trailer_url

    except:
        return "https://via.placeholder.com/300x450.png?text=No+Poster", "N/A", "No description available.", None
