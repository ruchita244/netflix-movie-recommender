import pandas as pd
import ast
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    movies = pd.read_csv(os.path.join(BASE_DIR, "data/tmdb_5000_movies.csv"))
    credits = pd.read_csv(os.path.join(BASE_DIR, "data/tmdb_5000_credits.csv"))

    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id', 'title', 'overview',
                     'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    def convert(text):
        try:
            return [i['name'] for i in ast.literal_eval(text)]
        except:
            return []

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(lambda x: convert(x)[:3])

    def fetch_director(text):
        try:
            for i in ast.literal_eval(text):
                if i['job'] == 'Director':
                    return [i['name']]
        except:
            return []
        return []

    movies['crew'] = movies['crew'].apply(fetch_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    def collapse(L):
        return [i.replace(" ", "") for i in L]

    for feature in ['genres', 'keywords', 'cast', 'crew']:
        movies[feature] = movies[feature].apply(collapse)

    movies['tags'] = movies['overview'] + movies['genres'] + \
                     movies['keywords'] + movies['cast'] + movies['crew']

    new_df = movies[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return new_df, similarity


def recommend(movie, new_df, similarity):
    index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [new_df.iloc[i[0]].title for i in movies_list]
