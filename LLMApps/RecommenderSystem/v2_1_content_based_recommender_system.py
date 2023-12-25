import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import json

# Function to calculate TF-IDF matrix
def calculate_movies_features(metadata):
    tfidf = TfidfVectorizer(stop_words='english')
    metadata['overview'] = metadata['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(metadata['overview'])
    return tfidf, tfidf_matrix

# Function to calculate user profile features
def calculate_user_features(watched_movies, metadata, tfidf):
    watched_overviews = []
    for movie in watched_movies:
        if movie in metadata['title'].values:
            watched_overviews.append(metadata.loc[metadata['title'] == movie, 'overview'].iloc[0])
    watched_overviews_str = " ".join(watched_overviews)
    print(watched_overviews_str)
    user_profile = tfidf.transform([watched_overviews_str])
    return user_profile

# Function to get recommendations
def get_recommendations(user_profile, metadata, tfidf_matrix, watched_movies):
    cosine_sim = cosine_similarity(user_profile, tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude movies already watched
    movie_indices = [i[0] for i in sim_scores if metadata['title'].iloc[i[0]] not in watched_movies]

    # Get top 5 recommendations
    top_recommendations = metadata['title'].iloc[movie_indices][:5]
    return top_recommendations

def main():
    st.title("Content-Based Movie Recommender System")



    # Calculate movie features
    if 'tfidf_matrix' not in st.session_state:
        with st.spinner("Calculating movie features..."):
            # Load Movies Metadata
            metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')
            tfidf, tfidf_matrix = calculate_movies_features(metadata)
            st.session_state.tfidf = tfidf
            st.session_state.tfidf_matrix = tfidf_matrix
            st.session_state.metadata = metadata
    else:
        tfidf = st.session_state.tfidf
        tfidf_matrix = st.session_state.tfidf_matrix
        metadata = st.session_state.metadata
    st.write("Sample movie features:")
    st.write(metadata[['title', 'overview']].head(10))

    
    user_history_input = st.text_area("Enter watched movies as a JSON list:", '["The Dark Knight", "Inception"]')
    watched_movies = json.loads(user_history_input)

    # Calculate user profile and get recommendations
    if st.button("Get Recommendations"):
        with st.spinner("Calculating recommendations..."):
            user_profile = calculate_user_features(watched_movies, metadata, tfidf)
            recommendations = get_recommendations(user_profile, metadata, tfidf_matrix, watched_movies)
            st.write("Recommended Movies:")
            st.write(recommendations)

if __name__ == "__main__":
    main()
