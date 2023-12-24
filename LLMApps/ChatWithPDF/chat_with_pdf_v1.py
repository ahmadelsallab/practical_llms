import os
from openai import OpenAI
import streamlit as st
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Hardcoded system message for extra context
'''
Let's use prompt templates to understand some research papers.
The following is a prompt template for GPT3 research paper [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165).

'''

system_msg = "Act as an AI expert who will answer questions about the {paper}."
paper = """
        Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of 
        text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires 
        task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a 
        new language task from only a few examples or from simple instructions - something which current NLP systems still largely 
        struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, 
        sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches. Specifically, we train GPT-3, 
        an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, 
        and test its performance in the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or fine-tuning,
        with tasks and few-shot demonstrations specified purely via text interaction with the model. GPT-3 achieves strong performance on
        many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly 
        reasoning or domain adaptation, such as unscrambling words, using a novel word in a sentence, or performing 3-digit arithmetic. 
        At the same time, we also identify some datasets where GPT-3's few-shot learning still struggles, as well as some datasets where 
        GPT-3 faces methodological issues related to training on large web corpora. Finally, we find that GPT-3 can generate samples of 
        news articles which human evaluators have difficulty distinguishing from articles written by humans. We discuss broader societal 
        impacts of this finding and of GPT-3 in general.
        """

system_msg = system_msg.format(paper=paper)

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
