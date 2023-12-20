import os
from openai import OpenAI

import streamlit as st

# Initialize the OpenAI client with your API key.
# Setting Up st.secrets:

#In your local development environment, you can create a file named secrets.toml in your Streamlit project directory with the following content: toml
# secrets.toml should be in a folder named .streamlit
# OPENAI_API_KEY = "your_openai_api_key_here"

# On Streamlit Cloud, you can use the app settings to securely add your secrets.
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
