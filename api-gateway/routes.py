from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
import os
import requests

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
IMPORTER_URL = os.getenv("IMPORTER_URL", "https://foto-owl-api.onrender.com/import")

class DriveRequest(BaseModel):
    folder_url: str

@router.post("/import/google-drive")
def import_images(data: DriveRequest):
    try:
        response = requests.post(
            IMPORTER_URL,
            json={"folder_url": data.folder_url},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images")
def get_images():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT name, google_drive_id, size, mime_type, storage_path
            FROM images
            ORDER BY id DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "name": row[0],
                "google_drive_id": row[1],
                "size": row[2],
                "mime_type": row[3],
                "storage_path": row[4]
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
