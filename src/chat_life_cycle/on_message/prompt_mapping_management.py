import chainlit as cl

from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_MEMORY_BUFFER
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION_SUMMARY
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT


def choose_prompt(extracting_result, summary_result, retrieval_result):
    if extracting_result and summary_result and retrieval_result:
        # Có đầy đủ thông tin thì sử dụng prompt có thể map những thông tin đó vào prompt
        print("[LOG] Choose prompt mapped memory buffer...")
        return QUESTION_ANSWERING_PROMPT_MAPPED_MEMORY_BUFFER, 1
    
    elif extracting_result is None and retrieval_result is None and summary_result is not None:
        # Có thông tin tóm tắt lịch sử hội thoại, nhưng trích lược và truy xuất thất bại
        print("[LOG] Choose prompt mapped only history conversation...")
        return QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION_SUMMARY, 2
    
    elif extracting_result is None and retrieval_result is None and summary_result is None:
        # Không có thông tin nào để hỗ trợ memory buffer, chọn prompt để map lịch sử hội thoại
        print("[LOG] Choose prompt mapped only history conversation...")
        return QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION, 3
    
    else:
        # Nếu tất cả các thông tin trên đều rỗng, trả về prompt cơ bản nhất
        print("[LOG] Choose original prompt...")
        return QUESTION_ANSWERING_PROMPT, 4
    

def prompt_mapping_management(extracting_result, summary_result, retrieval_result, user_query, memory_buffer_mode, k):
    print("[LOG] Mapping prompt...")
    extracting_result = extracting_result.result()
    summary_result = summary_result.result()
    retrieval_result = retrieval_result.result()

    if memory_buffer_mode == True and k == 1:
        # Với những thông tin trích xuất được là None, đổi thành string rỗng
        for field, value in extracting_result.model_dump().items():
            if value is None:
                extracting_result.model_dump()[field] = ""
        retrieval_information = ""

        for result in retrieval_result:
            retrieval_information += result.payload['embedding_content'] + "\n"

        prompt_mapping = {
            # "name": extracting_result.name,
            # "age_group": extracting_result.age_group,
            # "language": extracting_result.language,
            # "level": extracting_result.level,
            # "tone_preference": extracting_result.tone_preference,
            # "current_emotion": extracting_result.current_emotion,
            # "current_topic": extracting_result.current_topic,
            # "interested_characters": extracting_result.interested_characters,
            # "emotional_expression": extracting_result.emotional_expression,
            # "relative_question": extracting_result.relative_question,
            # "keywords": extracting_result.keywords,
            # "question_summary": extracting_result.question_summary,
            # "retrieval_information": retrieval_information,
            "summary": summary_result,
            "question": user_query
        }
        print("[LOG] Mapping prompt 1 done!")
        return prompt_mapping
    
    elif memory_buffer_mode == True and k == 2:
        # Khi trích lược và trích xuất thất bại, history_summary thành công
        prompt_mapping = {
            "question": user_query,
            "history_conversation_summary": summary_result.summary
        }
        return prompt_mapping
    
    elif memory_buffer_mode == True and k == 3:
        # Khi việc trích lược câu hỏi, truy xuất thông tin và cả tóm tắt lịch sử các đoạn hội thoại thất bại
        history_conversation = cl.chat_context.to_openai()
        if len(history_conversation) > 2:
            # Lấy hai cặp giá trị cuối cùng
            top_2_latest_conversation = str(dict(list(history_conversation.items())[-2:]))
        else:
            top_2_latest_conversation = str(history_conversation)

        prompt_mapping = {
            "question": user_query,
            "history_conversation": top_2_latest_conversation
        }
        return prompt_mapping
    
    elif memory_buffer_mode == False or k == 4:
        prompt_mapping = {
            "question": user_query,
        }
        return prompt_mapping
    