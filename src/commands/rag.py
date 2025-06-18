import asyncio

import chainlit as cl

from src.chat_life_cycle.retrieval_document.root_management import management


async def rag(message: cl.Message):
    """
    Điều hướng sang command RAG (Retrieval Augmented Generation).
    Hệ thống RAG này yêu cầu người dùng phải cung cấp một file để sử dụng, trong mỗi phiên trò chuyện
    chỉ cho phép tải lên một tập duy nhất mà thôi. Nếu sử dụng RAG mà không có file nào tải lên, hệ thống
    sẽ yêu câu người dùng phải tải lên một file mà hệ thống chấp nhận.

    Command RAG được chuyển về chat_life_cycle/retrieval_document/...
    """
    print("[LOG] RAG command...")
    await management(message)
    return