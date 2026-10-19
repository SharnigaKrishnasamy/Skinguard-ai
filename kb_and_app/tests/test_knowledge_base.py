import sys
import unittest
from pathlib import Path

KB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KB_DIR))

from knowledge_base import load_knowledge_base


class TestKnowledgeBase(unittest.TestCase):

    def test_loads_all_seven_classes(self):
        kb = load_knowledge_base()
        expected_classes = {
            "akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"
        }
        self.assertEqual(set(kb.keys()), expected_classes)

    def test_documents_have_required_fields(self):
        kb = load_knowledge_base()

        for class_code, document in kb.items():
            with self.subTest(class_code=class_code):
                self.assertTrue(document["title"])
                self.assertTrue(document["content"])
                self.assertTrue(document["source_url"])

    def test_documents_include_safety_limitation(self):
        kb = load_knowledge_base()

        for class_code, document in kb.items():
            with self.subTest(class_code=class_code):
                content = document["content"].lower()
                self.assertIn("important limitation", content)
                self.assertIn("dermatologist", content)


if __name__ == "__main__":
    unittest.main()
