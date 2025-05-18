import chainlit as cl


# @cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hello! How can I help you?").send()
