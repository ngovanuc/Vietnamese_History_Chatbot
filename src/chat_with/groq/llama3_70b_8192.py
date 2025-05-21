from langchain_groq import ChatGroq

from src.llms.groq import llama3_70b_8192


def chat_with_llama3_70b_8192(streaming, temperature):
    model_config = llama3_70b_8192()
    model = ChatGroq(
        model=model_config.model_name,
        groq_api_key=model_config.api_key,
        streaming=streaming,
        temperature=temperature,
    )
    return model