from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Say hello briefly."
        }
    ]
)

print(response.content[0].text)
