import os
import glob
import json
import asyncio

from typing import Dict
from typing import cast

import chainlit as cl

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableConfig

from src.chat_with.model_routing import model_routing
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT

from src.memory_buffer.extract_question import extracting
from src.memory_buffer.summary_history_conversation import summarize
from src.memory_buffer.summary_history_conversation import summarize_history_conversation
from src.memory_buffer.retrieval_information import retriever
from src.memory_buffer.memory_buffer import memory_buffer
from src.memory_buffer.backup_data import backup
from src.memory_buffer.short_memory_buffer import short_memory_buffer

from src.chat_life_cycle.on_message.suggestions import suggestions
from src.chat_life_cycle.on_message.prompt_mapping_management import choose_prompt
from src.chat_life_cycle.on_message.prompt_mapping_management import prompt_mapping_management

from src.commands.examination import examination


# @cl.on_message
async def on_message(message: cl.Message):
    # Điều hướng sang command examination
    if message.command == "Examination":
        await examination(message)
        return

    """
    Steps:
        - Chọn prompt phù hợp dựa trên hoàn cảnh hiện tại
        - Retrieval thông tin từ vector database
        - Mapping câu hỏi người dùng, thông tin được retireval và lịch sử trò chuyện đã được tóm tắt vào prompt
        - Nạp prompt, điều hướng model trả lời, xây dựng chain
        - Sinh phản hồi
        - Tạo bản tóm tắt lịch sử trò chuyện sau phản hồi
        - Backup nếu cần
    """
    user_input = message.content

    # Chọn prompt phù hợp dựa trên hoàn cảnh hiện tại (prompt_template)
    # Mapping câu hỏi người dùng và lịch sử trò chuyện đã được tóm tắt vào prompt (prompt_mapping)
    prompt_template, prompt_mapping = short_memory_buffer(user_input=user_input)

    # Nạp prompt (prompt), điều hướng model trả lời (llm_model), xây dựng chain (chain)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm_model = model_routing()
    chain: Runnable = prompt | llm_model | StrOutputParser()

    # Các cài đặt để phóng tokens phản hồi trực tiếp (streaming)
    callback = cl.LangchainCallbackHandler()
    stream_msg = cl.Message(content="")

    # Sinh phản hồi
    if cl.user_session.get("chat_settings")["Streaming"]:
        async for chunk in chain.astream(input=prompt_mapping, config=RunnableConfig(callbacks=[callback])):
            await stream_msg.stream_token(chunk)
        await stream_msg.send()
    
    else:
        response = chain.invoke(
            input=prompt_mapping,
            config=RunnableConfig(callbacks=[callback])
        )
        await cl.Message(content=response).send()

    cl.user_session.set("count_chat", cl.user_session.get("count_chat") + 1)

    # Tạo suggestions cho cuộc trò chuyện
    if cl.user_session.get('chat_settings')["Suggestions"]:
        await suggestions()

    # Tạo bản tóm tắt lịch sử trò chuyện sau phản hồi
    summary_of_history_conversation = await summarize_history_conversation()
    cl.user_session.set("summary_of_history_conversation", summary_of_history_conversation.summary)
    print("[LOG] Summarizing history conversation... Done!")
    print(f"[LOG] Summary of history conversation: {summary_of_history_conversation.summary}")

    # Backup data
    # backup(user_input=user_input, response=response)