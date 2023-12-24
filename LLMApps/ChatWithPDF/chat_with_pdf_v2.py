import os
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def stream_chat_response(message, chat_history, system_msg_content, model_name, temperature, max_history_length):
    system_msg = [{"role": "system", "content": system_msg_content}]  # Adding system message to chat history
    chat_history.append({"role": "user", "content": message})
    if len(chat_history) > max_history_length:
        chat_history = chat_history[-max_history_length:]
    messages = system_msg + chat_history
    
    stream = client.chat.completions.create(
        messages=messages,
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
    
    # Sidebar text area for paper content
    paper_content = st.sidebar.text_area("Paste Paper Content Here (Example [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165))", value="", height=300)
    system_msg = "Act as an AI expert who will answer questions about the following content:\n{paper_content}"
    system_msg = system_msg.format(paper_content=paper_content)

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
            for response_chunk in stream_chat_response(user_input, st.session_state.chat_history, system_msg, model_name, temperature, max_history_length):
                accumulated_response += response_chunk
                placeholder.markdown(accumulated_response)
            st.session_state.chat_history.append({"role": "assistant", "content": accumulated_response})

# Running the Streamlit app
if __name__ == "__main__":
    main()
