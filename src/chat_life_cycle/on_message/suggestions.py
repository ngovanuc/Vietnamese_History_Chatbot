import ast
import chainlit as cl
import cohere

from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable

from src.llms.cohere import command_a_03_2025
from src.prompt_engineering.suggestions_prompt import SUGGESTIONS_PROMPT


llm = command_a_03_2025()
model_name = llm.model_name
api_key = llm.api_key

co = cohere.Client(api_key=api_key)


def model_config():
    model_config = ChatCohere(
        model=model_name,
        cohere_api_key=api_key,
        streaming=False,
        temperature=1.0,
    )
    return model_config
 

async def suggestions():
    print("[LOG] Đang tạo suggestions cho cuộc trò chuyện...")
    lastest_chatbot_answer = cl.chat_context.to_openai()[-1].get("content")
    print(f"[LOG] The latest chatbot's answer: {lastest_chatbot_answer}")

    prompt = ChatPromptTemplate.from_template(template=SUGGESTIONS_PROMPT)
    llm = model_config()
    chain: Runnable = prompt | llm | StrOutputParser()

    suggestions = chain.invoke(input={"last_response": lastest_chatbot_answer})
    print(f"[LOG] Suggestions: {suggestions}")

    list_dict_suggestions = ast.literal_eval(suggestions)

    suggestions = cl.CustomElement(name="FollowUpSuggestions", props={"suggestions": list_dict_suggestions})
    # await cl.Message(content="Suggestions", elements=[suggestions]).send()
    await cl.Message(content="", elements=[suggestions]).send()

    return None