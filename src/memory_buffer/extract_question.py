"""Lược đồ trích xuất câu hỏi: Nhằm trích xuất các thông tin quan trọng trong câu hỏi."""
import os
import time
import asyncio
from src.memory_buffer.init_llm_for_extract import command_a_03_2025_for_extract
from src.memory_buffer.init_llm_for_extract import mistral_large_latest_for_extract
from src.memory_buffer.init_llm_for_extract import gemini_20_flash_for_extract
from src.memory_buffer.init_llm_for_extract import llama3_70b_8192_for_extract
from src.memory_buffer.init_llm_for_extract import claude_3_7_sonnet_20250219_for_extract

from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain.chat_models import init_chat_model

from src.memory_buffer.define_schema_extraction import SchemaExtractionQuestion


# Có thể thay thế bằng các model khác được import ở trên
llm = mistral_large_latest_for_extract()

# Xây dựng prompt hướng dẫn LLM trích xuất thông tin
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Bạn là một chuyên gia trong lĩnh vực trích xuất thông tin liên quan tới người dùng. 
     Hãy trích xuất các thông tin như tên và tuổi trong văn bản được cung cấp. Nếu không biết, hãy trả về giá trị null"""),
    ("human", "{text}"),
])

async def extracting(text: str|None=None):
    """Trích xuất các thông tin quan trọng từ câu hỏi người dùng.
    
    Inputs:
        text: Câu hỏi người dùng.
        
    Ouptuts:
        output: Đối tượng class chứa dữ liệu trích xuất được. Có thể truy xuất như sau:
        for field, value in output.model_dump().items():
            print(f"{field}: {value}")
    """
    if text == None:
        print(f"[LOG] No text provided!")
        return None
    try:
        structured_output = llm.with_structured_output(schema=SchemaExtractionQuestion)
        prompt = prompt_template.invoke({"text": text})
        output = structured_output.invoke(prompt)
        return output
    except Exception as e:
        print("[LOG] Error while extracting question! Error: ", e)
        return None
    