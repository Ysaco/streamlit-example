from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as mlp
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz
from datetime import date

"""
# Welcome to Steam Reco!

##SteamReco is a game recommendation system based of steam games for our fellow gamers! :video_game:

This app uses a database based on a webscraping on the steam webpage, it does not use SteamKit or any external tool, just BeautifulSoup and a bit of patience.

For more info, insight, or further development on this web app, you can contact me at "ysaco7@gmail.com"

"""
game_list = pd.read_excel('Webscraping_1.csv')



    insert_game = st.text_input("Insert a game you like")
    quantity = st.slider("Quantity of games you would like to see", 1, 4500, 100)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))
with st.echo(code_location='below'):
    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
