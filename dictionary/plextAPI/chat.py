import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

YOUR_API_KEY = os.environ["PERPLEXITY_API_KEY"]
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

response = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "How many stars are in our galaxy?"}
    ]
)

print(response)
