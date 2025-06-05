import os
import time
import tempfile
import io
import wave
import httpx
import numpy as np
import audioop
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper


SILENCE_THRESHOLD = (3500)
SILENCE_TIMEOUT = 1300.0

model = whisper.load_model(name="tiny", download_root="../../audio_models/whisper/")

def transcribe_with_whisper(audio_path):
    print("🧠 Đang chuyển giọng nói thành văn bản...")
    result = model.transcribe(audio_path, language="en")
    return result["text"]

def record_audio():
    print("🎙️ Đang ghi nói...")
    audio = sd.rec(int(10 * 16000), samplerate=16000, channels=1)
    sd.wait()
    return audio

def save_wav(audio, filename):
    wav.write(filename, 16000, audio)

def main():
    audio = record_audio()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        save_wav(audio, tmpfile.name)
        text = transcribe_with_whisper(tmpfile.name)
        os.unlink(tmpfile.name)  # Xóa file sau khi xử lý

    print("\n📄 Văn bản nhận được:")
    print("🗣️", text)


if __name__ == "__main__":
    main()