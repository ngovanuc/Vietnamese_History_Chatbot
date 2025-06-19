import chainlit as cl
import asyncio

from src.chat_life_cycle.retrieval_document.processing_document import processing_document
from src.chat_life_cycle.retrieval_document.prompt_mapping import mapping_prompt
from src.chat_life_cycle.retrieval_document.retrieval import retriever
from src.chat_life_cycle.on_message.suggestions import suggestions

# from src.memory_buffer.retrieval_information import retriever
from src.memory_buffer.summary_history_conversation import summarize_history_conversation

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableConfig
from src.chat_with.model_routing import model_routing


async def management(message: cl.Message):
    print("[LOG] RAG management...")

    # Kiểm tra đầu vào của người dùng
    has_text = bool(message.content)
    has_file = bool(message.elements)

    print("[LOG] Has text: ", has_text)
    print("[LOG] File: ", has_file)

    print("[LOG] Câu hỏi như sau: ", message.content)
    print("[LOG] File nhận: ", message.elements)

    # TH1: Upload file và đặt câu hỏi: Xử lý file -> Xử lý câu hỏi -> Trả lời
    # TH2: Chỉ upload file: Xử lý file -> Hỏi xem người dùng muốn làm gì với file này không?
    # TH3: Chỉ đặt câu hỏi: Kiểm tra xem đã upload file trước đó chưa? -> [yes] Xử lý câu hỏi -> Trả lời
    #                                                                  -> [no] Yêu cầu người dùng cung cấp một file

    # TODO: Đoạn này đang "mở" và cần giải quyết hết các trường hợp
    if has_file:
        # Xử lý file đầu vào:
        # Check type and sizeof file
        # Open file and read content
        # Preprocesing content of file
        # Chunk file
        # Embedding and save to Qdrant
        # Understand file (using LLM if needed)
        process = await processing_document(message)
        if process == False:
            await cl.Message(content="Lỗi trong khi xử lý file!").send()
            return None
        cl.user_session.set("files", True)
        pass
    else:
        # Nếu người dùng không upload file, kiểm tra xem đã upload file trước đó hay chưa
        # Nếu không có file thì chắc chắn có text
        if cl.user_session.get("files"):
            # Đã upload file trước đó rồi, chỉ cần xử lý câu hỏi trò chuyện thôi
            # Đi tới Retrieval
            pass
        else:
            # Chưa có file và đang bật command RAG, đề xuất người dùng upload file
            # Có thể return hoặc cho phép người dùng tiếp tục chat
            await cl.Message(content="Bạn đang dùng RAG và bạn chưa upload file. Vui lòng tải lên một file PDF hoặc TXT").send()
            return

    # Nếu có file mà không có câu hỏi
    if not has_text:
        # Hỏi xem người dùng muốn làm gì với file
        await cl.Message(content="Bạn đã upload một file nhưng bạn không đặt câu hỏi!").send()
        return
    
    # Retrieval
    collection_name = cl.user_session.get("collection_name")
    retrieval_result = retriever(collection_name=collection_name, query=message.content, top_k=1)
    print("[LOG] Kết quả retrieval tài liệu: \n", [result.payload['embedding_content'] for result in retrieval_result])
    
    # Xử lý câu hỏi (mapping câu hỏi vào prompt)
    prompt_template, prompt_mapping = await mapping_prompt(question=message.content, retrieval_result=retrieval_result)

    # Các cài đặt để phóng tokens phản hồi trực tiếp (streaming)
    callback = cl.LangchainCallbackHandler()
    stream_msg = cl.Message(content="")

    # Xây dựng chain
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm_model = model_routing()
    chain: Runnable = prompt | llm_model | StrOutputParser()

    # Trả lời câu hỏi
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

    # Trả lời xong rồi thì hiển thị suggestion nếu cần thiết
    if cl.user_session.get('chat_settings')["Suggestions"]:
        await suggestions()

    # Tóm tắt lịch sử hội thoại để có bối cảnh trò chuyện
    summary_of_history_conversation = await summarize_history_conversation()
    cl.user_session.set("summary_of_history_conversation", summary_of_history_conversation.summary)
    print("[LOG] Summarizing history conversation... Done!")
    print(f"[LOG] Summary of history conversation: {summary_of_history_conversation.summary}")

    # Backup data nếu cần thiết
    # backup(user_input=user_input, response=response)
    cl.user_session.set("count_chat", cl.user_session.get("count_chat") + 1)

    return