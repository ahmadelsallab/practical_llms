import pandas as pd
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import json
import time


# Function to generate embeddings for movie overviews and create a FAISS vector database
def create_vector_database(metadata, embeddings_model=OpenAIEmbeddings()):
    texts = metadata['title'].tolist()
    vec_db = FAISS.from_texts(texts, embeddings_model)
    return vec_db

# Function to get recommendations based on user's watch history
def get_recommendations(watched_movies, vec_db, metadata, k=5):

    # Get similar movies from their reviews embeddings
    relevant_movies_with_scores = vec_db.similarity_search_with_score(watched_movies, k=k)
    
    # Retrieve movie titles and scores
    recommended_movies = []
    for movie, score in relevant_movies_with_scores:
        recommended_movies.append({'title': movie.page_content, 
                                   'score': score}) 
    # Exclude wathced movies
    recommended_movies = [movie for movie in recommended_movies if movie['title'] not in watched_movies]
            
    recommendations_df = pd.DataFrame(recommended_movies)

    # Rank recommendations by score descendingly
    recommendations_df = recommendations_df.sort_values(by='score', ascending=False)
    
    return recommendations_df

def main():
    st.title("Collaborative Filtering Movie Recommender System with Embeddings and FAISS")

    n_movies = 1000
    # Initialize embeddings model and create a FAISS vector database
    if 'vec_db' not in st.session_state:
        with st.spinner("Loading movie metadata..."):
            # Load Movies Metadata
            metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')
            # Limit for memory purposes
            metadata = metadata[:n_movies]
            st.session_state.metadata = metadata
            

        with st.spinner("Creating vector database for movie embeddings..."):
            embeddings_model = OpenAIEmbeddings()
            start_time = time.time()
            st.session_state.vec_db = create_vector_database(st.session_state.metadata, embeddings_model)
            end_time = time.time()

            time_spent = end_time - start_time
            st.write(f"Time spent to build vector database: {time_spent} seconds for {n_movies} movies")
    
            
    
    st.write("Sample metadata:")
    st.write(st.session_state.metadata[['title', 'overview']].head())

    # User input for watched movies
    user_history_input = st.text_area("Enter your watch history as text:", 'I watched The Dark Knight and Inception recently.')
    

    # Get recommendations based on user's watch history
    if st.button("Get Recommendations"):
        with st.spinner("Finding relevant movies..."):
            start_time = time.time()
            recommended_movies = get_recommendations(user_history_input, 
                                                     st.session_state.vec_db, 
                                                     st.session_state.metadata)
            end_time = time.time()
            time_spent = end_time - start_time
            st.write(f"Time taken to obtain recommendations is {time_spent} seconds")
            st.write("Movies you might like:")
            st.write(recommended_movies[['title', 'score']])

if __name__ == "__main__":
    main()
