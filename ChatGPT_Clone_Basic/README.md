# ChatGPT Clone Basic

# Basic OpenAI API Interfacing

Welcome to the `ChatGPT_Clone_Basic` project! This is the first practical project in the "practical_llms" course. In this project, you will build a basic version of a ChatGPT clone using Python and the OpenAI API. This introductory project aims to familiarize you with the process of integrating with OpenAI's GPT models and setting up a simple chat interface.



## Learning Objectives
- Grasp the basics of interacting with OpenAI's API.
- Understand the importance of security in API interactions.
- Gain experience with JSON data structures.
- Learn asynchronous programming techniques.
- Explore streaming data handling.cd
- Develop a contextual understanding in chatbot applications.

## Prerequisites
- Basic knowledge of Python programming.
- Familiarity with JSON data format.
- Understanding of asynchronous programming concepts.

## Getting Started
Each version in this section builds upon the previous one. Start with v1 and progress through to v7, following the instructions and exploring the code in each version's directory.

---

Enjoy your journey through these diverse implementations of OpenAI API interfacing. Feedback and contributions are always welcome.


## Objectives

- Understand how to use the OpenAI API.
- Implement a basic chatbot in Python that interacts with the GPT model.
- Learn the basics of handling user input and generating AI-based responses.

## Prerequisites

- Basic knowledge of Python programming.
- An OpenAI API key (you can obtain one by signing up on OpenAI's website).

## Setup and Installation

1. **Clone the Repository**:
Clone this repository and navigate to the desired project directory:
   ```
   git clone https://github.com/coursat-ai/practical_llms.git
   cd practical_llms/ChatGPT_Clone_Basic
   ```

2. **Install Dependencies**:

    Follow the same instructions as in the main repo [README.md](../README.md)


3. **API Key Configuration**:

    Follow the same instructions as in the main repo [README.md](../README.md)

4. **Running the Project**

    Run the script:

    ```bash
    python chatgpt_clone.py
    ```

    Follow the on-screen instructions to chat with the AI model.

    Other examples can be run in the same way.

## Code Overview

This section of the course focuses on interfacing with the OpenAI API. It covers a range of implementations, from simple API interactions to building a fully functional chatbot with contextual understanding and history management.


### v1: Basic OpenAI API Interface (Hardcoded API Key)
- **Description**: Introduction to OpenAI API interaction with a hardcoded API key.
- **Purpose**: Understand the basics of OpenAI API and how to make requests to it.

### v2: API Key via Environment File
- **Description**: Enhance security by loading the API key from an environment file.
- **Purpose**: Learn about environment variables and the importance of keeping sensitive information secure.

### v3: Structured JSON Return
- **Description**: Modify the API interaction to force structured responses in JSON format.
- **Purpose**: Understand data formatting and the benefits of structured JSON responses for easier data handling.

### v4: Asynchronous API Clients
- **Description**: Implement asynchronous API calls for responsive user interactions and streaming.
- **Purpose**: Explore asynchronous programming to improve application performance and responsiveness.

### v5: OpenAI API for Streaming
- **Description**: Utilize OpenAI API's streaming capabilities for dynamic response generation.
- **Purpose**: Learn to handle streaming data from the OpenAI API for real-time applications.

### v6: ChatGPT Clone with Streaming
- **Description**: Build a ChatGPT-like application with environment variables and streaming features.
- **Purpose**: Combine knowledge of OpenAI API, environmental variables, and streaming to create a ChatGPT clone.

### v7: Contextual ChatGPT Clone with History Management
- **Description**: Develop an advanced chatbot capable of maintaining context and history throughout user interactions.
- **Purpose**: Implement history/memory management in a chatbot to provide contextually relevant responses.    
