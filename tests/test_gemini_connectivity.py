import unittest

from modules.generator import (
    generate_answer,
    generate_research_gaps,
    generate_summary,
    is_api_key_configured,
)


@unittest.skipUnless(
    is_api_key_configured(),
    "Set GEMINI_API_KEY in .env or Streamlit Secrets to run live Gemini tests.",
)
class GeminiConnectivityTests(unittest.TestCase):
    context = (
        "This hypothetical study evaluates a retrieval method. "
        "Its reported limitation is that it was tested only on English-language papers. "
        "The authors suggest evaluating the method on additional languages."
    )

    def test_chat_answer_generation(self):
        answer = generate_answer(
            "The capital of France is Paris.",
            "What is the capital of France?",
        )

        self.assertIn("paris", answer.lower())

    def test_summary_generation(self):
        summary = generate_summary(self.context)

        self.assertTrue(summary.strip())

    def test_research_gap_generation(self):
        gaps = generate_research_gaps(self.context)

        self.assertTrue(gaps.strip())


if __name__ == "__main__":
    unittest.main()
