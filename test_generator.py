from src.generator import generate_response

docs = [
    """
A 401 Unauthorized response indicates authentication failure.

Possible causes:
- Invalid API key
- Expired token
- Incorrect Authorization header

Troubleshooting:
1. Verify API credentials.
2. Confirm token validity.
3. Generate a new token if expired.
"""
]

response = generate_response(
    "Can you explain why my API authentication returns 401?",
    "Technical Expert",
    docs
)

print(response)