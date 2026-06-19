from src.generator import generate_response

docs = [
"""
A 401 Unauthorized response indicates authentication failure.

Possible causes:

- Invalid API key
- Expired token

Troubleshooting:

1. Verify API credentials.
2. Confirm token validity.
3. Generate a new token if expired.
"""
]

response = generate_response(
    "Why am I getting 401 Unauthorized?",
    "Technical Expert",
    docs
)

print(response)