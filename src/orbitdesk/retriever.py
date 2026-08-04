from sentence_transformers import SentenceTransformer
from loader import load_documents
from chunker import chunk_document
import numpy as np


# 1. Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# 2. Load all documents
documents = load_documents()


# 3. Convert documents into chunks
all_chunks = []

for document in documents:
    chunks = chunk_document(document)
    all_chunks.extend(chunks)


# 4. Extract text from chunks
passages = [chunk["passage"] for chunk in all_chunks]


# 5. Create embeddings for all chunks
embeddings = model.encode(
    passages,
    normalize_embeddings=True
)


def retrieve(question, top_k=3):

    # Convert user's question into an embedding
    question_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    # Calculate similarity
    scores = np.dot(embeddings, question_embedding)

    # Get highest scoring chunks
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "document_id": all_chunks[index]["document_id"],
            "passage": all_chunks[index]["passage"],
            "score": float(scores[index])
        })

    return results


if __name__ == "__main__":

    question = "Why did my scheduled export fail?"

    results = retrieve(question)

    print("\nQuestion:", question)

    for result in results:
        print("\nDocument:", result["document_id"])
        print("Score:", result["score"])
        print("Passage:", result["passage"][:500])