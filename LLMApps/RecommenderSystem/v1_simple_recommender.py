import pandas as pd
import streamlit as st

# Function to compute the weighted rating of each movie
def weighted_rating(x, M, C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+M) * R) + (M/(M+v) * C)

# Function to get the top-5 movie recommendations
def get_recommendations(metadata):
    C = metadata['vote_average'].mean()
    M = metadata['vote_count'].quantile(0.90)

    q_movies = metadata.copy().loc[metadata['vote_count'] >= M]
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1, args=(M, C))
    q_movies = q_movies.sort_values('score', ascending=False)

    return q_movies[['title', 'vote_count', 'vote_average', 'score']].head(5)

def main():
    st.title("Movie Recommender System")

    # Load Movies Metadata
    # Update the path to the dataset as per your setup
    metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')

    top_movies = get_recommendations(metadata)

    # Display the top 5 movies
    st.write("Top 5 Movies Based on Popularity and Votes:")
    st.write(top_movies)

if __name__ == "__main__":
    main()
