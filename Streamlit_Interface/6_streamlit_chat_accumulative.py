import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
# 
# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

# Fetching environment variables
MODEL_NAME = os.getenv("MODEL_NAME", default="gpt-3.5-turbo")
TEMPERATURE = float(os.getenv("TEMPERATURE", default="0.7"))
MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", default="3"))

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_chat_response(message, chat_history):
    chat_history.append({"role": "user", "content": message})

    # Keep the chat history within the specified max length
    if len(chat_history) > MAX_HISTORY_LENGTH:
        chat_history = chat_history[-MAX_HISTORY_LENGTH:]

    # Creating a chat completion with streaming enabled
    stream = client.chat.completions.create(
        messages=chat_history,
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Streamlit web interface setup
def main():
    st.title("💬 Chat with AI")

    # Session state to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        k = len(st.session_state.chat_history)
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Enter your message:", key="user_input")
    
    if user_input:
        st.chat_message("user").write(user_input)
        with st.spinner("AI is generating a response..."):
            accumulated_response = ""
            #placeholder = st.empty()
            placeholder = st.chat_message("AI").empty()
            for response_chunk in stream_chat_response(user_input, st.session_state.chat_history):
                accumulated_response += response_chunk
                placeholder.markdown(accumulated_response)
            st.session_state.chat_history.append({"role": "assistant", "content": accumulated_response})
            

# Running the Streamlit app
if __name__ == "__main__":
    main()
