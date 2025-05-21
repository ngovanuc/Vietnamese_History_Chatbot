from langchain_anthropic import ChatAnthropic

from src.llms.anthropic import claude_3_7_sonnet_20250219


def chat_with_claude_3_7_sonnet_20250219(streaming, temperature):
    model_config = claude_3_7_sonnet_20250219()
    model = ChatAnthropic(
        model=model_config.model_name,
        api_key=model_config.api_key,
        streaming=streaming,
        temperature=temperature,
    )
    return model