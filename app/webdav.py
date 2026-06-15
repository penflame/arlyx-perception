import httpx
import os

WEBDAV_URL = os.getenv("NEXTCLOUD_WEBDAV_URL")
WEBDAV_USER = os.getenv("NEXTCLOUD_USER")
WEBDAV_PASS = os.getenv("NEXTCLOUD_PASS")

async def scan_webdav():
    if not WEBDAV_URL or not WEBDAV_USER or not WEBDAV_PASS:
        return {"error": "Missing WebDAV credentials"}

    async with httpx.AsyncClient(auth=(WEBDAV_USER, WEBDAV_PASS)) as client:
        try:
            r = await client.request(
                "PROPFIND",
                WEBDAV_URL,
                headers={"Depth": "1"},
                timeout=10
            )
            return {"status": "ok", "raw_xml": r.text}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
