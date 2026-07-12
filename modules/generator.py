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

Your job is to answer questions ONLY using the provieded context.

Instructions:

- Read the context carefully before answering.
- If the author is clearly present, answer confidently and naturally.
- Do Not invent or assume information that is not in the context.
- If the context contains author names, paper title, affiliations, publication details, abstract, keywords, or other metadata, use the information directly when relevant.
- If multiple context chunks discuss the same topic, combine them into one clear answer.
- Do NOT mention page number or chunk information.
- Do NOT say "accoding to the context" or "based on the document."
- Keep answers concise but complete.
- Never contradict yourself.
- If the answer is genuinely unavailable in tht provided context, reply exactly:

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

