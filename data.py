import pickle
import pandas as pd

with open('songs_with_features.pkl', 'rb') as input_file:
    songs_with_features = pickle.load(input_file)   

selected_songs = songs_with_features.head(15).sort_values(by='zero_nineteen',ascending=False)

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence']