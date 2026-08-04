from pathlib import Path


def load_documents():
    knowledge_path = Path("data/knowledge_base")

    documents = []

    for file_path in knowledge_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "document_id": file_path.stem,
            "content": content
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print(document["document_id"])