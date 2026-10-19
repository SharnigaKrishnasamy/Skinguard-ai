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

            content = document_path.read_text(encoding="utf-8-sig").strip()

            if not content:
                raise ValueError(
                    f"Knowledge-base document is empty: {document_path}"
                )

            document = {
                "title": row["title"].strip(),
                "content": content,
                "source_url": row["source_url"].strip(),
                "source_type": row["source_type"].strip(),
            }

            if class_code not in knowledge_base:
                knowledge_base[class_code] = {
                    **document,
                    "documents": [],
                }

            knowledge_base[class_code]["documents"].append(document)

    # Keep the original single-document fields for compatibility.
    # Combine all document content so existing RAG calls can use every source.
    for class_code, entry in knowledge_base.items():
        entry["content"] = "\n\n--- Additional source ---\n\n".join(
            document["content"] for document in entry["documents"]
        )

    return knowledge_base


if __name__ == "__main__":
    kb = load_knowledge_base()
    print(f"Loaded {sum(len(v['documents']) for v in kb.values())} documents.")
    print(f"Across {len(kb)} skin-lesion classes.")

    for class_code, entry in kb.items():
        print(f"- {class_code}: {len(entry['documents'])} document(s)")