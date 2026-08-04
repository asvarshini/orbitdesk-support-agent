def classify_question(question):
    question = question.lower().strip()

    # Requests that are explicitly outside OrbitDesk support
    unsupported_words = [
        "refund",
        "cancel subscription",
        "legal",
        "medical",
        "payment",
        "invest",
        "investment",
        "stock",
        "stocks",
        "crypto",
        "cryptocurrency",
        "weather",
        "recipe",
        "travel",
        "movie",
        "music"
    ]

    if any(word in question for word in unsupported_words):
        return "NOT_ANSWERABLE"

    # OrbitDesk topics covered by the knowledge base
    orbitdesk_words = [
        "orbitdesk",
        "workspace",
        "dashboard",
        "export",
        "schedule",
        "connection",
        "refresh",
        "sync",
        "api",
        "credential",
        "token",
        "role",
        "owner",
        "admin",
        "analyst",
        "viewer",
        "permission",
        "timezone",
        "audit",
        "destination",
        "email",
        "storage",
        "integration",
        "run history"
    ]

    # If the question is clearly about OrbitDesk,
    # continue to clarification/answerable checks.
    is_orbitdesk_question = any(
        word in question for word in orbitdesk_words
    )

    # Vague OrbitDesk problems need clarification
    clarification_words = [
        "not working",
        "doesn't work",
        "issue",
        "problem",
        "failed"
    ]

    if is_orbitdesk_question and any(
        word in question for word in clarification_words
    ):
        return "CLARIFICATION"

    # Questions outside the documented OrbitDesk domain
    if not is_orbitdesk_question:
        return "NOT_ANSWERABLE"

    return "ANSWERABLE"


if __name__ == "__main__":

    questions = [
        "Why did my scheduled export fail?",
        "My export is not working",
        "Can you refund my subscription?",
        "How can I invest my money?",
        "Who can create an API credential?",
        "My sync is not working"
    ]

    for question in questions:
        result = classify_question(question)

        print("\nQuestion:", question)
        print("Classification:", result)