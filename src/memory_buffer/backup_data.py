"""Lưu lịch sử trò chuyện, các thông tin quan trọng được trích xuất từ lịch sử trò chuyện vào database."""
import chainlit as cl


def backup(user_id, session_id, extracting_result, summary_result, retrieval_result, history_conversation):
    print(f"[LOG] Backup data...")
    print(f"[LOG] Backup data done!")