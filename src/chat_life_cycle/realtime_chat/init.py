import os
import io
import wave
import httpx
import torch
import torchaudio
import numpy as np
import audioop
import chainlit as cl
import tempfile
import pyttsx3
import whisper
import faster_whisper

from pyttsx3 import engine
from pathlib import Path
from faster_whisper import WhisperModel
from transformers import WhisperProcessor
from transformers import WhisperForConditionalGeneration


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define a threshold for detecting silence and a timeout for ending a turn
# Xác định ngưỡng để phát hiện sự im lặng và thời gian chờ để kết thúc lắng nghe
# Adjust based on your audio level (e.g., lower for quieter audio)
# Điều chỉnh dựa trên mức âm thanh của bạn (ví dụ: thấp hơn để có âm thanh nhỏ hơn)
global SILENCE_THRESHOLD

# Seconds of silence to consider the turn finished
# Thời gian im lặng để xem xét là người dùng hoàn thành câu hỏi
global SILENCE_TIMEOUT

# whisper_model_path = "../../audio_models/whisper/whisper-tiny/"
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
whisper_model_path = project_root / "audio_models" / "whisper" / "whisper-tiny"
whisper_processor = WhisperProcessor.from_pretrained(whisper_model_path)
whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_path)
whisper_model.config.forced_decoder_ids = None  # Cho phép tự phát hiện ngôn ngữ

# Chọn giọng tiếng Việt
# Xem hướng dẫn cài đặt hỗ trợ tiếng Việt để sử dụng pyttsx3 tại đây:
# https://www.youtube.com/watch?v=aw7FVWOY1yE&t=213s
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)