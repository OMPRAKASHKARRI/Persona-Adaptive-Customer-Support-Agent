import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def fallback_response(
    persona,
    user_query,
    context
):

    if persona == "Technical Expert":

        return f"""
Technical Expert Response

Relevant Context:
{context[:500]}

Root Cause:
Please review the retrieved documentation.

Recommended Actions:
1. Review logs
2. Validate configuration
3. Follow troubleshooting steps
4. Escalate if issue persists
"""

    elif persona == "Business Executive":

        return f"""
Business Executive Response

Issue Summary:
{user_query}

Business Impact:
Potential operational disruption if unresolved.

Recommendation:
Review support documentation and assign to support team for further investigation.

Expected Resolution:
Dependent on support team review.
"""

    else:

        return f"""
I understand this issue may be frustrating.

Based on our documentation:

{context[:500]}

Recommended Actions:
1. Follow the documented troubleshooting steps.
2. Retry the operation.
3. Contact support if the issue continues.

We are here to help.
"""


def generate_response(
    user_query,
    persona,
    retrieved_docs
):

    context = "\n\n".join(retrieved_docs)

    if persona == "Technical Expert":

        persona_prompt = """
You are a Senior Technical Support Engineer.

Response Requirements:
- Root Cause Analysis
- Technical Explanation
- Step-by-step Troubleshooting
- Configuration Guidance

Be detailed and technical.
Only use the provided context.
Do not invent information.
"""

    elif persona == "Frustrated User":

        persona_prompt = """
You are an empathetic customer support specialist.

Response Requirements:
- Start with empathy
- Use simple language
- Reassure the customer
- Provide action-oriented steps

Only use the provided context.
Do not invent information.
"""

    else:

        persona_prompt = """
You are a business support manager.

Response Requirements:
- Focus on business impact
- Keep response concise
- Mention expected resolution guidance
- Avoid excessive technical jargon

Only use the provided context.
Do not invent information.
"""

    prompt = f"""
{persona_prompt}

SUPPORT KNOWLEDGE BASE:

{context}

CUSTOMER QUESTION:

{user_query}

Generate a response using only the provided knowledge base content.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800
        )

        result = response.choices[0].message.content

        print("Groq response generated successfully")

        return result.strip()

    except Exception as e:

        print(f"Groq Generator Error: {e}")
        print("Using fallback response...")

        return fallback_response(
            persona,
            user_query,
            context
        )