import pandas as pd
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import json
import time

# Function to compute the weighted rating of each movie
def weighted_rating(x, M, C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+M) * R) + (M/(M+v) * C)

# Function to get the top-5 movie recommendations
def get_simple_recommendations(metadata):
    C = metadata['vote_average'].mean()
    M = metadata['vote_count'].quantile(0.90)

    q_movies = metadata.copy().loc[metadata['vote_count'] >= M]
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1, args=(M, C))
    q_movies = q_movies.sort_values('score', ascending=False)

    return q_movies[['title', 'vote_count', 'vote_average', 'score']].head(5)


# Function to generate embeddings for movie overviews and create a FAISS vector database
def create_vector_database(metadata, embeddings_model):
    metadata['overview'] = metadata['overview'].fillna('')
    # Here we must add the movie title and and any extra info in the metadata field of the Document.
    # That's why we use from_documents instead of from_texts
    docs = [Document(page_content=overview, metadata=dict(index=i)) for i,overview in enumerate(metadata['overview'])]
    vec_db = FAISS.from_documents(docs, embeddings_model)
    return vec_db

def calculate_user_features(watched_movies, metadata):
    watched_overviews = []
    for movie in watched_movies:
        if movie in metadata['title'].values:
            watched_overviews.append(metadata.loc[metadata['title'] == movie, 'overview'].iloc[0])
    if len(watched_overviews) == 0:        
        return None, False
    else:

        watched_overviews_str = " ".join(watched_overviews)
        return watched_overviews_str, True

# Function to get recommendations based on user's watch history
def get_recommendations(watched_movies, vec_db, metadata, k=5):
    # Transform user's watch history into a single text of movie overviews:
    user_features, status = calculate_user_features(watched_movies, st.session_state.metadata)
    # The movie title the user watched might not be in the metadata, 
    # if this is the case, we fall back to the default recommendations
    if status == False:
        st.write("Cannot find the movie titles entered, falling back to default recommendations")
        return get_simple_recommendations(metadata)    
    
    # Get similar movies from their reviews embeddings
    relevant_movies_with_scores = vec_db.similarity_search_with_score(user_features, k=k)
    
    # Retrieve movie titles and scores
    recommended_movies = []
    for movie, score in relevant_movies_with_scores:
        recommended_movies.append({'title':metadata['title'].iloc[movie.metadata['index']], 
                                'overview': movie.page_content, 
                                'score': score}) 
    # Exclude wathced movies
    recommended_movies = [movie for movie in recommended_movies if movie['title'] not in watched_movies]
            
    recommendations_df = pd.DataFrame(recommended_movies)

    # Rank recommendations by score descendingly
    recommendations_df = recommendations_df.sort_values(by='score', ascending=False)
    
    return recommendations_df

def main():
    st.title("Collaborative Filtering Movie Recommender System with Embeddings and FAISS")


    # Initialize embeddings model and create a FAISS vector database
    if 'vec_db' not in st.session_state:
        n_movies = 10000
        with st.spinner("Loading movie metadata..."):
            # Load Movies Metadata
            metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')
            # Limit for memory purposes
            #metadata = metadata[:n_movies]
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

    # User input for watch history
    user_history_input = st.text_area("Enter watched movies as a JSON list:", '["The Dark Knight", "Inception"]')
    user_watched_movies = json.loads(user_history_input)

    # Get recommendations based on user's watch history
    if st.button("Get Recommendations"):
        with st.spinner("Finding relevant movies..."):
            start_time = time.time()
            recommended_movies = get_recommendations(user_watched_movies, 
                                                     st.session_state.vec_db, 
                                                     st.session_state.metadata)
            end_time = time.time()
            time_spent = end_time - start_time
            st.write(f"Time taken to obtain recommendations is {time_spent} seconds")

            st.write("Movies you might like:")
            st.write(recommended_movies[['title', 'score']])

if __name__ == "__main__":
    main()
