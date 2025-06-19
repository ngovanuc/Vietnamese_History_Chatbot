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
from src.commands.rag import rag

# @cl.on_message
async def on_message(message: cl.Message):
    # Điều hướng sang command examination
    if message.command == "Examination":
        await examination(message)
        return
    # Điều hướng sang command RAG
    if message.command == "RAG":
        await rag(message)
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

    # TODO: Xử lý câu hỏi đầu vào ban đầu, bao gồm:
    # 1. Sử dụng các lược đồ để trích xuất các thông tin quan trọng từ người dùng
    # 2. Map các thông tin đã trích xuất được vào prompt phù hợp với hoàn cảnh hiện tại

    """Chỉ lựa chọn một trong hai: memory buffer hoặc short memory buffer để chạy"""
    # TODO: Code này cho mục đích memory buffer
    # Trích xuất câu hỏi từ người dùng
    extracting_result, summary_result, retrieval_result = await memory_buffer(query=user_input, top_k=1)
    prompt_template, _ = choose_prompt(extracting_result, summary_result, retrieval_result)
    prompt_mapping = prompt_mapping_management(extracting_result=extracting_result, 
                                               summary_result=summary_result, 
                                               retrieval_result=retrieval_result, 
                                               user_query=user_input, 
                                               k=_)
    cl.user_session.set("extracting_question", extracting_result)
    # print(f"[LOG] User information (extracted): {cl.user_session.get('user_information')}")
    
    # TODO: Code này cho mục đích short memory buffer
    # Chọn prompt phù hợp dựa trên hoàn cảnh hiện tại (prompt_template)
    # Mapping câu hỏi người dùng và lịch sử trò chuyện đã được tóm tắt vào prompt (prompt_mapping)
    # prompt_template, prompt_mapping = short_memory_buffer(user_input=user_input)

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