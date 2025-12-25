from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
import os
import requests

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class DriveRequest(BaseModel):
    folder_url: str

def extract_folder_id(url: str):
    return url.split("folders/")[1].split("?")[0]

@router.post("/import/google-drive")
def import_images(data: DriveRequest):
    try:
        folder_id = extract_folder_id(data.folder_url)

        drive_api = "https://www.googleapis.com/drive/v3/files"
        params = {
            "q": f"'{folder_id}' in parents and mimeType contains 'image/'",
            "fields": "files(id,name,mimeType,size)",
            "key": GOOGLE_API_KEY
        }

        r = requests.get(drive_api, params=params)
        r.raise_for_status()
        files = r.json().get("files", [])

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        for f in files:
            cur.execute("""
                INSERT INTO images (name, google_drive_id, size, mime_type, storage_path)
                VALUES (%s,%s,%s,%s,%s)
            """, (
                f["name"],
                f["id"],
                f.get("size", 0),
                f["mimeType"],
                f"google-drive/{f['id']}"
            ))

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "imported", "images": len(files)}

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
                "name": r[0],
                "google_drive_id": r[1],
                "size": r[2],
                "mime_type": r[3],
                "storage_path": r[4]
            } for r in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
