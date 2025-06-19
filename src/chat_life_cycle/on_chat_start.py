import uuid
from pymongo import MongoClient
import chainlit as cl

from src.commands.commands import commands

from qdrant_client import QdrantClient
from qdrant_client import models

from src.memory_buffer import retrieval_information
from src.memory_buffer.retrieval_information import collection_name
from src.memory_buffer.retrieval_information import qdrant_client
from src.memory_buffer.retrieval_information import connect_qdrant_client
from src.memory_buffer.retrieval_information import embedding_model
from src.chat_settings.chat_settings import chat_settings

from src.memory_buffer.define_schema_extraction import SchemaExtractionQuestion

# @cl.on_chat_start
async def on_chat_start():
    print("[LOG] The user connected!")
    await cl.ChatSettings(chat_settings).send()
    await cl.context.emitter.set_commands(commands)
    print("[LOG] Initializing chat setting... Done!")
    print("Chat settings: ", cl.user_session.get("chat_settings"))

    cl.user_session.set("count_chat", 0)
    cl.user_session.set("realtime_chat", False)
    
    # Connect tới Qdrant và khởi tạo collection để embedding file được tải lên từ người dùng
    print("[LOG] Connecting to Qdrant and create a new collection...")
    qdrant_client = QdrantClient(url="http://localhost:6333")
    # Lấy ID đoạn chat làm tên của vector database (id ngoài: dựa vào uuid4())
    collection_name = uuid.uuid4()
    cl.user_session.set("id_conversation", str(collection_name))
    cl.user_session.set("collection_name", str(collection_name))
    # Khởi tạo collection mới
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=embedding_model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )
    cl.user_session.set("qdrant_client", qdrant_client)
    cl.user_session.set("max_length_ids_vector_database", 0)
    cl.user_session.set("files", None) # Files for RAG command
    print("[LOG] Init collection for new conversation... Done!")

    cl.user_session.set("summary_of_history_conversation", "")

    user_information = SchemaExtractionQuestion(
        name=None,
        age_group=None,
        language=None,
        level=None,
        tone_preference=None,
        current_emotion=None,
        current_topic=None,
        interested_characters=[],
        emotional_expression=None,
        relative_question=None,
        keywords=[],
        question_summary=None
    )
    cl.user_session.set("user_information", user_information)
    # Set user session parameters
    # cl.user_session.set("history_chat", []) -> cl.chat_context.messages

    # cl.user_session.set("user_name", id_user) -> được đặt sau khi đăng nhập thành công
    # cl.user_session.set("id_user", id_user) -> được đặt sau khi đăng nhập thành công
