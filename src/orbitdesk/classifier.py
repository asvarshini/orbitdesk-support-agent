def classify_question(question):
    question = question.lower()

    clarification_words = [
        "not working",
        "doesn't work",
        "issue",
        "problem",
        "failed"
    ]

    unsupported_words = [
        "refund",
        "cancel subscription",
        "legal",
        "medical",
        "payment"
    ]

    if any(word in question for word in unsupported_words):
        return "NOT_ANSWERABLE"

    if any(word in question for word in clarification_words):
        return "CLARIFICATION"

    return "ANSWERABLE"


if __name__ == "__main__":

    questions = [
        "Why did my scheduled export fail?",
        "My export is not working",
        "Can you refund my subscription?"
    ]

    for question in questions:
        result = classify_question(question)

        print("\nQuestion:", question)
        print("Classification:", result)