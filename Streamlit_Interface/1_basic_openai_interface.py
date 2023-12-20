import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file located in the parent directory.
# This is important for securely managing sensitive data like API keys.
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

# Initialize the OpenAI client with your API key.
# Replace "sk-<your-api-key>" with your actual OpenAI API key.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"))

def get_chat_response(message):
    # Function to get a chat response from the OpenAI API.
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": message},
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content

# Streamlit web interface setup
def main():
    st.title("Ask the AI")

    # Creating a text input widget for user input.
    user_input = st.text_input("Enter your message:", key="user_input")

    # A button to send the message. When clicked, it triggers the response generation.
    # Note that, without the "or user_input" part, the button will not work when the user input is empty.
    if st.button("Send") or user_input:
        if user_input:
            # Displaying a spinner while the AI generates a response.
            with st.spinner("AI is generating a response..."):
                response = get_chat_response(user_input)
                # Displaying the AI response in a text area widget.
                st.text_area("AI Response:", value=response, height=200)
        else:
            # Warning shown if no input is provided by the user.
            st.warning("Please enter a message.")

# Running the Streamlit app
if __name__ == "__main__":
    main()
