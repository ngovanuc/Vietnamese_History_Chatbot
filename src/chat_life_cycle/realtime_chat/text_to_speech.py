import io
import os
import wave
import httpx
import torch
import torchaudio
import numpy as np
import audioop
import tempfile
import pyttsx3
import chainlit as cl

from src.chat_life_cycle.realtime_chat.init import engine


# @cl.step(type="tool")
async def text_to_speech(text: str, mime_type: str):
    """Trả về phải là:
        - buffer.name: Tên của file âm thanh được tạo, ví dụ "output_audio.wav"
        - buffer.read(): Kiểu: bytes: Dữ liệu nhị phân của file âm thanh (.wav, .mp3,... tùy theo mime_type)"""
    voice_speed = cl.user_session.get("chat_settings")["Voice_speed"]
    engine.setProperty('rate', voice_speed)
    # Tạo file tạm để lưu âm thanh
    ext = mime_type.split("/")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as f:
        temp_filename = f.name

    # Lưu âm thanh vào file
    engine.save_to_file(text, temp_filename)
    engine.runAndWait()

    # Đọc file thành bytes
    with open(temp_filename, "rb") as audio_file:
        audio_bytes = audio_file.read()

    # Xóa file tạm
    os.remove(temp_filename)

    buffer = io.BytesIO(audio_bytes)
    buffer.name = f"output_audio.{ext}"
    buffer.seek(0)
    return buffer.name, buffer.read()