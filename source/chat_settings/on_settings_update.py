import chainlit as cl


# @cl.on_settings_update
async def update_settings(chat_settings):
    # cl.user_session.set("chat_settings", chat_settings)
    print(f"[LOG] User chat settings has been updated: \n{chat_settings}")
