from classifier import classify_question
from retriever import retrieve
from llm import generate_answer


def answer_question(question):
    classification = classify_question(question)

    # 1. Out of scope
    if classification == "out_of_scope":
        return {
            "classification": "out_of_scope",
            "answer": "This request is outside the available OrbitDesk support knowledge base.",
            "sources": [],
            "confidence": 1.0,
            "requires_human": False,
            "reason": "Question contains topics outside OrbitDesk support scope (legal, medical, financial, or unrelated).",
            "clarification_question": None,
            "warnings": []
        }

    # 2. Needs clarification
    if classification == "requires_clarification":
        return {
            "classification": "requires_clarification",
            "answer": "I need more information to help you.",
            "sources": [],
            "confidence": 0.0,
            "requires_human": False,
            "reason": "Question lacks specific symptoms, error codes, or object identifiers needed for documented troubleshooting.",
            "clarification_question": "Please provide the specific error code, connection/schedule ID, and what you observed.",
            "warnings": []
        }

    # 3. Retrieve evidence
    evidence = retrieve(question, top_k=5)

    # If no good evidence found, safe failure
    if not evidence or evidence[0]["score"] < 0.25:
        return {
            "classification": "safe_failure",
            "answer": "I could not find sufficient documented information to answer this safely. Please provide more details or contact support.",
            "sources": [],
            "confidence": 0.0,
            "requires_human": False,
            "reason": "Retrieved evidence scores were too low to provide a confident answer.",
            "clarification_question": "Can you provide the specific error code, workspace ID, or object ID involved?",
            "warnings": []
        }

    # 4. Generate answer via LLM
    result = generate_answer(question, evidence, classification)

    # 5. Override classification if pipeline detected escalation
    if classification == "requires_escalation":
        result["classification"] = "requires_escalation"
        result["requires_human"] = True
        if not result.get("reason"):
            result["reason"] = "This request requires elevated permission or human approval."

    return result


if __name__ == "__main__":
    question = "My sync is not working"
    print(answer_question(question))