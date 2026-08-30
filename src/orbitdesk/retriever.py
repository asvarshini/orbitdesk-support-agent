import json
import numpy as np
from sentence_transformers import SentenceTransformer
from loader import load_documents
from chunker import chunk_document

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load KB documents
kb_documents = load_documents()

# Load resolved cases
all_chunks = []

# 1. Chunk KB docs
for doc in kb_documents:
    chunks = chunk_document(doc)
    for chunk in chunks:
        chunk["source_type"] = "kb"
        chunk["outdated"] = False
        all_chunks.append(chunk)

# 2. Load and chunk resolved cases
try:
    with open("data/resolved_cases.json", "r", encoding="utf-8") as f:
        cases_data = json.load(f)
    for case in cases_data.get("cases", []):
        text = f"Case {case['case_id']} (status: {case['status']}): {case['title']}\n"
        text += f"Symptoms: {'; '.join(case.get('symptoms', []))}\n"
        text += f"Resolution: {'; '.join(case.get('resolution', []))}\n"
        if case.get("important_limit"):
            text += f"Limit: {case['important_limit']}\n"
        if case.get("superseded_reason"):
            text += f"Superseded reason: {case['superseded_reason']}\n"
        
        all_chunks.append({
            "document_id": case["case_id"],
            "passage": text,
            "source_type": "case",
            "outdated": case.get("status") == "superseded",
            "case_status": case.get("status")
        })
except FileNotFoundError:
    pass

passages = [chunk["passage"] for chunk in all_chunks]
embeddings = model.encode(passages, normalize_embeddings=True)


def retrieve(question, top_k=5):
    q_embedding = model.encode([question], normalize_embeddings=True)[0]
    scores = np.dot(embeddings, q_embedding)
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        chunk = all_chunks[idx]
        results.append({
            "source_id": chunk["document_id"],
            "passage": chunk["passage"],
            "score": float(scores[idx]),
            "source_type": chunk.get("source_type", "kb"),
            "outdated": chunk.get("outdated", False)
        })
    return results


if __name__ == "__main__":
    q = "Why did my scheduled export fail?"
    for r in retrieve(q):
        print(f"\n{r['source_id']} | {r['source_type']} | score: {r['score']:.3f}")
        print(r["passage"][:300])