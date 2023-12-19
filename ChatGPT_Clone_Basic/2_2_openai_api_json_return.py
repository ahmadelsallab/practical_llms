#https://github.com/openai/openai-python#using-types
#https://github.com/openai/openai-python#nested-params

from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

# Create an OpenAI client instance using the API key from the .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"))

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Can you generate an example json object describing a fruit?",
        }
    ],
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
)
print('\n**Complete Response Object**:\n', completion)
print('\n**Message Response Object**:\n', completion.choices[0].message)
print('\n**Message Response Content**:\n', completion.choices[0].message.content)