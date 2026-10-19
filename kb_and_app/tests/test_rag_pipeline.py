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


if __name__ == "__main__":
    unittest.main()
