import os
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"),
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Describe the sun in scientific terms",
        }
    ],
    model="gpt-3.5-turbo",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")