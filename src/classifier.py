import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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
- timelines
- operations

Return JSON only:

{{
    "persona":"",
    "confidence":0.0,
    "reasoning":""
}}

Message:
{user_message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        cleaned_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned_text)

    except Exception as e:

        print(f"Gemini Error: {e}")
        print("Using fallback classifier...")

        return fallback_persona(user_message)