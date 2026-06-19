import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def fallback_persona(user_message):

    text = user_message.lower()

    technical_keywords = [
        "api",
        "401",
        "logs",
        "authentication",
        "endpoint",
        "configuration",
        "database",
        "integration",
        "error"
    ]

    executive_keywords = [
        "business",
        "operations",
        "impact",
        "timeline",
        "roi",
        "executive",
        "revenue"
    ]

    if any(word in text for word in technical_keywords):

        return {
            "persona": "Technical Expert",
            "confidence": 0.50,
            "reasoning": "Rule-based fallback"
        }

    if any(word in text for word in executive_keywords):

        return {
            "persona": "Business Executive",
            "confidence": 0.50,
            "reasoning": "Rule-based fallback"
        }

    return {
        "persona": "Frustrated User",
        "confidence": 0.50,
        "reasoning": "Rule-based fallback"
    }


def detect_persona(user_message):

    prompt = f"""
Classify the user into exactly one persona.

Technical Expert:
- APIs
- logs
- configurations
- debugging

Frustrated User:
- emotional
- angry
- urgent

Business Executive:
- business impact
- operations
- timelines
- revenue
- executive reporting
- risk assessment
- customer impact
IMPORTANT:

If the message discusses:
- business impact
- operational impact
- timelines
- revenue
- outcomes

then classify as Business Executive.

Return ONLY valid JSON.

Example:

{{
    "persona":"Technical Expert",
    "confidence":0.95,
    "reasoning":"Uses API authentication terminology"
}}

Message:
{user_message}
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
            temperature=0
        )

        result = response.choices[0].message.content

        cleaned_text = (
            result
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        print("Groq persona classification successful")

        return json.loads(cleaned_text)

    except Exception as e:

        print(f"Groq Error: {e}")
        print("Using fallback classifier...")

        return fallback_persona(user_message)