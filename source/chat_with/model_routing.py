import chainlit as cl

from source.chat_with.default.default import chat_with_default
from source.chat_with.cohere.command_a_03_2025 import chat_with_command_a_03_2025
from source.chat_with.groq.llama3_70b_8192 import chat_with_llama3_70b_8192


def model_routing():
    current_model_name = cl.user_session.get("chat_settings")["Model"]
    streaming = cl.user_session.get("chat_settings")["Streaming"]
    temperature = cl.user_session.get("chat_settings")["Temperature"]

    if current_model_name == "command-a-03-2025":
        model = chat_with_command_a_03_2025(streaming=streaming, temperature=temperature)
        return model
    elif current_model_name == "llama3-70b-8192":
        model = chat_with_llama3_70b_8192(streaming=streaming, temperature=temperature)
        return model
    elif current_model_name == "gpt-3.5-turbo (alpha)":
        model = chat_with_default(temperature=temperature, streaming=streaming)
        return model
    elif current_model_name == "insert_any_model_used":
        model = chat_with_default(temperature=temperature, streaming=streaming)
        return model
    else:
        model = chat_with_default(temperature=temperature, streaming=streaming)
        return model
