
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

#Load Dta
movies = pd.read_csv("movies.csv")

#splites genres into lostssss\
movies["genres"] = movies["genres"].apply(lambda x : x.split("|"))

#encooooooooooooooding

mlb = MultiLabelBinarizer()

genre_matrix = mlb.fit_transform(movies["genres"])

#Compute cosine similiraity

cosine_sim = cosine_similarity(genre_matrix,genre_matrix)

#Map movies title to indices
indices = pd.Series(movies.index, index=movies["title"])

def recommend_movies(title, top_n=5):
    if title not in indices:
        return[]
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #skip the first one same
    sim_scores = sim_scores[1:top_n + 1]

    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices][["title", "genres"]]

def recommend_by_genre(genre, top_n=5):
    #filter movies 
    filtered_movies = movies[movies["genres"].apply(lambda x: genre in x)]

    #sort by number of genres
    filtered_movies = filtered_movies.copy()
    filtered_movies["genre_count"] = filtered_movies["genres"].apply(len)

    filtered_movies = filtered_movies.sort_values(
        by="genre_count" , ascending=False
    )
    return filtered_movies[["title","genres"]].head(top_n)


