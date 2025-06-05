import io
import os
import torchaudio
import chainlit as cl

from src.chat_life_cycle.realtime_chat.init import whisper_processor, whisper_model


# @cl.step(type="tool")
async def speech_to_text(whisper_input):
    filename, audio_buffer, mime_type = whisper_input
    waveform, sample_rate = torchaudio.load(io.BytesIO(audio_buffer))

    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        sample_rate = 16000

    # Convert sang tensor input cho model
    input_features = whisper_processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt").input_features

    # Dự đoán
    predicted_ids = whisper_model.generate(input_features)

    # Decode ra text
    transcription = whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription