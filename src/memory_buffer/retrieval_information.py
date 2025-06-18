"""Kết hợp các thông tin câu hỏi trích xuất được và một bản tóm tắt lịch sử cuộc trò chuyện để 
truy xuất các thông tin liên quan trong cơ sở dữ liệu vector database, nhằm bổ sung thông tin trả lời cho chatbot"""

from transformers import AutoTokenizer
from transformers import AutoModel
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer

from qdrant_client import models
from qdrant_client import QdrantClient

from pathlib import Path
import asyncio


current_file = Path(__file__)
root_path = current_file.parent.parent.parent
embedding_model_path = (root_path / "embedding_models" / "vietnamese-bi-encoder").resolve()

collection_name = "vietnamese-bi-encoder"

async def load_embedding_model():
    try:
        print("[LOG] Loading embedding model...")
        model = SentenceTransformer(str(embedding_model_path))
        print("[LOG] Embedding model loaded!")
        print(f"[LOG] Embedding model: {model}")
        return model
    except Exception as e:
        print(f"[LOG] Error while loading embedding model! Error: {e}",)
        return None

async def connect_to_qdrant():
    try:
        print("[LOG] Loading vector database (của dataset về lịch sử)...")
        client = QdrantClient(url="http://localhost:6333")
        if client.collection_exists(collection_name=collection_name):
            collection = client.get_collection(collection_name=collection_name)
            print("[LOG] Connected to Qdant and vector database exist!")
            # return client, collection
            return client
        else:
            print("[LOG] Error while connecting to vector database!")
            return None
    except Exception as e:
        print(f"[LOG] Error while loading vector database! Error: {e}")
        return None

async def connect_qdrant_client():
    print("[LOG] Connecting to Qdrant...")
    client = QdrantClient(url="http://localhost:6333")
    print("[LOG] Connected to Qdant!")
    return client

# embedding_model = asyncio.create_task(load_embedding_model())
# qdrant_client = asyncio.create_task(connect_to_qdrant())
embedding_model = asyncio.run(load_embedding_model())
qdrant_client = asyncio.run(connect_to_qdrant())
# qdrant_client = asyncio.run(connect_qdrant_client())


async def retriever(collection_name: str|None=None, query: str|None=None, top_k: int|None=None):
    """Trích xuất thông tin từ cơ sở dữ liệu vector database.
    
    Inputs:
        query: Câu hỏi trích xuất
        top_k: Số kết quả trích xuất
        
    Ouptuts:
        Danh sách các kết quả liên quan nhất. Trong đó bao gồm payload và chỉ số mức độ liên quan.
        Truy cập vào results: result.payload['embedding_content']}, score: {result.score}
    """
    if not embedding_model or not qdrant_client:
        print(f"[LOG] Embedding model or vector database not loaded yet!")
        # raise Exception("Embedding model or vector database not loaded yet!")
        return None

    if collection_name is None:
        return None
    
    if query is None:
        return None
    
    if top_k is None:
        top_k = 2
    elif top_k > 4 or top_k <= 0:
        top_k = 2

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
        return None
