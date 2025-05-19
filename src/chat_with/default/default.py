from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq

from src.llms.default import default


def chat_with_default(temperature, streaming):
    model_config = default()
    model = ChatCohere(
        model=model_config.model_name,
        cohere_api_key=model_config.api_key,
        temperature=temperature,
        streaming=streaming,
    )
    return model