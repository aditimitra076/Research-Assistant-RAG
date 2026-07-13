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


def generate_summary(
        context
):

    prompt = f"""

You are an expert Research Assistant.

Read the research paper context and produce a structured summary.

Use ONLY the provided context.

Return the summary in the following format.

# Paper Title

# Authors

# Abstract (2-4 sentences)

# Main Contributions
- Bullet points

# Methodology
- Bullet points

# Key Findings
- Bullet points

# Limitations
- Bullet points

# Future Work
- Bullet points

If any section is unavailable, write:

Not available in the document.

Context:

{context}

Summary:
"""

    response = client.chat_completion(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=700
    )

    return response.choices[0].message.content

