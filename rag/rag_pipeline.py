
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "kb_and_app"

if str(KB_DIR) not in sys.path:
    sys.path.insert(0, str(KB_DIR))

from knowledge_base import load_knowledge_base


CLASS_KEYWORDS = {
    "akiec": [
        "akiec",
        "actinic keratosis",
        "solar keratosis",
    ],
    "bcc": [
        "bcc",
        "basal cell carcinoma",
    ],
    "bkl": [
        "bkl",
        "benign keratosis",
        "seborrhoeic keratosis",
        "seborrheic keratosis",
    ],
    "df": [
        "df",
        "dermatofibroma",
    ],
    "mel": [
        "mel",
        "melanoma",
    ],
    "nv": [
        "nv",
        "melanocytic nevus",
        "melanocytic naevus",
        "mole",
        "moles",
    ],
    "vasc": [
        "vasc",
        "vascular lesion",
        "vascular lesions",
    ],
}


def answer(question, predicted_label=None):
    """Return educational information and its source."""

    kb = load_knowledge_base()
    question = (question or "").strip().lower()

    # Handle an empty question.
    if not question:
        return {
            "answer": (
                "Please enter a question about "
                "skin-lesion information."
            ),
            "sources": [],
            "sufficient_evidence": False,
        }

    # Refuse requests for personal diagnosis, exact staging, or guarantees.
    safety_patterns = [
        r"exact.{0,30}(diagnosis|stage)",
        r"(diagnos(e|is)).{0,30}(me|my|photo|image)",
        r"my exact melanoma stage",
        r"stage.{0,30}(photo|image)",
        r"prescribe",
        r"personally start",
        r"guarantee.{0,50}(harmless|never misses|never miss|100 percent)",
        r"(never misses|never miss).{0,30}melanoma",
        r"confirm.{0,30}(do not need|don't need).{0,30}dermatologist",
    ]

    if any(re.search(pattern, question) for pattern in safety_patterns):
        return {
            "answer": (
                "I cannot diagnose a skin lesion, determine its exact stage, "
                "or guarantee that a model will never miss melanoma. "
                "This tool provides educational information only and is not "
                "a medical diagnosis. Please consult a dermatologist for "
                "assessment, especially for a changing or suspicious lesion."
            ),
            "sources": [],
            "sufficient_evidence": False,
        }

    selected_code = None

    # Match complete keywords instead of arbitrary substrings.
    # This reduces accidental matches for short terms like "mel".
    for code, keywords in CLASS_KEYWORDS.items():
        if any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                question,
            )
            for keyword in keywords
        ):
            selected_code = code
            break

    # Use a valid predicted label only if the question
    # does not mention a recognized category.
    valid_codes = set(kb.keys())
    label = (predicted_label or "").strip().lower()

    if selected_code is None and label in valid_codes:
        selected_code = label

    # Handle questions that do not match a known topic.
    if selected_code is None:
        return {
            "answer": (
                "I could not identify a relevant topic in "
                "the knowledge base. Please mention a specific "
                "skin-lesion category, or consult a dermatologist "
                "for medical advice."
            ),
            "sources": [],
            "sufficient_evidence": False,
        }

    # Handle a missing document safely.
    document = kb.get(selected_code)

    if not document:
        return {
            "answer": (
                "Information for this category is currently "
                "unavailable in the knowledge base."
            ),
            "sources": [],
            "sufficient_evidence": False,
        }

    # Return educational content and its source.
    return {
        "answer": (
            document["content"]
            + "\n\nThis information is educational only and is not a "
            "medical diagnosis. Consult a dermatologist for assessment."
        ),
        "sources": [
            {
                "title": document["title"],
                "url": document["source_url"],
            }
        ],
        # A matching document is available; this does not
        # mean clinical evidence has been independently verified.
        "sufficient_evidence": True,
    }


if __name__ == "__main__":
    test_questions = [
        "What is melanoma?",
        "What is dermatofibroma?",
        "Tell me about something unrelated",
        "",
    ]

    for question in test_questions:
        result = answer(question)

        print("\nQuestion:", repr(question))
        print("Answer:", result["answer"][:200])
        print("Sources:", result["sources"])
        print(
            "Knowledge-base topic found:",
            result["sufficient_evidence"],
        )
