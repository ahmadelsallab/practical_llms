import pandas as pd
import streamlit as st
from openai import OpenAI
import threading

import os
import datetime

RECOMMENDATIONS_LIFETIME = 2  # minutes
RECOMMENDATIONS_FILE = 'recommendations.txt'

import json
# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to compute the weighted rating of each movie
def weighted_rating(x, M, C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+M) * R) + (M/(M+v) * C)

# Function to get the top-5 movie recommendations
def get_simple_recommendations(metadata, k=1000):
    C = metadata['vote_average'].mean()
    M = metadata['vote_count'].quantile(0.90)

    q_movies = metadata.copy().loc[metadata['vote_count'] >= M]
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1, args=(M, C))
    q_movies = q_movies.sort_values('score', ascending=False)

    return q_movies[['title', 'vote_count', 'vote_average', 'score']].head(k)



def get_llm_recommendations(watched_movies, all_movies, model_name="gpt-3.5-turbo-1106"):#gpt-4-1106-preview and gpt-3.5-turbo-1106
    input_json = {
        'user_watched_movies': watched_movies,
        'all_movies': all_movies
    }
    print("Input to LLM: ", input_json)
    system_msg = """
       #Task:
        Act as a movie recommender system.I will give you a json like that:
        # Input:
        {
            'user_watched_movies': list of strings representing all the movies the user has watched,
            'all_movies': list of strings representing all the movies available in the database from which we can recommend movies,
        }

        # Output:
        I want you to return to me a json like that: 
        {
                'recommended_movies':[
                    list of json objects, each object represents a recommended movie including the following fields:
                    {   
                        'title': string representing the title of the recommended movie,
                        'score': string representing the score of the recommended movie, from 0 to 1, ranked based on relevance to the user,
                        'justification': string representing the reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt. limit your justification of why you picked this movie to 2 sentences maximum,
                    },
                ]
            }
        # Example Input:
        {
            'user_watched_movies':['Movie X', 'Movie Y'],
            'all_movies':['Movie 1', ..., 'Movie N'],
        }

        # Example Output:
        I want you to return to me a json like that: 
        {
                'recommended_movies':[
                    {
                    'title': 'Movie Z',
                    'score': '0.8',
                    'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',
                    },
                    {
                    'title': 'Movie P',
                    'score': '0.6',
                    'justification': 'Reason provided by the LLM why this movie matches the user. It will help debugging and improve the prompt',

                    }
                ]
            }

        #RULES:
        - Be specific with your recommendations. 
        - If the user is already watched a movie, don't recommend it, or give it score = 0
        - Pick recommendations only from the given set of all available movies 'all_movies'.
        - Movies that are sequels to movies the user has watched should be recommended with a higher score than other movies.
        - Provide your answer in json format only with no extra unformatted text so that I can parse it in code. 
        - Do not enclose your answer in ```json quotes
        """

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": json.dumps(input_json)}],
        model=model_name,
        temperature=0.1,
        top_p=0.1,
        #Compatible with gpt-4-1106-preview and gpt-3.5-turbo-1106.
        response_format={"type": "json_object"},
    )

    recommendations = json.loads(response.choices[0].message.content)['recommended_movies']
    print("Recommendations from LLM: ", recommendations)
    # Exclude wathced movies
    recommendations = [movie for movie in recommendations if movie['title'] not in watched_movies]
    
    # Exclude movies with score < 0.5   
    recommendations = [rec for rec in recommendations if float(rec['score']) > 0.5]   
            
    recommendations_df = pd.DataFrame(recommendations)

    # Rank recommendations by score descendingly
    recommendations_df = recommendations_df.sort_values(by='score', ascending=False)
    
    return recommendations_df.to_json(orient='records')

# Check if recommendations are old and need to be updated
def recommendations_need_update():
    if not os.path.exists(RECOMMENDATIONS_FILE):
        return True
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(RECOMMENDATIONS_FILE))
    return (datetime.datetime.now() - last_modified).total_seconds() > RECOMMENDATIONS_LIFETIME * 60

# Offline process to update recommendations
def update_recommendations_process(watched_movies, all_movies):
    recommendations = get_llm_recommendations(watched_movies, all_movies)
    with open(RECOMMENDATIONS_FILE, 'w') as f:
        json.dump(recommendations, f)

# Read recommendations from file
def get_cached_recommendations():
    if os.path.exists(RECOMMENDATIONS_FILE):
        with open(RECOMMENDATIONS_FILE, 'r') as f:
            return json.load(f)
    return None

def main():
    st.title("LLM-based Movie Recommender System")

    metadata = pd.read_csv('.\imdb.data\movies_metadata.csv')
    default_recommendations = get_simple_recommendations(metadata, k=1000)
    all_movies = default_recommendations['title'].tolist()

    user_history_input = st.text_area("Enter watched movies as a JSON list:", '["The Dark Knight", "Inception"]')
    watched_movies = json.loads(user_history_input)

    if st.button("Get Recommendations"):
        if recommendations_need_update():
            # Trigger the offline process
            threading.Thread(target=update_recommendations_process, args=(watched_movies, all_movies)).start()
            st.write("Fetching new recommendations...")
            #Delete old recommendations
            if os.path.exists(RECOMMENDATIONS_FILE):
                os.remove(RECOMMENDATIONS_FILE)
            st.write("Default Recommended Movies:")
            st.write(default_recommendations[:5])
        else:
            # Display cached recommendations
            cached_recommendations = get_cached_recommendations()
            if cached_recommendations:
                st.write("Cached LLM Recommended Movies:")
                st.write(pd.DataFrame(json.loads(cached_recommendations)))
            else:
                st.write("Default Recommended Movies:")
                st.write(default_recommendations[:5])

if __name__ == "__main__":
    main()
