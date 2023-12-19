import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
# https://medium.com/@jmgb_ai/comparing-async-and-sync-calls-with-openais-gpt-api-447ea5f43b64

# Load environment variables from .env file in the parent directory
env_path = os.path.join("..", '.env')
load_dotenv(env_path)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", default="sk-<your-api-key>"))


async def main():
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Describe the sun in scientific terms"}],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
    


asyncio.run(main())
