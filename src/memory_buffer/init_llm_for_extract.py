from src.llms.cohere import command_a_03_2025
from src.llms.mistral import mistral_large_latest
from src.llms.google import gemini_20_flash
from src.llms.groq import llama3_70b_8192
from src.llms.anthropic import claude_3_7_sonnet_20250219

from langchain.chat_models import init_chat_model

import os


def command_a_03_2025_for_extract():
    llm = command_a_03_2025()
    model_name = llm.model_name
    os.environ["COHERE_API_KEY"] = llm.api_key
    llm_provider = init_chat_model(model_name, model_provider="cohere", temperature=0)
    return llm_provider

def mistral_large_latest_for_extract():
    llm = mistral_large_latest()
    model_name = llm.model_name
    os.environ["MISTRAL_API_KEY"] = llm.api_key
    llm_provider = init_chat_model(model_name, model_provider="mistralai", temperature=0)
    return llm_provider

def gemini_20_flash_for_extract():
    llm = gemini_20_flash()
    model_name = llm.model_name
    os.environ["GENAI_API_KEY"] = llm.api_key
    llm_provider = init_chat_model(model_name, model_provider="google_genai", temperature=0)
    return llm_provider

def llama3_70b_8192_for_extract():
    llm = llama3_70b_8192()
    model_name = llm.model_name
    os.environ["GROQ_API_KEY"] = llm.api_key
    llm_provider = init_chat_model(model_name, model_provider="groq", temperature=0)
    return llm_provider

def claude_3_7_sonnet_20250219_for_extract():
    llm = claude_3_7_sonnet_20250219()
    model_name = llm.model_name
    os.environ["ANTHROPIC_API_KEY"] = llm.api_key
    llm_provider = init_chat_model(model_name, model_provider="anthropic", temperature=0)
    return llm_provider

