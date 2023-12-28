import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

# Fetching API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

def stream_chat_response(message, chat_history, model_name, temperature, max_history_length):
    chat_history.append({"role": "user", "content": message})

    if len(chat_history) > max_history_length:
        chat_history = chat_history[-max_history_length:]

    stream = client.chat.completions.create(
        messages=chat_history,
        model=model_name,
        temperature=temperature,
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def clear_chat():
    st.session_state.chat_history = []

# Streamlit web interface setup
def main():
    st.title("💬 Chat with AI")

    # Sidebar controls
    model_name = st.sidebar.selectbox("Choose the Model", ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"], index=1)
    temperature = st.sidebar.slider("Set Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_history_length = int(st.sidebar.number_input("Max History Length", min_value=1, max_value=10, value=3))
    if st.sidebar.button("Clear Chat"):
        clear_chat()

    # Session state to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Enter your message:", key="user_input")
    
    if user_input:
        st.chat_message("user").write(user_input)
        with st.spinner("AI is generating a response..."):
            accumulated_response = ""
            placeholder = st.chat_message("AI").empty()
            for response_chunk in stream_chat_response(user_input, st.session_state.chat_history, model_name, temperature, max_history_length):
                accumulated_response += response_chunk
                placeholder.markdown(accumulated_response)
            st.session_state.chat_history.append({"role": "assistant", "content": accumulated_response})

# Running the Streamlit app
if __name__ == "__main__":
    main()
