import pickle
import pandas as pd

with open('songs_with_features.pkl', 'rb') as input_file:
    songs_with_features = pickle.load(input_file)

with open('songs_bill_melt.pkl', 'rb') as input_file:
    songs_bill_melt = pickle.load(input_file)   

selected_songs19 = songs_with_features.head(15).sort_values(by='zero_nineteen',ascending=True)
selected_songs99 = songs_with_features[songs_with_features['ninety_nine'] > 0]
selected_songs99 = selected_songs99.head(15).sort_values(by='ninety_nine',ascending=True)

feature_list = ['Danceability','Energy','Speachiness','Instrumentalness','Liveness','Valence']

feature_desc = {'Danceability':'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.'
,'Energy':'	Energy is a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.'
,'Speachiness':'Speechiness detects the presence of spoken words in a track. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.'
,'Instrumentalness':'Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'
,'Liveness':'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.'
,'Valence':'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).'
}

features_descriptions = pd.DataFrame.from_dict(feature_desc,orient='index')
features_descriptions = features_descriptions.reset_index()
features_descriptions = features_descriptions.rename(columns={0:'Feature description','index':'Features'})
