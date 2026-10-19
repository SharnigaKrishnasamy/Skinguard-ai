import csv
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent
METADATA_FILE = KB_DIR / "metadata.csv"


def load_knowledge_base():
    knowledge_base = {}

    with METADATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            class_code = row["class_code"].strip().lower()
            document_path = KB_DIR / row["document_file"]

            if not document_path.is_file():
                raise FileNotFoundError(
                    f"Knowledge-base document not found: {document_path}"
                )

            content = document_path.read_text(encoding="utf-8-sig")

            knowledge_base[class_code] = {
                "title": row["title"].strip(),
                "content": content,
                "source_url": row["source_url"].strip(),
                "source_type": row["source_type"].strip(),
            }

    return knowledge_base


if __name__ == "__main__":
    kb = load_knowledge_base()
    print(f"Loaded {len(kb)} knowledge-base documents.")

    for class_code, document in kb.items():
        print(f"- {class_code}: {document['title']}")
