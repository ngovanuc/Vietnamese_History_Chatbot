import chainlit as cl

from src.chat_with.default.default import chat_with_default
from src.chat_with.cohere.command_a_03_2025 import chat_with_command_a_03_2025
from src.chat_with.groq.llama3_70b_8192 import chat_with_llama3_70b_8192
from src.chat_with.google.gemini_20_flash import chat_with_gemini_20_flash
from src.chat_with.anthropic.claude_3_7_sonnet_20250219 import chat_with_claude_3_7_sonnet_20250219


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
    elif current_model_name == "gemini-2.0-flash":
        model = chat_with_gemini_20_flash(streaming=streaming, temperature=temperature)
        return model
    elif current_model_name == "claude-3-7-sonnet-20250219":
        model = chat_with_claude_3_7_sonnet_20250219(streaming=streaming, temperature=temperature)
        return model
    elif current_model_name == "gpt-3.5-turbo (alpha)":
        model = chat_with_default(temperature=temperature, streaming=streaming)
        return model
    else:
        model = chat_with_default(temperature=temperature, streaming=streaming)
        return model
