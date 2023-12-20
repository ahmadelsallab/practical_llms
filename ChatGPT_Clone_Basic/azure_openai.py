from openai import AzureOpenAI
import os

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY", default="sk-<your-api-key>"),
    api_version="2023-03-15-preview",
    azure_endpoint="https://testopenaiahmad.openai.azure.com/")

completion = client.chat.completions.create(
    model="Test",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)

print(completion.model_dump_json(indent=2))