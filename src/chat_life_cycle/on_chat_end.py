import chainlit as cl


# @cl.on_chat_end
def on_chat_end():
    print("[LOG] The user disconnected!")
    # Ghi log
    # Logic code here!