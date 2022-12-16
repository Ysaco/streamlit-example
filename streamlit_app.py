from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
from datetime import date

"""
# Welcome to SteamReco!

SteamReco is a game recommendation system based of steam games for our fellow gamers! :video_game:

This app uses a database based on a webscraping on the steam webpage, it does not use SteamKit or any external tool, just BeautifulSoup and a bit of patience.



"""

#For more info, insight, or further development on this web app, you can contact me at "ysaco7@gmail.com"
game_list = pd.read_excel('all_data.xlsx')

vectorizer_train = TfidfVectorizer(analyzer = 'word', min_df=0.0, max_df = 1.0, strip_accents = None,
                                       encoding = 'utf-8', preprocessor=None)
vector_matrix = vectorizer_train.fit_transform(game_list['genre'])

cos_matrix = linear_kernel(vector_matrix[21022],vector_matrix[21022])

def get_title_from_index(index):
    return game_list[game_list.index == index]['title'].values[0]

def get_index_from_title(title):
    return game_list[game_list.title == title].index.values[0]

def get_picture_from_index(index):
    return game_list[game_list.index == index]['photo'].values[0]

def matching_score(a,b):
    return fuzz.ratio(a,b)

def find_closest_title(title):
    leven_scores = list(enumerate(game_list['title'].apply(matching_score, b=title)))
    sorted_leven_scores = sorted(leven_scores, key=lambda x: x[1], reverse=True)
    closest_title = get_title_from_index(sorted_leven_scores[0][0])
    distance_score = sorted_leven_scores[0][1]
    
    return closest_title, distance_score


def contents_recommender(insert_game, quantity):
    
    closest_title, distance_score = find_closest_title(insert_game)

    if distance_score == 100:
        
        name = []
        photo = []
        game_index = get_index_from_title(closest_title)
        game_list = list(enumerate(cos_matrix[int(game_index)]))
        similar_games = list(filter(lambda x:x[0] != int(game_index), sorted(game_list,key=lambda x:x[1], reverse=True)))

        print('List of games similar to '+'\033[1m'+str(closest_title)+'\033[0m'+':'+'\n')

        for i in similar_games[:quantity]:
            name.append(str(get_title_from_index(i[0]))+' '+str(math.trunc(i[1]*100))+'%')
            photo.append(str(get_picture_from_index(i[0])))

        return name, photo

    else:

        print('Did you mean '+'\033[1m'+str(closest_title)+'\033[0m'+'?','\n')

        name = []
        photo = []
        game_index = get_index_from_title(closest_title)
        game_list = list(enumerate(cos_matrix[int(game_index)]))
        similar_games = list(filter(lambda x:x[0] != int(game_index), sorted(game_list,key=lambda x:x[1], reverse=True)))

        print('List of games similar to '+'\033[1m'+str(closest_title)+'\033[0m'+':'+'\n')

        for i in similar_games[:quantity]:
            name.append(str(get_title_from_index(i[0]))+' '+str(math.trunc(i[1]*100))+'%')
            photo.append(str(get_picture_from_index(i[0])))
    
        return name, photo
            
insert_game = st.text_input("Insert a game you like")

quantity = st.slider("Quantity of games you would like to see", 10, 4500, 100)

if st.button('Recommend'): 
    closest_title, distance_score = find_closest_title(insert_game)
    name, photo = contents_recommender(insert_game, quantity)
    if distance_score == 100:
        st.text('List of games similar to '+str(closest_title))

        st.text(' ')
        for i in range(len(name)):
            st.text(name[i])
            st.image(photo[i])

    else:
        st.text(str('Did you mean '+str(closest_title)+'?'))
        st.text(str('List of games similar to '+str(closest_title)+':'))
        st.text(' ')
        for i in range(len(name)):
            st.text(name[i])
            st.image(photo[i])