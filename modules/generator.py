import os
import logging

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def is_api_key_configured():
    return bool(get_gemini_api_key())


def format_generation_error(error):
    error_text = str(error)

    if "api_key" in error_text.lower() or "api key" in error_text.lower() or "invalid" in error_text.lower():
        return (
            "⚠️ Gemini API key is invalid or missing. "
            "Get a free key from https://aistudio.google.com/apikey, "
            "set GEMINI_API_KEY=<your-key> in the .env file, then restart Streamlit."
        )

    if "quota" in error_text.lower() or "rate" in error_text.lower() or "429" in error_text:
        return (
            "⚠️ Gemini free-tier rate limit reached. "
            "Wait a moment and try again, or check your quota at https://aistudio.google.com."
        )

    return f"⚠️ Generation failed: {error_text}"


def _get_client():
    api_key = get_gemini_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Get a free key from https://aistudio.google.com/apikey and add it to .env."
        )

    return genai.Client(api_key=api_key)


def _generate(prompt, max_tokens):
    try:
        client = _get_client()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.2,
            ),
        )

        answer = response.text

        if not answer or not answer.strip():
            raise RuntimeError("The model returned an empty response.")

        return answer.strip()

    except Exception:
        logging.exception("Gemini generation failed")
        raise


def generate_answer(context, query):
    prompt = f"""You are an intelligent Research Assistant.

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
    prompt = f"""You are an expert Research Assistant.

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
    prompt = f"""You are an expert AI Research Assistant.

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