import chainlit as cl

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from src.prompt_engineering.rag_command_prompt import RAG_COMMAND_PROMPT
from src.prompt_engineering.rag_command_prompt import RAG_COMMAND_PROMPT_2
from src.prompt_engineering.rag_command_prompt import RAG_COMMAND_PROMPT_3


async def mapping_prompt(question, retrieval_result):
    # Lấy bản tóm tắt lịch sử hội thoại
    summary_of_history_conversation = cl.user_session.get("summary_of_history_conversation")

    # Lấy nội dung truy xuất được
    for result in retrieval_result:
        # Do k=1, nên lấy nội dung cuối cùng truy xuất được
        content = result.payload['embedding_content']

    prompt_mapping = {
        "history_conversation": summary_of_history_conversation,
        "retrieved_context": content,
        "question": question,
    }
    return RAG_COMMAND_PROMPT_3, prompt_mapping