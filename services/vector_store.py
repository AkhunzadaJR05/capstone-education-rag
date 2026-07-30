from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

COLLECTION_NAME = "documents"
EMBEDDING_DIM = 384

client = QdrantClient(":memory:")


def ensure_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def search_chunks(query_vector: list[float], room_id: int, top_k: int = 5) -> list[dict]:
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=Filter(
            must=[FieldCondition(key="room_id", match=MatchValue(value=room_id))]
        ),
        limit=top_k,
    ).points

    return [
        {
            "filename": r.payload["filename"],
            "file_type": r.payload["file_type"],
            "chunk_index": r.payload["chunk_index"],
            "text": r.payload["text"],
        }
        for r in results
    ]