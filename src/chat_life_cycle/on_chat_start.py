import chainlit as cl

from src.chat_settings.chat_settings import chat_settings

# @cl.on_chat_start
async def on_chat_start():
    print("[LOG] The user connected!")
    print("[LOG] Initializing chat setting...")
    await cl.ChatSettings(chat_settings).send()
    print("[LOG] New chat setting initialized!")
    print("chat setting: ", cl.user_session.get("chat_setting"))    