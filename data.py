import pickle
import pandas as pd

with open('songs_with_features.pkl', 'rb') as input_file:
    songs_with_features = pickle.load(input_file)   

selected_songs19 = songs_with_features.head(15).sort_values(by='zero_nineteen',ascending=True)
selected_songs99 = songs_with_features[songs_with_features['ninety_nine'] > 0]
selected_songs99 = selected_songs99.head(15).sort_values(by='ninety_nine',ascending=True)


feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence']