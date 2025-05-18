from langchain_cohere import ChatCohere

from source.llms.cohere import command_a_03_2025

def chat_with_command_a_03_2025(streaming, temperature):
    model_config = command_a_03_2025()
    model = ChatCohere(
        model=model_config.model_name,
        cohere_api_key=model_config.api_key,
        streaming=streaming,
        temperature=temperature,
    )
    return model