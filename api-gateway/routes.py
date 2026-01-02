from fastapi import APIRouter
from pydantic import BaseModel
import psycopg2, os, requests

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
IMPORTER_URL = os.getenv("IMPORTER_URL")

class DriveRequest(BaseModel):
    folder_url: str


def ensure_tables():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        name TEXT,
        google_drive_id TEXT,
        size BIGINT,
        mime_type TEXT,
        storage_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


@router.post("/import/google-drive")
def import_images(data: DriveRequest):
    ensure_tables()

    response = requests.post(
        f"{IMPORTER_URL}/import",
        json={"folder_url": data.folder_url},
        timeout=120
    )

    return response.json()


@router.get("/images")
def get_images():
    ensure_tables()

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT name, google_drive_id, size, mime_type, storage_path
        FROM images ORDER BY id DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [{
        "name": r[0],
        "google_drive_id": r[1],
        "size": r[2],
        "mime_type": r[3],
        "storage_path": r[4]
    } for r in rows]
