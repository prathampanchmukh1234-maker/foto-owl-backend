import os
import requests
import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_KEY = os.getenv("S3_KEY")
S3_SECRET = os.getenv("S3_SECRET")
S3_BUCKET = os.getenv("S3_BUCKET")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{S3_ENDPOINT}",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

class ImportRequest(BaseModel):
    folder_url: str

def get_folder_id(url):
    return url.split("/")[-1]

@router.post("/import/google-drive")
def import_images(data: ImportRequest):
    folder_id = get_folder_id(data.folder_url)

    api = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents&fields=files(id,name,mimeType)&key={GOOGLE_API_KEY}"
    res = requests.get(api).json()

    count = 0
    for f in res.get("files", []):
        if "image" not in f["mimeType"]:
            continue

        download = f"https://www.googleapis.com/drive/v3/files/{f['id']}?alt=media&key={GOOGLE_API_KEY}"
        img = requests.get(download)

        s3.put_object(Bucket=S3_BUCKET, Key=f["name"], Body=img.content)
        count += 1

    return {"status": "queued", "images": count}
