import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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

{context[:400]}

Recommended Actions:

1. Review logs
2. Validate configuration
3. Follow troubleshooting steps in documentation
"""

    elif persona == "Business Executive":

        return f"""
Business Executive Response

Issue Summary:
{user_query}

Business Impact:
Potential operational disruption.

Recommendation:
Review the retrieved support documentation and assign to the support team if unresolved.
"""

    else:

        return f"""
I understand this issue may be frustrating.

Based on our documentation:

{context[:400]}

Please follow the recommended troubleshooting steps. If the issue persists, we will escalate it to a support specialist.
"""


def generate_response(
    user_query,
    persona,
    retrieved_docs
):

    context = "\n\n".join(retrieved_docs)

    try:

        if persona == "Technical Expert":

            persona_prompt = """
You are a Senior Technical Support Engineer.

Provide:
- Root Cause
- Technical Explanation
- Troubleshooting Steps
"""

        elif persona == "Frustrated User":

            persona_prompt = """
You are an empathetic support specialist.

Use empathy and simple language.
"""

        else:

            persona_prompt = """
You are a business support manager.

Focus on business impact and timelines.
"""

        prompt = f"""
{persona_prompt}

CONTEXT:
{context}

QUESTION:
{user_query}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print(f"Gemini Generator Error: {e}")
        print("Using fallback response...")

        return fallback_response(
            persona,
            user_query,
            context
        )