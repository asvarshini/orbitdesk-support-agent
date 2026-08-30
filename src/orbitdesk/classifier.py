def classify_question(question):
    question_lower = question.lower().strip()

    # OUT OF SCOPE: legal, medical, financial, or unrelated topics
    out_of_scope_words = [
        "legal advice", "medical", "lawyer", "sue", "court",
        "invest my money", "stock price", "crypto", "weather",
        "recipe", "travel booking", "movie", "music", "sports"
    ]
    if any(word in question_lower for word in out_of_scope_words):
        return "out_of_scope"

    # ESCALATION: actions the assistant cannot perform
    escalation_actions = [
        "create a credential", "create an api", "generate a token",
        "give me a token", "reveal the secret", "show me the secret",
        "reset my password", "change my role", "change the workspace",
        "execute the export", "run the export for me", "start the refresh",
        "contact the recipient", "contact the provider",
        "issue a refund", "process a refund", "cancel my subscription",
        "billing dispute", "ownership dispute"
    ]
    if any(action in question_lower for action in escalation_actions):
        return "requires_escalation"

    # ESCALATION: specific symptoms that require human team
    if any(x in question_lower for x in [
        "two consecutive render_failed",
        "two repeated connector_internal_error",
        "credential exposed", "secret exposed", "suspected exposure"
    ]):
        return "requires_escalation"

    # Is this even about OrbitDesk?
    orbitdesk_words = [
        "orbitdesk", "workspace", "dashboard", "export", "schedule",
        "connection", "refresh", "sync", "api", "credential", "token",
        "role", "owner", "admin", "analyst", "viewer", "permission",
        "timezone", "audit", "destination", "email", "storage",
        "run history", "render_failed", "timeout", "unverified", "revoked"
    ]
    is_orbitdesk = any(word in question_lower for word in orbitdesk_words)

    if not is_orbitdesk:
        return "out_of_scope"

    # CLARIFICATION: too vague to diagnose
    vague = ["not working", "doesn't work", "broken", "sync is not working"]
    has_details = any(x in question_lower for x in [
        "error", "code", "timeout", "unverified", "revoked", "render_failed",
        "source_refresh_timeout", "destination_unverified",
        "connector_internal_error", "kb-", "case-", "workspace id"
    ])
    if any(v in question_lower for v in vague) and not has_details:
        return "requires_clarification"

    return "answerable"


if __name__ == "__main__":
    test_questions = [
        "Why did my scheduled export fail?",
        "My export is not working",
        "Can you refund my subscription?",
        "Who can create an API credential?",
        "My sync is not working",
        "Two consecutive render_failed after checks"
    ]
    for q in test_questions:
        print(f"\nQuestion: {q}")
        print("Classification:", classify_question(q))