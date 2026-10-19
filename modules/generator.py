import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def is_gemini_api_key_configured():
    return bool(get_gemini_api_key())


# Compatibility with existing UI code that may call this function.
def is_hf_token_configured():
    return is_gemini_api_key_configured()


def _generate(prompt, max_tokens):
    api_key = get_gemini_api_key()

    if not api_key:
        raise RuntimeError(
            "Configure GEMINI_API_KEY in your .env file or Streamlit Secrets."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "The model returned an empty response. Please try again."
        )

    return response.text.strip()


def generate_answer(context, query):
    prompt = f"""
You are an intelligent Research Assistant.

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

    return _generate(prompt, max_tokens=500)


def generate_summary(context):
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

    return _generate(prompt, max_tokens=700)


def generate_research_gaps(context):
    prompt = f"""
You are an expert AI Research Assistant.

Analyze ONLY the provided research paper context.

Identify research gaps, open problems, limitations, and future research
directions mentioned or strongly implied by the paper.

Return the result in this format.

# Research Gaps
- Gap 1
- Gap 2
- Gap 3

# Open Problems
- Problem 1
- Problem 2

# Future Research Directions
- Direction 1
- Direction 2
- Direction 3

Rules:
- Use ONLY the provided context.
- Do NOT invent research gaps.
- If a section is unavailable, write:

Not available in the document.

Context:
{context}

Research Gaps:
"""

    return _generate(prompt, max_tokens=700)