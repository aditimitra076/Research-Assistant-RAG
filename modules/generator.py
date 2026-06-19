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
You are a helpful reserach assistant.

Answer the question using ONLY the provided context.

If authors, tutle, abstract, affiliations, publication information,
or metadata are present in the context, use them directly.

If answer is not found , say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{query}
"""
    
    response = client.chat_completion(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role":"user",
                "content": prompt
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

