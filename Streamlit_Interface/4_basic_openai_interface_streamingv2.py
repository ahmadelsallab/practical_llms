import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"))

def stream_chat_response(message):
    # Create a chat completion with streaming enabled
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": message}],
        model="gpt-3.5-turbo",
        stream=True,
    )

    # Yield each chunk of the response as it's received
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Streamlit web interface setup
def main():
    st.title("Ask the AI")
    user_input = st.text_input("Enter your message:", key="user_input")

    # Placeholder for dynamic updates
    response_placeholder = st.empty()

    if st.button("Send") or user_input:
        if user_input:
            response_text = ""
            # Stream the response and update the interface in real-time
            with st.spinner("AI is generating a response..."):
                for response_part in stream_chat_response(user_input):
                    response_text += response_part
                    response_placeholder.text_area("AI Response:", value=response_text, height=200)
        else:
            st.warning("Please enter a message.")

# Running the Streamlit app
if __name__ == "__main__":
    main()
