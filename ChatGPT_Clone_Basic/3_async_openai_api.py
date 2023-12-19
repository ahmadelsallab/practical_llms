import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"))

async def fetch_chat_completion():
    # This function will run the chat completion asynchronously
    chat_completion = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Describe the sun in scientific terms"}],
    )
    print('\n**Response Ready**\n', chat_completion.choices[0].message.content)


async def main():
    print("Hello World! Let's send a chat completion request to OpenAI!")
    # Create an asynchronous task for the chat completion
    task = asyncio.create_task(fetch_chat_completion())

    # Proceed with other operations
    print("I am not blocked with the chat completion task!")

    # Optionally, wait for the task to complete if needed later in the code
    await task

asyncio.run(main())
