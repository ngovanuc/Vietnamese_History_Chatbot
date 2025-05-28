import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

# Cấu hình
SAMPLE_RATE = 16000  # Tốc độ lấy mẫu
SILENCE_DURATION = 1.5  # Thời gian im lặng để kết thúc (giây)
THRESHOLD = 0.01  # Ngưỡng âm lượng để phát hiện im lặng

def record_audio():
    print("🎙️ Bắt đầu ghi âm... (nói gì đó và im lặng để dừng)")
    recording = []
    silence_counter = 0

    def callback(indata, frames, time, status):
        nonlocal recording, silence_counter
        volume_norm = np.linalg.norm(indata) * 10
        recording.extend(indata.copy())

        if volume_norm < THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0

        if silence_counter > int(SILENCE_DURATION * SAMPLE_RATE / 1024):
            raise sd.CallbackStop()

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        try:
            sd.sleep(100000)  # sẽ bị dừng bởi CallbackStop
        except sd.CallbackStop:
            pass

    print("🛑 Dừng ghi âm.")
    return np.array(recording)

def save_wav(audio_data, filename):
    wav.write(filename, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))

def transcribe_with_whisper(audio_path):
    print("🧠 Đang chuyển giọng nói thành văn bản...")
    model = whisper.load_model(name="base", download_root="../../audio_models/whisper")
    result = model.transcribe(audio_path, language="vi")
    return result["text"]

if __name__ == "__main__":
    audio = record_audio()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        save_wav(audio, tmpfile.name)
        text = transcribe_with_whisper(tmpfile.name)
        os.unlink(tmpfile.name)  # Xóa file sau khi xử lý

    print("\n📄 Văn bản nhận được:")
    print("🗣️", text)
