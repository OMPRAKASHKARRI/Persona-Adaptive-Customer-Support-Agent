from src.classifier import detect_persona

result = detect_persona(
    "Can you explain why my API authentication returns a 401 error?"
)

print(result)