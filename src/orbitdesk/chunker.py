import re
from loader import load_documents


def chunk_document(document, chunk_size=500):
    content = document["content"]

    # Get the KB document ID from the front matter
    match = re.search(r"document_id:\s*(KB-\d+)", content)

    if match:
        document_id = match.group(1)
    else:
        document_id = document["document_id"]

    words = content.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])

        chunks.append({
            "document_id": document_id,
            "passage": chunk_text
        })

    return chunks


if __name__ == "__main__":
    documents = load_documents()

    chunks = chunk_document(documents[0])

    print("Document:", chunks[0]["document_id"])
    print("Number of chunks:", len(chunks))
    print("\nFirst chunk:")
    print(chunks[0]["passage"])