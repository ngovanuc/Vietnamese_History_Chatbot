import chainlit as cl
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from src.memory_buffer.retrieval_information import embedding_model
from src.memory_buffer.retrieval_information import qdrant_client


def retriever(collection_name, query, top_k=1):
    print("[LOG] Retrieving information from Qdrant...")
    try:
        embeded_query = embedding_model.encode(query).tolist()
        results = qdrant_client.query_points(
            collection_name=collection_name,
            query=embeded_query,
            limit=top_k,
        ).points
        return results
    except Exception as e:
        print("[LOG] Error while retrieving information! Error: ", e)
        return ""
