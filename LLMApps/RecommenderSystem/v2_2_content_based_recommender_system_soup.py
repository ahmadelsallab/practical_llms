import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import streamlit as st
import json
# Function to convert all strings to lower case and strip names of spaces
def normalize_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
        
# Function to parse the stringified features into their corresponding python objects

# Function to create a 'soup' of features
def create_soup(features):
    return ' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) + ' ' + features['director'] + ' ' + ' '.join(features['genres'])

# Function to calculate movie features
def calculate_movie_features(metadata):
    '''
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(metadata['soup'])
    return count_matrix, count
    '''
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(metadata['soup'])
    return tfidf_matrix, tfidf

# Function to calculate user profile features
def calculate_user_features(watched_movies, metadata, count):
    watched_soups = [metadata.loc[metadata['title'] == movie, 'soup'].iloc[0] for movie in watched_movies if movie in metadata['title'].values]
    watched_soups_str = " ".join(watched_soups)
    user_profile = count.transform([watched_soups_str])
    return user_profile

# Function to get recommendations
def get_recommendations(user_profile, metadata, count_matrix):
    cosine_sim = cosine_similarity(user_profile, count_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores[1:6]]  # Top 5 movies
    return metadata['title'].iloc[movie_indices]

# Get the director's name from the crew feature. If director is not listed, return NaN
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Returns the list top 3 elements or entire list; whichever is more.
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []
def clean_data():
    # Load Movies Metadata
    metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')
    # Load keywords and credits
    credits = pd.read_csv('.\imdb.data\credits.csv')
    keywords = pd.read_csv('.\imdb.data\keywords.csv')

    # Remove rows with bad IDs.
    metadata = metadata.drop([19730, 29503, 35587])

    # Convert IDs to int. Required for merging
    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')
    metadata['id'] = metadata['id'].astype('int')

    # Merge keywords and credits into your main metadata dataframe
    metadata = metadata.merge(credits, on='id')
    metadata = metadata.merge(keywords, on='id')
    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(literal_eval)
        
    features = ['cast', 'keywords', 'genres']
    for feature in features:
        metadata[feature] = metadata[feature].apply(get_list)
    
    # Define new director, cast, genres and keywords features that are in a suitable form.
    metadata['director'] = metadata['crew'].apply(get_director)
        


    # Apply clean_data function to your features.
    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        metadata[feature] = metadata[feature].apply(normalize_data)    
    return metadata

def main():
    st.title("Content-Based Movie Recommender System with Additional Features")
    if 'feature_matrix' not in st.session_state:
        with st.spinner("Cleaning data..."):
            metadata = clean_data()   
            st.write("Sample Data:")
            st.write(metadata[['title', 'cast', 'director', 'keywords', 'genres']].head(10)) 

        with st.spinner("Calculating movie features..."):    
            # Create a 'soup' of features and calculate movie features
            metadata['soup'] = metadata.apply(create_soup, axis=1)
            feature_matrix, transform = calculate_movie_features(metadata)
            st.session_state.feature_matrix = feature_matrix
            st.session_state.transform = transform
            st.session_state.metadata = metadata
    else:
        feature_matrix = st.session_state.feature_matrix
        transform = st.session_state.transform
        metadata = st.session_state.metadata
        st.write("Sample Data:")
        st.write(metadata[['title', 'cast', 'director', 'keywords', 'genres']].head(10)) 

    # User input for watched movies
    user_history_input = st.text_area("Enter watched movies as a JSON list:", '["The Dark Knight", "Inception"]')
    watched_movies = json.loads(user_history_input)

    # Calculate user profile and get recommendations
    if st.button("Get Recommendations"):
        with st.spinner("Calculating recommendations..."):
            user_profile = calculate_user_features(watched_movies, metadata, transform)
            recommendations = get_recommendations(user_profile, metadata, feature_matrix)
            st.write("Recommended Movies:")
            st.write(recommendations)

if __name__ == "__main__":
    main()
