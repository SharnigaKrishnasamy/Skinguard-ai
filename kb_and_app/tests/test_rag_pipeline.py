
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from rag.rag_pipeline import answer


class TestRAGPipeline(unittest.TestCase):

    def test_melanoma_returns_correct_source(self):
        result = answer("What is melanoma?")

        self.assertTrue(result["sufficient_evidence"])
        self.assertEqual(result["sources"][0]["title"], "Melanoma")

    def test_dermatofibroma_returns_correct_source(self):
        result = answer("What is dermatofibroma?")

        self.assertTrue(result["sufficient_evidence"])
        self.assertEqual(
            result["sources"][0]["title"],
            "Dermatofibroma"
        )

    def test_empty_question_returns_insufficient_evidence(self):
        result = answer("")

        self.assertFalse(result["sufficient_evidence"])
        self.assertEqual(result["sources"], [])

    def test_response_has_required_keys(self):
        result = answer("What is melanoma?")

        self.assertEqual(
            set(result.keys()),
            {"answer", "sources", "sufficient_evidence"}
        )

    def test_unrelated_question_returns_no_source(self):
        result = answer("Tell me about something unrelated")

        self.assertFalse(result["sufficient_evidence"])
        self.assertEqual(result["sources"], [])

    def test_answer_includes_medical_safety_disclaimer(self):
        result = answer("What is melanoma?")
        answer_text = result["answer"].lower()

        self.assertIn("educational only", answer_text)
        self.assertIn("not a medical diagnosis", answer_text)
        self.assertIn("consult a dermatologist", answer_text)

    def test_sources_are_a_list(self):
        result = answer("What is melanoma?")

        self.assertIsInstance(result["sources"], list)
        self.assertGreater(len(result["sources"]), 0)


if __name__ == "__main__":
    unittest.main()
