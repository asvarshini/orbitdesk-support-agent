from classifier import classify_question
from retriever import retrieve
from llm import generate_answer


def answer_question(question):

    # 1. Classify the question
    classification = classify_question(question)

    print("Classification:", classification)

    # 2. Handle unsupported questions
    if classification == "NOT_ANSWERABLE":
        return {
            "classification": classification,
            "message": "This request is outside the available OrbitDesk support knowledge."
        }

    # 3. Handle unclear questions
    if classification == "CLARIFICATION":
        return {
            "classification": classification,
            "message": "Please provide more details about the problem."
        }

    # 4. Retrieve relevant knowledge
    results = retrieve(question, top_k=3)

    answer = generate_answer(question, results)

    return {
    "classification": classification,
    "answer": answer,
    "evidence": results

    }


if __name__ == "__main__":

    question = "Why did my scheduled export fail?"    
    result = answer_question(question)

    print("\nResult:")
    print(result)