from document_loader import load_documents
from embedding_service import EmbeddingService
from vector_store import VectorStore


def main():

    # 1. Load and chunk documents
    documents = load_documents()

    print(f"Loaded {len(documents)} chunks")

    # 2. Extract chunk text
    texts = [
        document["content"]
        for document in documents
    ]

    # 3. Create embedding service
    embedding_service = EmbeddingService(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Generate embeddings
    print("Generating embeddings...")

    embeddings = embedding_service.embed_documents(
        texts
    )

    print("Embeddings generated")

    # 5. Create vector store
    vector_store = VectorStore()

    # 6. Store documents + embeddings
    vector_store.upsert_documents(
        documents,
        embeddings
    )

    # 7. Verify
    print(
        f"Vector store contains "
        f"{vector_store.count()} chunks"
    )


if __name__ == "__main__":
    main()