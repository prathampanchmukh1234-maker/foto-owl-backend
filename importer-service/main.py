from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from importer import enqueue_images

app = FastAPI()

class DriveRequest(BaseModel):
    folder_url: str

@app.post("/import")
def import_images(data: DriveRequest):
    try:
        count = enqueue_images(data.folder_url)
        return {"status": "queued", "images": count}
    except Exception as e:
        print("IMPORTER ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
