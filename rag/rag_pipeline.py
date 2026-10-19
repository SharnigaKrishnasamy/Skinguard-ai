import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "kb_and_app"

if str(KB_DIR) not in sys.path:
    sys.path.insert(0, str(KB_DIR))

from knowledge_base import load_knowledge_base

CLASS_KEYWORDS = {
    "akiec": ["akiec", "actinic keratosis", "solar keratosis"],
    "bcc": ["bcc", "basal cell carcinoma"],
    "bkl": ["bkl", "benign keratosis", "seborrhoeic keratosis", "seborrheic keratosis"],
    "df": ["df", "dermatofibroma"],
    "mel": ["mel", "melanoma"],
    "nv": ["nv", "melanocytic nevus", "melanocytic naevus", "mole", "moles"],
    "vasc": ["vasc", "vascular lesion", "vascular lesions"],
}


def answer(question, predicted_label=None):
    """Return educational information with its source."""

    kb = load_knowledge_base()
    question = (question or "").strip().lower()

    if not question:
        return {
            "answer": "Please enter a question about skin-lesion information.",
            "sources": [],
            "sufficient_evidence": False,
        }

    selected_code = None

    # Prefer explicit condition names in the user's question.
    for code, keywords in CLASS_KEYWORDS.items():
        if any(keyword in question for keyword in keywords):
            selected_code = code
            break

    # Use the predicted label only when the question has no known condition.
    valid_codes = set(kb.keys())
    label = (predicted_label or "").strip().lower()

    if selected_code is None and label in valid_codes:
        selected_code = label

    if selected_code is None:
        return {
            "answer": (
                "I could not identify a relevant topic in the knowledge base. "
                "Please mention a specific skin-lesion category, or consult "
                "a dermatologist for medical advice."
            ),
            "sources": [],
            "sufficient_evidence": False,
        }

    document = kb[selected_code]

    return {
        "answer": (
            document["content"]
            + "\n\nThis information is educational only and is not a "
            "medical diagnosis. Consult a dermatologist for assessment."
        ),
        "sources": [{
            "title": document["title"],
            "url": document["source_url"],
        }],
        "sufficient_evidence": True,
    }


if __name__ == "__main__":
    for question in ["What is melanoma?", "What is dermatofibroma?"]:
        result = answer(question)
        print("\nQuestion:", question)
        print("Selected source:", result["sources"])
        print("Sufficient evidence:", result["sufficient_evidence"])
