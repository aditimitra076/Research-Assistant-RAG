from huggingface_hub import InferenceClient

import os


client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

def generate_answer(
        context,
        query
):
    prompt =f"""

You are an intelligent Researh Assistant.

Answer the user's question using ONLY the provided context.

Rules:

- Never make up facts.
- If the answer appears in multiple chunks, combine them naturally.
- Quote titles and author names exactly as written.
- Keep the answer concise and professional.
- Ignore irrelevant context.
- If the answer cannot be confidently found in the context, reply exactly:

"I could not find the answer in the provided document."

Context:
{context}

Question:
{query}

Answer:
"""
    
    response = client.chat_completion(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role":"user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

