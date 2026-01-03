from fastapi import FastAPI
from pydantic import BaseModel
from drive_fetcher import fetch_images_from_drive

app = FastAPI()

class DriveRequest(BaseModel):
    folder_url: str

@app.post("/import")
def import_images(data: DriveRequest):
    images = fetch_images_from_drive(data.folder_url)
    return {
        "status": "queued",
        "images": len(images),
        "files": images
    }
