from qdrant_client import QdrantClient
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

COLLECTION_NAME = "bible_verses"

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

hf_client = InferenceClient(
    api_key=os.getenv("HF_ACCESS_TOKEN")
)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding(text: str):
    try:
        embedding = hf_client.feature_extraction(
            text,
            model=EMBEDDING_MODEL,
        )

        embedding = np.array(embedding)
        norm = np.linalg.norm(embedding)

        if norm == 0:
            return None

        return (embedding / norm).tolist()

    except Exception:
        return None


def retrieve(query: str, limit: int = 10):
    try:
        embedding = get_embedding(query)

        if embedding is None:
            return []

        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            limit=limit,
        )

        return results.points if results and results.points else []

    except Exception:
        return []