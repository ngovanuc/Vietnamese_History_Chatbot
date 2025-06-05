import chainlit as cl

from src.chat_life_cycle.realtime_chat.on_audio_end import on_audio_end


# @cl.on_chat_end
def on_chat_end():
    print("[LOG] The user disconnected!")
    # Ghi log
    # Logic code here!