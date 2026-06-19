# API Authentication Guide

A 401 Unauthorized response indicates authentication failure.

Possible causes:

- Invalid API key
- Expired token
- Incorrect Authorization header

Required Header Format:

Authorization: Bearer <TOKEN>

Troubleshooting:

1. Verify API credentials.
2. Confirm token validity.
3. Generate a new token if expired.
4. Retry the request.