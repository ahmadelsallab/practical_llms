# YouTube Assistant
Now lets work on a new app: "Youtube assisstant". This app is the same as Chat with PDF, except that the extra context is provided as youtube url. We need to transcribe it into text first. From there, all should work the same as RAG model with vector db we just built.

YouTube Assistant is a chatbot application that leverages the power of large language models to provide contextual responses based on content extracted from YouTube videos. This application is built using Streamlit, LangChain, and OpenAI's GPT models.

## Features

- **YouTube Transcript Extraction**: Automatically extracts transcripts from YouTube videos using the LangChain library's `YoutubeLoader`.
- **RAG Model Integration**: Utilizes Retrieval-Augmented Generation for enhanced chatbot responses based on the YouTube video's context.
- **Interactive Chat Interface**: Built with Streamlit, allowing for easy interaction and a user-friendly experience.
- **Vector Database Creation**: Transforms extracted text into a searchable vector database using FAISS for efficient context retrieval.

## How It Works

1. **Enter YouTube URL**: Users can input the URL of a YouTube video in the provided text box.
2. **Extract Transcript**: The application processes the video to extract its transcript, which is then used as context for the chatbot.
3. **Chat Interaction**: Users can interact with the chatbot, which uses the extracted video transcript to provide contextually relevant responses.

## Setup and Installation

Follow the instructions in the main repo

## Running the Application
Launch the application by running the Streamlit server:
```
streamlit run youtube_assistant.py
```