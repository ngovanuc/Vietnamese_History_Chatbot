import chainlit as cl


# @cl.on_audio_end
async def on_audio_end():
    cl.user_session.set("realtime_chat", False)
    print("[LOG] The user stopped speaking!")