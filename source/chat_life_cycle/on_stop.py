import chainlit as cl


# @cl.on_stop
def on_stop():
    print("[LOG] The user stopped generating!")