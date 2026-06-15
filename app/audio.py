from faster_whisper import WhisperModel
from fastapi import UploadFile
import tempfile
import os

# Load small model (fast + CPU-friendly)
model = WhisperModel("small", device="cpu", compute_type="int8")

async def transcribe_audio(file: UploadFile):
    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path, beam_size=1)

    text = " ".join([seg.text for seg in segments])

    os.remove(tmp_path)

    return {
        "language": info.language,
        "text": text.strip()
    }
