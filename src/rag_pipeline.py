import os

from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

import chromadb

from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K
)


class RAGPipeline:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="support_kb"
        )

    def get_embedding(self, text):

        return self.embedding_model.encode(
            text
        ).tolist()

    def load_documents(self, data_folder="data"):

        documents = []

        for filename in os.listdir(data_folder):

            filepath = os.path.join(
                data_folder,
                filename
            )

            # Handle Markdown and TXT files
            if filename.endswith(".md") or filename.endswith(".txt"):

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as f:

                    documents.append({
                        "source": filename,
                        "text": f.read()
                    })

            # Handle PDF files
            elif filename.endswith(".pdf"):

                try:

                    if os.path.getsize(filepath) == 0:
                        print(f"Skipping empty PDF: {filename}")
                        continue

                    reader = PdfReader(filepath)

                    text = ""

                    for page_num, page in enumerate(reader.pages):

                        extracted = page.extract_text()

                        if extracted:
                            text += extracted + "\n"

                    documents.append({
                        "source": filename,
                        "text": text
                    })

                except Exception as e:

                    print(
                        f"Error reading PDF {filename}: {e}"
                    )

        return documents

    def ingest_documents(self):

        docs = self.load_documents()

        print(
            f"Loaded {len(docs)} documents"
        )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        total_chunks = 0

        for doc in docs:

            chunks = splitter.split_text(
                doc["text"]
            )

            for idx, chunk in enumerate(chunks):

                embedding = self.get_embedding(
                    chunk
                )

                self.collection.add(
                    ids=[
                        f"{doc['source']}_{idx}"
                    ],
                    embeddings=[
                        embedding
                    ],
                    documents=[
                        chunk
                    ],
                    metadatas=[
                        {
                            "source": doc["source"],
                            "section": f"chunk_{idx}"
                        }
                    ]
                )

                total_chunks += 1

        print(
            f"Indexed {total_chunks} chunks successfully."
        )

    def retrieve(self, query):

        query_embedding = self.get_embedding(
            query
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=TOP_K
        )

        return results