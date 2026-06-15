import mimetypes
from vision import analyze_image
from ocr import extract_text
from audio import transcribe_audio

async def analyze_file(file):
    mime, _ = mimetypes.guess_type(file.filename)

    if not mime:
        return {"status": "error", "detail": "Unknown file type"}

    # IMAGE
    if mime.startswith("image/"):
        vision = await analyze_image(file)
        return {
            "type": "image",
            "vision": vision
        }

    # AUDIO
    if mime.startswith("audio/"):
        audio = await transcribe_audio(file)
        return {
            "type": "audio",
            "audio": audio
        }

    # PDF → OCR
    if mime == "application/pdf":
        ocr = await extract_text(file)
        return {
            "type": "pdf",
            "ocr": ocr
        }

    return {"status": "unsupported", "mime": mime}
