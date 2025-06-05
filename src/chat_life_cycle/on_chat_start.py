from pymongo import MongoClient
import chainlit as cl

from src.authentication.password_auth_callback import connect_to_mongo

from src.memory_buffer.retrieval_information import connect_to_qdrant
from src.memory_buffer.retrieval_information import collection_name

from src.chat_settings.chat_settings import chat_settings

# @cl.on_chat_start
async def on_chat_start():
    print("[LOG] The user connected!")
    await cl.ChatSettings(chat_settings).send()
    print("[LOG] Initializing chat setting... Done!")
    print("Chat settings: ", cl.user_session.get("chat_settings"))

    cl.user_session.set("count_chat", 0)
    cl.user_session.set("realtime_chat", False)
    cl.user_session.set("summary_of_history_conversation", None)
    # Set user session parameters
    # cl.user_session.set("history_chat", []) -> cl.chat_context.messages

    # cl.user_session.set("user_name", id_user) -> được đặt sau khi đăng nhập thành công
    # cl.user_session.set("id_user", id_user) -> được đặt sau khi đăng nhập thành công
