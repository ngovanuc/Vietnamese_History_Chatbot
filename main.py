import chainlit as cl

# from source.starters.starters import init_starters
from source.chat_life_cycle.on_chat_start import on_chat_start
# from source.chat_life_cycle.on_chat_end import on_chat_end


# cl.on_chat_start(init_starters)
cl.on_chat_start(on_chat_start)
# cl.on_chat_end(on_chat_end)