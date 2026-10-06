from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        vector = self.model.encode(text, normalize_embeddings=True)

        return vector.tolist()

    def embed_documents(self, text: List[str]) -> List[List[float]]:
        vectors = self.model.encode(text, normalize_embeddings=True)

        return vectors.tolist()

    
