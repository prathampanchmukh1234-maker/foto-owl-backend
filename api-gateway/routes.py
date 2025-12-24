from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

class DriveRequest(BaseModel):
    folder_url: str

@router.post("/import/google-drive")
def import_images(data: DriveRequest):
    try:
        r = requests.post(
            "http://importer-service:8000/import",
            json={"folder_url": data.folder_url},
            timeout=30
        )

        if r.text.strip() == "":
            raise Exception("Importer returned empty response")

        result = r.json()

        return {
            "status": result.get("status"),
            "images": result.get("images", 0)
        }

    except Exception as e:
        print("API GATEWAY ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
