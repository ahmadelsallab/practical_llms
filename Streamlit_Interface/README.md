# Building a ChatGPT Clone with Streamlit

This section focuses on creating a ChatGPT clone using Streamlit, an open-source app framework. The course is structured into versions, each adding new functionality and complexity. The goal is to familiarize learners with Streamlit and progressively build a feature-rich chatbot.

## Versions Overview

### v1: Basic OpenAI API Call via Streamlit
- **Description**: Simple implementation of an OpenAI API call within a Streamlit app.
- **Objective**: Get familiar with the basics of Streamlit and API integration.

### v2: Managing Secrets with `st.secrets`
- **Description**: Use Streamlit's `st.secrets` for managing sensitive information like API keys.
- **Objective**: Learn about secure management of secrets in Streamlit applications.

### v3: Streaming Feature Integration
- **Description**: Implement the streaming capability of the OpenAI API in the Streamlit UI.
- **Objective**: Understand how to use Python generators for streaming data in Streamlit.

### v4: Building a Functional Chatbot
- **Description**: Develop a chatbot with history/memory context management.
- **Objective**: Create a chatbot that maintains conversation context for more coherent interactions.

### v5: ChatGPT Clone with Chat Interaction
- **Description**: Enhance the chatbot to include all chat interactions visible to the user.
- **Objective**: Build a ChatGPT-like interface with full conversation history.

### v6: Clear Chat and API Options
- **Description**: Add features to clear chat history and set API options via the Streamlit UI.
- **Objective**: Introduce advanced UI elements for better user control and customization.

### v7: User Feedback Integration
- **Description**: Implement a user feedback system to evaluate the bot's responses.
- **Objective**: Learn to gather and handle user feedback within a Streamlit application.

## Learning Objectives
- Gain proficiency in building applications with Streamlit.
- Learn to integrate and interact with the OpenAI API.
- Understand the implementation of streaming data in a user interface.
- Develop skills in managing conversation context and history in chat applications.
- Implement user interaction and feedback features.

## Prerequisites
- Basic understanding of Python and asynchronous programming.
- Familiarity with Streamlit and its components.
- Knowledge of interacting with APIs, particularly the OpenAI API.

## Getting Started
Begin with v1 and progress through each version, following the instructions provided. Ensure you have Streamlit installed and are familiar with its basic operation. 

### Streamlit secrets
In some code versions we use st.secrets. This is similar to env files. But the variables are in a file called secrets.toml. This file is either kept in:
- the same folder as the app, or 
```
your-app-directory/
├─ .streamlit/
│  ├─ secrets.toml
├─ app.py
```
- system wide folder (in windows, this is under your user folder: C:\Users\<user-name>\.streamlit)

---

Enjoy exploring the capabilities of Streamlit in building an advanced chatbot, and feel free to provide feedback or contributions to the project.
