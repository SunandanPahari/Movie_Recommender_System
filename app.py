import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    api_key="YOUR_TMDB_APIKEY"
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    
    response = requests.get(url,timeout=15)
    
    data = response.json()
    
    data_path="https://image.tmdb.org/t/p/w500" + data['poster_path']
    
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    




def recommend(movie):
    movie_index= movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
        
    return recommended_movies ,recommended_movies_poster

st.title("Movie Recommender System")

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.header("Enter the name of the movie below:")

selected_movie=st.selectbox("",movies['title'].values)



if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    
    for i in range(len(names)):
        st.header(names[i])
        st.image(posters[i])


