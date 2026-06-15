from fastapi import UploadFile
import pytesseract
from PIL import Image
import io

async def extract_text(file: UploadFile):
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    text = pytesseract.image_to_string(image, lang="fra")
    return {"text": text.strip()}
