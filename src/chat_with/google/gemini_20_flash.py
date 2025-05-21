from langchain_google_genai import ChatGoogleGenerativeAI

from src.llms.google import gemini_20_flash

def chat_with_gemini_20_flash(streaming, temperature):
    disable_streaming = not streaming
    model_config = gemini_20_flash()
    model = ChatGoogleGenerativeAI(
        model=model_config.model_name,
        google_api_key=model_config.api_key,
        disable_streaming=disable_streaming,
        temperature=temperature,
    )
    return model