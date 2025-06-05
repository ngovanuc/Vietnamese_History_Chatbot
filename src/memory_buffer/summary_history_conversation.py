"""Lược đồ trích xuất câu hỏi: Nhằm trích xuất các thông tin quan trọng trong câu hỏi."""
import os
import time
import chainlit as cl

from src.memory_buffer.init_llm_for_extract import command_a_03_2025_for_extract
from src.memory_buffer.init_llm_for_extract import mistral_large_latest_for_extract
from src.memory_buffer.init_llm_for_extract import gemini_20_flash_for_extract
from src.memory_buffer.init_llm_for_extract import llama3_70b_8192_for_extract
from src.memory_buffer.init_llm_for_extract import claude_3_7_sonnet_20250219_for_extract

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatMessagePromptTemplate

from src.memory_buffer.define_schema_extraction import SummaryConversation


# Có thể thay thế bằng các model khác được import ở trên
llm = command_a_03_2025_for_extract()

# Xây dựng prompt hướng dẫn LLM trích xuất thông tin
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Bạn là một chuyên gia trong trong việc tóm tắt lịch sử cuộc trò chuyện giữa người dùng và chatbot,
    nội dung tóm tắt được dùng để bổ sung ngữ cảnh cho chatbot có trí nhớ lâu dài. 
    Hãy tóm tắt các nội dung chính của các phiên hội thoại này sao cho ngắn gọn nhưng phải đầy đủ thông tin để
    giúp chatbot có trí nhớ dài hạn."""),
    ("human", "{text}"),
])

async def summarize(history_conversations: str|None=None):
    """Tóm tắt lịch sử cuộc trò chuyện.
    
    Inputs:
        history_conversaton: Danh sách các cuộc trò chuyện giữa người dùng và chatbot.
        
    Ouptuts:
        output: Một bản tóm tắt ở dạng đối tượng.
    """
    if history_conversations == None:
        print(f"[LOG] No history conversation provided! Auto get history conversation from user session or MongoDB!")
        # Tự động lấy lịch sử đoạn chat trong phiên người dùng của chainlit
        history_conversations = cl.chat_context.to_openai() # history_conversations is a dict
        if len(history_conversations) >= 5:
            # Lấy 5 cuộc hội thoại cuối
            latest_5_conversations = dict(list(history_conversations.items())[-5:])
            # Chuyển dict sang str
            history_conversations = str(latest_5_conversations)

        # Hoặc có thể lấy từ cơ sở dữ liệu MongoDB
    try:
        structured_output = llm.with_structured_output(schema=SummaryConversation)
        prompt = prompt_template.invoke({"text": history_conversations})
        output = structured_output.invoke(prompt)
        return output
    except Exception as e:
        print("[LOG] Error while summarize history conversation! Error: ", e)
        return None
    
    
async def summarize_history_conversation():
    print("[LOG] Summarizing history conversation...")
    messages = cl.chat_context.to_openai()
    if len(messages) >= 5:
        messages = str(messages[-5:])
    else:
        messages = str(messages)
    try:
        structured_output = llm.with_structured_output(schema=SummaryConversation)
        prompt = prompt_template.invoke({"text": messages}) 
        output = structured_output.invoke(prompt)
        print("[LOG] Summarizing history conversation... Done!")
        return output
    except Exception as e:
        print("[LOG] Error while summarize history conversation! Error: ", e)
        print("[LOG] History conversation will be used as summary...")
        output = SummaryConversation(summary=messages)
        return output