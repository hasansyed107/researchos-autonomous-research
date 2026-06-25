import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
)

from tools.embeddings import embed_chunks

# Create storage directory
QDRANT_PATH = "./qdrant_data"
COLLECTION_NAME = "research_docs"

os.makedirs(QDRANT_PATH, exist_ok=True)

_client = None


def get_qdrant_client():
    global _client

    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)

    return _client


def ensure_collection():
    client = get_qdrant_client()

    collections = client.get_collections()
    existing = [c.name for c in collections.collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def store_chunks(chunks):
    if not chunks:
        return

    ensure_collection()
    client = get_qdrant_client()

    vectors = embed_chunks(chunks)
    points = []

    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={"text": chunk},
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def retrieve_chunks(query, limit=5):
    ensure_collection()
    client = get_qdrant_client()

    query_vector = embed_chunks([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=limit,
    )

    return [
        point.payload["text"]
        for point in results.points
    ]