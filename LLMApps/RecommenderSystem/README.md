# Recommender System

The Recommender System is a Streamlit-based application designed to recommend movies using the IMDB movie dataset. The system is built progressively through various versions, each employing different techniques to enhance the recommendation quality.

## IMDB Dataset
We will use MovieLense dataset. The dataset can be downloaded from [here](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

## Overview of Versions

### v1: Simple Rank-Based Recommender
- **Description**: Recommends the top-5 popular movies based on their ranks.
- **Implementation**: Utilizes movie rankings to suggest the most popular movies.

### v2.1: Content-Based Recommender System
- **Description**: Uses the movie overview to create content-based recommendations.
- **Implementation**: 
   - Calculates TF-IDF features for all movie overviews.
   - Takes a user's watch history in JSON format to generate user profile features based on watched movie overviews.
   - Recommends top-5 movies based on cosine similarity between user features and movie features.
### v2.2: Content-Based Recommender System with Soup of Features
- **Description**: Same as v2.1, but with more than the overview. We include: cast, director, genres...etc
- **Implementation**: 
   - Calculates TF-IDF features for all movie overviews+cast+director+genres...etc
   - Takes a user's watch history in JSON format to generate user profile features based on watched movie features.
   - Recommends top-5 movies based on cosine similarity between user features and movie features.

### v3: Collaborative Filtering with Embeddings
- **Description**: Similar to v2 but replaces TF-IDF with embeddings for both movies and users.
- **Implementation**:
   - Generates embeddings for movie overviews and stores them in a vector database.
   - Creates user embeddings from the user's watch history.
   - Recommends top-5 movies based on cosine similarity between user embedding and movie embeddings.
   - Utilizes FAISS (from LangChain) for the vector database and OpenAI embeddings.

### v4: Collaborative Filtering with ANN
- **Description**: Enhances v3 by using Approximate Nearest Neighbor (ANN) search for recommendations.
- **Implementation**:
   - Similar to v3 but employs `vector_db.similarity_search` for efficient retrieval of similar movies.
   - Leverages the power of ANN for scalable and fast recommendation generation.

