import chainlit as cl

from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableConfig

from src.chat_with.model_routing import model_routing
from src.memory_buffer.short_memory_buffer import short_memory_buffer
from src.memory_buffer.summary_history_conversation import summarize_history_conversation


# @cl.step(type="tool")
async def generate_text_answer(transcription):
    # Chọn prompt phù hợp và nạp thông tin vào prompt
    prompt_template, prompt_mapping = short_memory_buffer(user_input=transcription)

    # Nạp prompt, điều hướng model trả lời, xây dựng chain
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm_model = model_routing()
    chain: Runnable = prompt | llm_model | StrOutputParser()

    # Sinh phản hồi
    response = chain.invoke(input=prompt_mapping,)

    cl.user_session.set("count_chat", cl.user_session.get("count_chat") + 1)

    # Tạo bản tóm tắt lịch sử trò chuyện sau phản hồi
    summary_of_history_conversation = await summarize_history_conversation()
    cl.user_session.set("summary_of_history_conversation", summary_of_history_conversation.summary)
    print("[LOG] Summarizing history conversation... Done!")
    print(f"[LOG] Summary of history conversation: {summary_of_history_conversation.summary}")

    return response