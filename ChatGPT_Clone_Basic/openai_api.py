import os
from openai import OpenAI
client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-<your-api-key>",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

print('\n**Complete Response Object**:\n', chat_completion)
print('\n**Message Response Object**:\n', chat_completion.choices[0].message)
print('\n**Message Response Content**:\n', chat_completion.choices[0].message.content)