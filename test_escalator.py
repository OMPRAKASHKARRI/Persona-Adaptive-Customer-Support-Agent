from src.escalator import (
    should_escalate,
    generate_handoff_summary
)

status, reason = should_escalate(
    "I want a refund immediately",
    0.80
)

print(status)
print(reason)

print(
    generate_handoff_summary(
        "Frustrated User",
        "Refund request",
        ["Customer requested refund"],
        ["billing_policy.txt"],
        ["Reviewed billing policy"]
    )
)