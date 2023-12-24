# Chat with your PDF

This section of the course explores various versions of a chatbot integrated with PDF content. These versions range from simple implementations using hardcoded context to more complex setups involving vector databases and semantic search. Each version builds upon the previous one, introducing new concepts and techniques.

## Versions Overview

### v1: Simple Chatbot with Hardcoded Context
- **Description**: A basic chatbot using the OpenAI API.
- **Key Feature**: Utilizes a hardcoded `system_msg` string for extra context.
- **Purpose**: Understand how to provide context to a chatbot using a system message.

### v2: Chatbot with Stream and History Management
- **Description**: Enhances the chatbot with streaming capabilities and history management.
- **Key Feature**: Extra context provided through a sidebar text area, integrated into the chat as a system message.
- **Purpose**: Learn about streaming responses and managing chat history with additional context from user input.

### v3: Chatbot with RAG Model and Vector DB
- **Description**: Advanced chatbot using a Retrieval-Augmented Generation (RAG) model with vector database and semantic search. Extends the chatbot to process and utilize content from an uploaded PDF file.
- **Key Feature**: Creates a vector database from PDF content and utilizes semantic search for context retrieval.

### v4: Chatbot with RAG Model and Vector DB --> Show relevant context
- **Description**: Same as V3, showing the relevant context using RAG.
- **Key Feature**: Shows relevant context in side bar

### v5: Chatbot with RAG Model and Vector DB --> Format and parse relevant context
- **Description**: Same as V4, formatting the retrieved context.
- **Key Feature**: Formatting the retrieved context.

### v5.1: Chatbot with RAG Model and Vector DB --> Use prompt directly instead of system_message
- **Description**: Same as V5, but using the prompt template of the message, in case the LLM we use is not like OpenAI (not using System Message).
- **Key Feature**: Use Prompt template of the message

### v6: Generic hatbot with RAG Model and Vector DB --> Add system message in UI
- **Description**: Same as V5, but instead of hard coding the system message, we can design our bot as we want.
- **Key Feature**: Generic RAG Bot with configurable Persona.

## Learning Objectives
- Understand the basics of integrating external content into chatbot responses.
- Explore different methods of providing context to chatbots.
- Learn about advanced concepts like vector databases and semantic search in chatbot applications.

## Prerequisites
- Familiarity with Python and Streamlit.
- Basic understanding of chatbots and the OpenAI GPT models.
- Knowledge of PDF handling and text extraction in Python.

## Getting Started
Follow the instructions in each version's directory to set up and run the chatbot applications. Ensure you have the required dependencies installed and understand the key concepts introduced in each version.

---

Enjoy building and experimenting with these chatbot versions! Your feedback and contributions are welcome.
