from fastapi import FastAPI
from pydantic import BaseModel
from importer import enqueue_images

app = FastAPI(title="Foto-Owl Importer Service")

class DriveRequest(BaseModel):
    folder_url: str


@app.post("/import")
def import_images(data: DriveRequest):
    count = enqueue_images(data.folder_url)
    return {"status": "queued", "images": count}
