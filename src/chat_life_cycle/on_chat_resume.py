import chainlit as cl
from chainlit.types import ThreadDict

from src.chat_settings.chat_settings import chat_settings

# @cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    await cl.ChatSettings(chat_settings).send()
    print("[LOG] Init chat setting for resume conversation... Done!")
    print("[LOG] Conversation resumed!")