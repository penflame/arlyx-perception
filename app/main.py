from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import httpx
import os

from vision import analyze_image
from ocr import extract_text
from audio import transcribe_audio
from webdav import scan_webdav

app = FastAPI(title="ARLYX Perception v2.1")

ARLYX_CORE_URL = os.getenv("ARLYX_CORE_URL", "http://arlyx-core:8000")


class IngestPayload(BaseModel):
    source: str
    modality: str
    content: str


@app.get("/health/")
async def health():
    return {"status": "ok", "component": "perception"}


@app.post("/ingest/")
async def ingest(payload: IngestPayload):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(f"{ARLYX_CORE_URL}/ingest", json=payload.dict())
            return {"status": "forwarded", "core_status": r.status_code}
        except Exception as e:
            return {"status": "error", "detail": str(e)}


@app.post("/vision/")
async def vision_endpoint(file: UploadFile = File(...)):
    result = await analyze_image(file)
    return {"status": "ok", "analysis": result}


@app.post("/ocr/")
async def ocr_endpoint(file: UploadFile = File(...)):
    result = await extract_text(file)
    return {"status": "ok", "ocr": result}


@app.post("/audio/")
async def audio_endpoint(file: UploadFile = File(...)):
    result = await transcribe_audio(file)
    return {"status": "ok", "audio": result}


@app.get("/webdav/scan/")
async def webdav_scan():
    result = await scan_webdav()
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
