"""Memory buffer chịu trách nhiệm cung cấp thông tin:
    - Thông tin câu hỏi trích xuất được.
    - Thông tin trích xuất được từ vector database
    - Tóm tắt của lịch sử trò chuyện"""

import asyncio
import chainlit as cl

from src.memory_buffer.extract_question import extracting
from src.memory_buffer.summary_history_conversation import summarize
from src.memory_buffer.retrieval_information import retriever


async def memory_buffer(query: str|None=None, top_k: int|None=None):
    """
    Nhận câu hỏi đầu vào của người dùng sau đó:
        - Trích lược thông tin trong câu hỏi
        - Trích xuất các thông tin từ vector database
        - Tóm tắt lịch sử cuộc hội thoại
        
    Kết quả trả về:
        - extracting_result: Một đối tượng của class chứa các thông tin trích xuất được
        - summary_result: Một string thông tin được tóm tắt
        - retrieval_result: Trả về một đối tượng data point của Qdrant.
        Và có thể truy cập như sau: result.payload['embedding_content']}, score: {result.score}
    """
    # Chạy trích lược câu hỏi và Tóm tắt lịch sử đoạn chat song song
    extracting_result = asyncio.create_task(extracting(query))
    # summary_result = asyncio.create_task(summarize())
    summary_result = cl.user_session.get("summary_history_conversation")
    
    # Đợi kết quả trích lược và dùng nó để trích xuất vector database
    await extracting_result
    # await summary_result

    # Có hai hình thức lấy thông tin retrieval
    # Thứ 1: Dùng chính câu hỏi để retrieval
    # Thứ 2: Dùng thông tin có chọn lọc trong extracting_result để retrieval
    # Cụ thể là sử dụng bản tóm tắt câu hỏi hoặc keywords...
    retrieval_result = asyncio.create_task(retriever(query, top_k))
    await retrieval_result
    
    if extracting_result:
        print(f"[LOG] Kết quả trích xuất từ câu hỏi: {extracting_result}")
        for field, value in extracting_result.result().model_dump().items():
            print(f"[LOG] {field}: {value}")
            if value != None:
                # Nếu có thông tin mới được trích xuất thì cập nhật vào user_information
                user_information = cl.user_session.get("user_information")
                user_information = user_information.model_copy(update={field: value})
                cl.user_session.set("user_information", user_information)
        extracting_result = user_information

    print(f"[LOG] Kết quả tóm tắt lịch sử hội thoại: {summary_result}")
    # for field, value in summary_result.result().model_dump().items():
        # print(f"[LOG] {field}: {value}")

    print(f"[LOG] Kết quả truy xuất thông tin từ database: {retrieval_result}")
    # for result in retrieval_result.result():
    for result in retrieval_result:
        print(f"Content: {result.payload['embedding_content']}\nscore: {result.score}\n")

    return extracting_result, summary_result, retrieval_result
