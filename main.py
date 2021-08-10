import streamlit as st
import pickle
import pandas as pd
import requests

movie_dict = pickle.load(open('data/df.pkl', 'rb'))
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

movie_df = pd.DataFrame(movie_dict)

def parseImage(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    recommended_movies_list = []
    movie_image_url = []
    i = movie_df[movie_df['title'] == movie].index[0]
    distances = similarity[i]

    similar = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    similar_movies = similar[1: 7]
    for i in similar_movies:
        movie_image_url.append(parseImage(movie_df.iloc[i[0]].id))
        recommended_movies_list.append(movie_df.iloc[i[0]].title)

    return recommended_movies_list, movie_image_url

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
'Select your favourite movie,',
movie_df.title.values
)

if st.button('Recommend'):
    recommended_movies, movie_image_url = recommend(selected_movie)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.text(recommended_movies[0])
        st.image(movie_image_url[0])

    with col2:
        st.text(recommended_movies[1])
        st.image(movie_image_url[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(movie_image_url[2])

    with col4:
        st.text(recommended_movies[3])
        st.image(movie_image_url[3])

    with col5:
        st.text(recommended_movies[4])
        st.image(movie_image_url[4])

    with col6:
        st.text(recommended_movies[5])
        st.image(movie_image_url[5])