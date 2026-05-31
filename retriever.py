from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

COLLECTION_NAME = "bible_verses"

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def retrieve(query: str, limit: int = 10):
    embedding = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit,
    )

    return results.points