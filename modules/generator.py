import os
import logging

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

DEFAULT_MODEL_NAME = "gemini-3.5-flash-lite"
logger = logging.getLogger(__name__)


def _get_streamlit_secret(name):
    try:
        return st.secrets.get(name)
    except (KeyError, StreamlitSecretNotFoundError):
        return None


def get_gemini_api_key():
    return os.getenv("GEMINI_API_KEY") or _get_streamlit_secret("GEMINI_API_KEY")


def get_gemini_model():
    return (
        os.getenv("GEMINI_MODEL")
        or _get_streamlit_secret("GEMINI_MODEL")
        or DEFAULT_MODEL_NAME
    ).strip()


def is_api_key_configured():
    return bool(get_gemini_api_key())


def format_generation_error(error):
    error_text = str(getattr(error, "message", error)).lower()
    status_code = getattr(error, "code", None)

    if "gemini_api_key is missing" in error_text:
        return (
            "Gemini API key is not configured. Set GEMINI_API_KEY in the local .env "
            "file or Streamlit Secrets."
        )

    if (
        status_code == 401
        or "unauthenticated" in error_text
        or "invalid api key" in error_text
        or "api_key_invalid" in error_text
        or "api key not valid" in error_text
    ):
        return (
            "Gemini authentication failed. Check that GEMINI_API_KEY is valid and "
            "belongs to the intended Google AI Studio project."
        )

    if status_code == 429 or any(
        term in error_text
        for term in ("resource_exhausted", "quota", "rate limit")
    ):
        return (
            "Gemini returned a quota or rate-limit error. Check this project's "
            "model-specific RPM, TPM, RPD, and tier in Google AI Studio; the error "
            "does not identify which limit was reached. The app does not retry "
            "generation requests automatically."
        )

    if (
        status_code in (403, 404)
        or "model not found" in error_text
        or "model is unavailable" in error_text
    ):
        return (
            "Gemini denied access to the configured model. Check GEMINI_MODEL, "
            "the selected Google AI Studio project, and that the model is available "
            "to that project."
        )

    return (
        "Gemini generation failed. Check the application log for the sanitized "
        "technical error and verify the model and project configuration."
    )


def _get_client():
    api_key = get_gemini_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the local .env file or Streamlit Secrets."
        )

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(attempts=1)
        ),
    )


def _log_generation_error(error, model, api_key):
    if isinstance(error, APIError):
        detail = (
            error.message.replace(api_key, "[REDACTED_API_KEY]")
            if api_key
            else error.message
        )
        logger.error(
            "Gemini generation failed: model=%s status=%s error=%s",
            model,
            error.code,
            detail,
        )
        return

    logger.error(
        "Gemini generation failed: model=%s error_type=%s",
        model,
        type(error).__name__,
    )


def _generate(prompt, max_tokens):
    api_key = get_gemini_api_key()
    model = get_gemini_model()

    try:
        client = _get_client()

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.2,
                ),
            )
        finally:
            client.close()

        answer = response.text

        if not answer or not answer.strip():
            raise RuntimeError("The model returned an empty response.")

        return answer.strip()

    except Exception as error:
        _log_generation_error(error, model, api_key)
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