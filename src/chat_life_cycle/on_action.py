import chainlit as cl


# @cl.action_callback
async def on_action(action: cl.Action):
    print(action.payload)