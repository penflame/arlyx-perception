from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import httpx
import os

from vision import analyze_image

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
