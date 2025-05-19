from typing import Dict
from typing import Dict

import chainlit as cl

from src.starters.set_starters import set_starters
from src.chat_settings.on_settings_update import update_settings
from src.chat_life_cycle.on_chat_start import on_chat_start
from src.chat_life_cycle.on_message.on_message import on_message
from src.chat_life_cycle.on_audio_chunk import on_audio_chunk
from src.chat_life_cycle.on_audio_end import on_audio_end
from src.chat_life_cycle.on_stop import on_stop
from src.chat_life_cycle.on_action import on_action
from src.chat_life_cycle.on_chat_end import on_chat_end
from src.chat_life_cycle.on_loggout import on_logout


cl.set_starters(set_starters)
cl.on_settings_update(update_settings)
cl.on_chat_start(on_chat_start)
cl.on_message(on_message)
cl.on_audio_chunk(on_audio_chunk)
cl.on_audio_end(on_audio_end)
cl.on_stop(on_stop)
cl.action_callback(on_action)
cl.on_chat_end(on_chat_end)
cl.on_logout(on_logout)