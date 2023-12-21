# Practical LLMs

Welcome to "Practical LLMs," a course designed to guide you through the fascinating world of Large Language Models (LLMs) using Python and Streamlit. This course aims to provide hands-on experience in building various AI applications, starting from basic chatbot implementations to more advanced applications like recommendation systems and semantic search tools.

## Course Overview

This course is structured into multiple projects, each focusing on a unique aspect of LLMs and their applications. You'll start with creating simple ChatGPT clones and gradually move to more complex projects involving vector databases, YouTube assistants, and more. By the end of this course, you'll have a comprehensive understanding of LLMs and practical experience in deploying them in real-world scenarios.

## Projects

- `ChatGPT_Clone_Basic`: Learn the basics of interfacing with the OpenAI API to create a ChatGPT clone.
- `OpenSource_LLM`: Explore open-source LLMs like Llama and their unique features.
- `Streamlit_Interface`: Build a configurable Streamlit interface for interactive AI applications.
- `Applications`: Delve into a variety of applications that demonstrate the power of LLMs:
  - `ChatWithPDF_v1`: Create a chatbot that uses a PDF document as its knowledge base.
  - `ChatWithPDF_v2`: Enhance the previous chatbot with vector databases and semantic search.
  - `YoutubeAssistant`: Develop an assistant that utilizes transcriptions from YouTube videos.
  - `RecommenderSystem`: Implement a recommender system using LLMs and prompt engineering.

## Prerequisites

- Basic understanding of Python.
- Understanding of LLM and Prompt engineering.
- An OpenAI API key (obtainable from OpenAI's website).

## Getting Started

To get started with the projects, you need to follow the following steps:

## Setup and Installation


1. **Clone the Repository**:
Clone this repository:

```bash
git clone https://github.com/coursat-ai/practical_llms.git
cd practical_llms
```

2. **Environment setup**:
It's recommended to use a virtual environment to keep dependencies for this project separate. You can create and activate one using:

- On Linux:

```bash
python3 -m venv env
source env/bin/activate
```
- On Windows (Command Prompt):

```bash
python -m venv env
.\env\Scripts\activate
```

- Using conda/anaconda
```bash
conda create --name llms_course python=3.12
conda activate llms_course
```

3. **Install dependencies**:
Make sure you have Python installed on your system. Then install the required packages:

```
pip install -r requirements.txt
```

4. **API Key Configuration**:

- Using environment variables

  You need to have an OpenAI API key to interact with the GPT models.
  Set your API key as an environment variable for security:

  - On Linux
  ```bash
  export OPENAI_API_KEY='your-api-key
  ```

  - On Windows
  ```
  set OPENAI_API_KEY=your-api-key
  ```

- Using .env file

  Alternatively, you can load .env file. **This is the recommended way in this repo**

  Create a .env file in the project directory. You will find a sample env.sample in this repo.
  Add your OpenAI API key to the file:
  ```
  OPENAI_API_KEY=your-api-key
  ```
  Replace your-api-key with your actual OpenAI API key.

5. **Specific project instructions**:

  Follow the instructions in the README.md of each project directory for setup and execution details.

# Contributions
We welcome contributions to this project! If you have suggestions, bug reports, or contributions, please submit them via pull requests or issues. For more details, check out our CONTRIBUTING.md file.

# License
This project is licensed under [License Name - e.g., MIT License]. See the LICENSE file for more details.

# Contact
For any queries or feedback related to this course, feel free to reach out to [support@coursat.ai](mailto:support@aitar.ai).

Enjoy your journey through the world of Practical LLMs!