import json

SENSITIVE_KEYWORDS = [
    "refund",
    "billing",
    "chargeback",
    "legal",
    "lawsuit",
    "account deletion"
]


def should_escalate(
    query,
    retrieval_score,
    frustration_count=0
):

    query_lower = query.lower()

    for keyword in SENSITIVE_KEYWORDS:

        if keyword in query_lower:

            return True, "Sensitive Issue"

    if retrieval_score < 0.45:

        return True, "Low Retrieval Confidence"

    if frustration_count >= 2:

        return True, "Repeated Dissatisfaction"

    return False, "No Escalation"


def generate_handoff_summary(
    persona,
    user_query,
    conversation_history,
    documents_used,
    attempted_steps
):

    summary = {
        "persona": persona,
        "issue": user_query,
        "conversation_history": conversation_history,
        "documents_used": documents_used,
        "attempted_steps": attempted_steps,
        "recommended_next_steps":
            "Human support agent should review and continue investigation."
    }

    return json.dumps(
        summary,
        indent=4
    )