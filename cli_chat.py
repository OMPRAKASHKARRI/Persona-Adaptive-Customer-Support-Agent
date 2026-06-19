from src.classifier import detect_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff_summary
)

rag = RAGPipeline()

print("Indexing documents...")
rag.ingest_documents()

print("\n===================================")
print("Persona-Adaptive Customer Support Agent")
print("Type 'exit' to quit")
print("===================================\n")

while True:

    query = input("Customer: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    try:

        persona_result = detect_persona(query)

        persona = persona_result["persona"]

        retrieval = rag.retrieve(query)

        docs = retrieval["documents"][0]

        sources = [
            meta["source"]
            for meta in retrieval["metadatas"][0]
        ]

        score = 1 - retrieval["distances"][0][0]

        response = generate_response(
            query,
            persona,
            docs
        )

        escalated, reason = should_escalate(
            query,
            score
        )

        print("\n-----------------------------------")
        print(f"Detected Persona: {persona}")
        print(f"Sources: {sources}")

        print("\nResponse:\n")
        print(response)

        print("\nEscalation Status:")
        print(f"{escalated} ({reason})")

        if escalated:

            handoff = generate_handoff_summary(
                persona,
                query,
                [query],
                sources,
                ["Knowledge Base Review"]
            )

            print("\nHuman Handoff Summary:")
            print(handoff)

        print("-----------------------------------\n")

    except Exception as e:

        print("\nUnexpected Error:")
        print(e)

        print("\nContinuing chatbot...\n")