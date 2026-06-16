#############################
#testing model usng token

from dotenv import load_dotenv

from huggingface_hub import InferenceClient

import os

load_dotenv()

client = InferenceClient(
    api_key = os.getenv("HF_TOKEN")
)


response = client.chat_completion(
    model= "meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ],

    max_tokens = 100
)

print(response.choices[0].message.content)