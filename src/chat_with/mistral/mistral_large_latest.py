from langchain_mistralai import ChatMistralAI

from src.llms.mistral import mistral_large_latest


def chat_with_mistral_large_latest(streaming, temperature):
    model_config = mistral_large_latest()
    model = ChatMistralAI(
        model=model_config.model_name,
        api_key=model_config.api_key,
        streaming=streaming,
        temperature=temperature,
    )
    return model