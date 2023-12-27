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
   - Uses OpenAI ada2 for embeddings
   - If the user watch history is unkown, we fall back to default recommendations, using simple recommender system (not personalized).

### v3.1: calculates the embeddings in a loop, with averaging of all watched user movie embeddings

### v3.2: Uses batch mode of embeddings in OpenAI ada2, with averaging of all watched user movie embeddings

### v3.3: instead of averaging embeddings, we concatenate all watch history in one string and embed that.
 This is a valid alternative:
 
 Pros:
 - Saves multiple API calls, which saves communication time
 Cons:
 - Consumes more tokens in text. But shoud be the same as multiple API calls.


### v4: Collaborative Filtering with ANN
- **Description**: Enhances v3 by using Approximate Nearest Neighbor (ANN) search for recommendations.
- **Implementation**:
   - Similar to v3 but employs `vector_db.similarity_search` for efficient retrieval of similar movies.
   - Leverages the power of ANN for scalable and fast recommendation generation.
   - Uses langchain FAISS vectorstore and OpenAIEmbeddings in langchain.embeddings

### v4.1: Uses movie titles as features
This enables that the user enters watch history as natural text, like: "I watched The Dark Knight and Jumanji"

### v4.2: Uses more movie features, like overview
The user now is asked to enter the watch history as list. Internally, we should obrain the corresponding movie overviews and any extra metadata as features. We use that as text features to get their embeddings in `create_vector_database` and same for user features in `calculate_user_features`.

### v5: Recommender System with LLM
- **Description**: In this version we leverage prompt engineering and output type forcing (JSON), to build a state of the art recommender system.
- **Implementation**:
   - The code will use LLM via OpenAI to send a JSON that contains the user watch history, along with all available movies. The input JSON will look as follows:
   ```
   {
      'user_watched_movies':['Movie X', 'Movie Y'],
      'all_movies':['Movie 1', ..., 'Movie N'],
   }
   ```
   - Through system message, we will set the bot persona to act as movie recommender that chooses movies from the list of all available movies and recommend it to the user. We will ask it to provide a score and a justification.
   ```
   {
      'recommended_movies':[
         {
            'movie': 'Movie Z',
            'score': '0.8',
            'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',
         },
         {
            'movie': 'Movie P',
            'score': '0.6',
            'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',

         }
      ]
   }
   ``` 
   - On the app side, we will filter the movies and rank them based on the score > 0.5. We can view the justification as well.


   ### LLM prompt design:
   `get_llm_recommendations` calls the OpenAI API. It shall not use streaming mode to get the answer. It also sets the system message which identifies the recommender persona and controls the output. Following prompt engineering rules, here is a working prompt design (note that: you can modify the debug via monitoring the justification of the returned recommendations to see if it make sense):

   ```
   #Task:
   Act as a movie recommender system.I will give you a json like that:

   #Input:
   {
      'user_watched_movies':['Movie X', 'Movie Y'],
      'all_movies':['Movie 1', ..., 'Movie N'],
   }

   # Output:
   I want you to return to me a json like that: 
   {
         'recommended_movies':[
            {
               'movie': 'Movie Z',
               'score': '0.8',
               'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',
            },
            {
               'movie': 'Movie P',
               'score': '0.6',
               'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',

            }
         ]
      }

   #RULES:
   - Be specific with your recommendations. 
   - If the user is already watched a movie, don't recommend it, or give it score = 0
   - Pick recommendations only from the given set of all available movies 'all_movies'.
   - Provide your answer in json format only with no extra unformatted text so that I can parse it in code. 
   - Do not enclose your answer in ```json quotes
   ```

   ### v5.1: feeding ALL movies--> fails due to large prompt beyond the context window of any model

   ### v5.2: get random 1000 movies for llm prompt as `all_movies`

   ### v5.3: use the simple recommender as a limiter for the top-1000 voted movies.

   ### v5.4: use CF+ANN for pre-select top-1000 relevant movies to the user watch history.

   ### v6: Responsive Recommender System 
- **Description**: Similar to v5, but with more responsive design. In v5, the user is blocked by the API call, which takes some time. This is called the online serving. We will use here "Lambda Architecture" for serving recommendations. In other words, we will have an online serving and offline preparation code:
      - Offline: is activated via a call to sub-process or thread, which calls the API and stores the user recommendations in a database. In streamlit, we will use the `st.session_state` as simulation to database, where we will store `recommendations` obtained via offline process. The trigger to offline shall happen on different events like: user watched a new movie, user liked/disliked a movie, periodic events...etc. In our case, we will just trigger it with every button press of "Get recommendations" for simplicity.
      - Online: in the lambda setup, the online process is just getting the cached recommendations from the database. If no cached recommendations, some default recommendations are viewed. For example, we could use simple or content-based recommendations from previous versions.
- **Implementation**:
   - `get_recommendations`: is the online process, which is responsible of querying the st.session_state.recommendations and view it to the user as table via `st.write` showing all the attributes like score and justification. If no stored recommendations, it will call `get_default_recommendations`, which can use simple or content-based recommendations from previous versions. However, in our version it will call the offline process `update_recommendations_process` in a different thread, and return default recommendations, like using simple recommendations. The `update_recommendations_process` is triggered when the user provides new watch history and presses "Get recommendations" button, or if there are no cached recommendations. In a more complicated setup, we can also add `RECOMMENDATIONS_LIFETIME` which triggers the process if the cached recommendations in `st.session_state.recommendations` is older than this life time.
   - `update_recommendations_process`: this is the offline process, which is executed in a separate thread. It is responsible of calling the LLM via `get_llm_recommendations` which calls the OpenAI API, and processing the output JSON vie `process_llm_output`. `process_llm_output` shall parse the JSON and filter out the recommendations with score < 0.5. In case of invalid JSON, it shall return default recommendations. It should also filter out the recommendations of the movies the user already watched.



### v7: Responsive Recommender System with Async OpenAI
- **Description**: This is similar to v6, but using `AsyncOpenAI` API in `get_llm_recommendations`. 
- **Implementation**: In this version we don't have to have explicit thread for offline processing. We can use `asyncio.create_task`, which is a cleaner design, and free of racing hazards unlike `threads`.