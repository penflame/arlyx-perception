from fastapi import UploadFile
from PIL import Image
import io

async def analyze_image(file: UploadFile):
    content = await file.read()
    image = Image.open(io.BytesIO(content))

    width, height = image.size
    mode = image.mode
    format = image.format

    return {
        "width": width,
        "height": height,
        "mode": mode,
        "format": format
    }
