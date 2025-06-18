import PyPDF2
import chainlit as cl
import asyncio

from transformers import AutoTokenizer
from transformers import AutoModel
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer

from qdrant_client import models
from qdrant_client import QdrantClient

from pathlib import Path

from src.memory_buffer.retrieval_information import embedding_model
from src.memory_buffer.retrieval_information import qdrant_client
from src.memory_buffer.retrieval_information import retriever


async def check_file(message: cl.Message):
    print("[LOG] Check file...")
    # Mỗi lần chỉ xử lý một file
    file = message.elements[0]
    file_name = file.name
    file_type = file.mime
    file_size = (len(file.content) if file.content else 0)
    """
    CÁC VẤN ĐỀ BẢO MẬT HỆ THỐNG KHI NHẬN MỘT FILE CỦA NGƯỜI DÙNG:
    - Việc đảm bảo an toàn cho hệ thống là điều cần thiết khi người dùng tải lên tài liệu trong các
    ứng dụng. Cần có những biện pháp mạnh mẽ để ngăn ngừa tác động tiêu cực đến toàn bộ hệ thống.

    Các phương pháp có thể cân nhắc:
        - Kiểm tra và xác thực file: Kiểm tra phần mở rộng, kiểu MIME, kích thước, header file...
        - Quét virus: Sử dụng phần mềm diệt virus, quét virus định kỳ
        - Cách ly file: Lưu trữ riêng biệt, không trực tiếp thực thi file
        - Cài đặt môi trường sandbox: Tạo sandbox để cách ly, kiểm soát truy cập
        - Mã hóa: Mã hóa dữ liệu
        - Ghi nhật ký và giám sát, update phần mềm và đào tạo người dùng...
    """
    # Chấp nhận file txt
    if file_type == "text/plain" or file_type == "application/txt" or file_type == 'text/x-plain':
        file_size_mb = len(file.content) / (1024 * 1024) if file.content else 0
        # Nếu file txt lớn hơn 5 mb thì không mở
        if file_size_mb > 1:
            await cl.Message(content="File size is too large!").send()
            return False
        else:
            # Tiếp tục
            return True
    # Hoặc chấp nhận file pdf
    elif file_type == "application/pdf":
        file_size_mb = len(file.content) / (1024 * 1024) if file.content else 0
        # Nếu file lớn hơn 5 mb thì không mở
        if file_size_mb > 5:
            await cl.Message(content="File size is too large!").send()
            return False
        else:
            return True
    # Còn lại: cút...
    else:
        await cl.Message(content="File type is not supported!").send()
        return True


async def get_content_file(message):
    print("[LOG] Get content file...")
    file = message.elements[0]
    # if file.content:
    #     try:
    #         file_content = file.content.decode('utf-8')
    #         # await cl.Message(content=f"Nội dung file: {file_content}").send()
    #         print("[LOG] File content has been readed!")
    #         return file_content
    #     except UnicodeDecodeError:
    #         await cl.Message(content="Lỗi: Không thể giải mã file bằng UTF-8. Hãy thử một định dạng khác.").send()
    #         return
    #     except Exception as e:
    #         await cl.Message(content="Lỗi trong khi xử lý file!").send()
    #         print("[LOG] Error while reading file content!")
    #         return
    # else:
    #     await cl.Message(content="Lỗi: File không có nội dung.").send()
    #     return 
    if file.mime == "text/plain":
        with open(file.path, "r") as f:
            content = f.read()
        return content
    if file.mime == "application/pdf":
        with open(file.path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()
            return text_content
        

async def preprocessing_content_file(content: str):
    """Tiền xử lý văn bản trước khi đưa vào model embedding."""
    print("[LOG] Preprocessing content file...")
    # Do nothing
    return content


async def chunking(content, chunk_size=1024, overlap=100):
    print("[LOG] Chunking content...")
    # Chunk content to chunks with chunk_size
    # Return list of chunks
    chunks = []
    for i in range(0, len(content), chunk_size - overlap):
        chunks.append(content[i:i + chunk_size])
    return chunks


async def load_embedding_model():
    print("[LOG] Loading model embedding...")
    # Do nothing
    return embedding_model

async def connect_to_qdrant():
    print("[LOG] Loading vector database...")
    return qdrant_client

async def embedding_content(chunks, model_embedding, qdrant_client, collection_name):
    print("[LOG] Embedding content...")
    max_length_ids_vector_database = cl.user_session.get("max_length_ids_vector_database")
    for idx in range(max_length_ids_vector_database, len(chunks) + max_length_ids_vector_database):
        content = chunks[idx - max_length_ids_vector_database]
        payload = {"embedding_content": content}
        vector = model_embedding.encode(content).tolist()
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[models.PointStruct(id=idx, vector=vector, payload=payload)]
        )
    cl.user_session.set("max_length_ids_vector_database", len(chunks) + max_length_ids_vector_database)
    return None


async def processing_document(message: cl.Message):
    """Các bước thứ tự như sau:
    - Kiểm tra kiểu file, kích thước file
    - Mở file và đọc nội dung
    - Tiền xử lý nội dung (loại bỏ ký tự đặc biệt...)
    - Chunking content về độ dài thích hợp (1024)
    - Load model embedding, Qdrant và thực hiện embedding content, lưu vào Qdrant
    - Dùng LLM để hiểu file (nếu cần)"""

    print("[LOG] Processing document...")
    check_file_status = await check_file(message)
    if check_file_status:
        content_file = await get_content_file(message)
        if content_file:
            content_file = await preprocessing_content_file(content_file)
            chunks = await chunking(content_file, chunk_size=2048, overlap=100)
            embedding_model = await load_embedding_model()
            qdrant_client = await connect_to_qdrant()
            collection_name = cl.user_session.get("collection_name")
            await embedding_content(chunks, embedding_model, qdrant_client, collection_name)
        return True
    else:
        print("[LOG] Error while processing document!")
        return False
