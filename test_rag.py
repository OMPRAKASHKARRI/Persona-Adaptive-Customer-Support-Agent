from src.rag_pipeline import RAGPipeline

rag = RAGPipeline()

rag.ingest_documents()

results = rag.retrieve(
    "How do I fix API authentication errors?"
)

print(results)