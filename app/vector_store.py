import os
import chromadb
from typing import List, Dict


class VectorStore:

    def __init__(
        self,
        collection_name: str = "support_documents"
    ):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        vector_db_path = os.path.join(
            base_dir,
            "..",
            "data",
            "vector_db"
        )

        self.client = chromadb.PersistentClient(
            path=vector_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine"
                }
            }
        )

    def upsert_documents(
        self,
        documents: List[Dict],
        embeddings: List[List[float]]
    ):
        ids = [
            document["chunk_id"]
            for document in documents
        ]

        contents = [
            document["content"]
            for document in documents
        ]

        metadata = [
            document["metadata"]
            for document in documents
        ]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadata
        )

    def search(self, query_embedding: List[float], top_k: int = 3, 
               max_distance: float | None = None) -> List[Dict]:
        
        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        retrieved_documents = []

        for index in range(len(results["ids"][0])):

            distance = results["distances"][0][index]

            if(max_distance is not None and distance > max_distance):
                continue

            retrieved_documents.append({
                "chunk_id": results["ids"][0][index],
                "content": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": distance
            })

        return retrieved_documents

    def count(self) -> int:
        return self.collection.count()