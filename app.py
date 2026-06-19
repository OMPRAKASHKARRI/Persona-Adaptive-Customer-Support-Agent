import streamlit as st

from src.classifier import detect_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff_summary
)

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    layout="wide"
)

st.title(
    "🤖 Persona-Adaptive Customer Support Agent"
)

rag = RAGPipeline()

if "indexed" not in st.session_state:

    rag.ingest_documents()

    st.session_state.indexed = True

query = st.text_area(
    "Enter Customer Message"
)

if st.button("Generate Response"):

    if query:

        persona_result = detect_persona(
            query
        )

        persona = persona_result["persona"]

        retrieval = rag.retrieve(
            query
        )

        docs = retrieval["documents"][0]

        sources = []

        for meta in retrieval["metadatas"][0]:

            sources.append(
                meta["source"]
            )

        response = generate_response(
            query,
            persona,
            docs
        )

        score = 1 - retrieval["distances"][0][0]

        escalated, reason = should_escalate(
            query,
            score
        )

        st.subheader(
            "Detected Persona"
        )

        st.write(persona)

        st.subheader(
            "Retrieved Sources"
        )

        st.write(sources)

        st.subheader(
            "Response"
        )

        st.write(response)

        st.subheader(
            "Escalation Status"
        )

        st.write(
            escalated,
            reason
        )

        if escalated:

            handoff = generate_handoff_summary(
                persona,
                query,
                [query],
                sources,
                ["Knowledge Base Review"]
            )

            st.subheader(
                "Human Handoff Summary"
            )

            st.json(handoff)