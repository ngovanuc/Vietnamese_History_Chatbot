"""Short memory buffer cố gắng giữ ngữ cảnh trong phiên trò chuyện hiện tại."""
import chainlit as cl

from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_MEMORY_BUFFER
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION_SUMMARY
from src.prompt_engineering.question_answering_prompt import QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION

from src.prompt_engineering.realtime_chat_prompt import REALTIME_CHAT_PROMPT
from src.prompt_engineering.realtime_chat_prompt import REALTIME_CHAT_PROMPT_WITH_HISTORY_CONVERSATION_SUMMARY
from src.prompt_engineering.realtime_chat_prompt import REALTIME_CHAT_PROMPT_WITH_LATEST_3_CONVERSATION
from src.prompt_engineering.realtime_chat_prompt import REALTIME_CHAT_PROMPT_WITH_RETRIEVAL_INFORMATION
from src.prompt_engineering.realtime_chat_prompt import REALTIME_CHAT_PROMPT_WITH_HISTORY_CONVERSATION_SUMMARY_AND_RETRIEVAL_INFORMATION


def prompt_routing(text: str|None=None):
    print("[LOG] Prompt routing...")
    if cl.user_session.get("realtime_chat"):
        # Chức năng realtime đang bật
        if text == None:
            print("[LOG] No text provided and realtime chat is on. Return 1!")
            return REALTIME_CHAT_PROMPT, 1
        else:
            print("[LOG] Text provided and realtime chat is on. Return 2!")
            return REALTIME_CHAT_PROMPT_WITH_HISTORY_CONVERSATION_SUMMARY, 2

    else:
        # Chế độ hỏi đáp bình thường
        if text == None:
            print("[LOG] No text provided and realtime chat is off. Return 3!")
            return QUESTION_ANSWERING_PROMPT, 3
        else:
            print("[LOG] Text provided and realtime chat is off. Return 4!")
            return QUESTION_ANSWERING_PROMPT_MAPPED_ONLY_HISTORY_CONVERSATION_SUMMARY, 4
    

def short_memory_buffer(user_input: str|None=None):
    print("[LOG] Short memory buffer...")
    prompt_template, _ = prompt_routing(text=user_input)

    if _ == 1:
        prompt_mapping = {"question": user_input,}
        return prompt_template, prompt_mapping

    elif _ == 2:
        summary_of_history_conversation = cl.user_session.get("summary_of_history_conversation")
        prompt_mapping = {
            "history_conversation_summary": summary_of_history_conversation,
            "question": user_input,
        }
        return prompt_template, prompt_mapping
    
    elif _ == 3:
        prompt_mapping = {
            "question": user_input,
        }
        return prompt_template, prompt_mapping

    elif _ == 4:
        summary_of_history_conversation = cl.user_session.get("summary_of_history_conversation")
        prompt_mapping = {
            "history_conversation_summary": summary_of_history_conversation,
            "question": user_input,
        }
        return prompt_template, prompt_mapping

    else:
        raise ValueError("Invalid value for _. Field when returning prompt_template and prompt_mapping.")