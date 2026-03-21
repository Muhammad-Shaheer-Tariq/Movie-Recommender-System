import streamlit as st
import pandas as pd
from main import recommend_by_genre

st.set_page_config(page_title="Genre-Based Recommender", layout="centered")

st.title("Genre Based Recommendation using Cosine Similarity")
st.write("Pick a genre and get movie recommendations")

# Load data
movies = pd.read_csv("movies.csv")
movies["genres"] = movies["genres"].apply(lambda x: x.split("|"))

# Get unique genres
all_genres = sorted(set(g for genres in movies["genres"] for g in genres))

selected_genre = st.selectbox("Choose a genre:", all_genres)

if st.button("Recommend"):
    recommendations = recommend_by_genre(selected_genre,10)

    st.subheader(f"Top Movies in {selected_genre}")
    for _, row in recommendations.iterrows():
        st.write(f"**{row['title']}**")
        st.caption("Genres: " + ", ".join(row["genres"]))
