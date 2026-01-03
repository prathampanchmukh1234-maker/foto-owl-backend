import os, re, requests, boto3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT"),
    aws_access_key_id=os.getenv("S3_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET"),
)

BUCKET = os.getenv("S3_BUCKET")

class ImportData(BaseModel):
    folder_url: str

def extract_id(url):
    m = re.search(r"folders/([^/?]+)", url)
    return m.group(1)

def fetch_images(folder_id):
    r = requests.get("https://www.googleapis.com/drive/v3/files", params={
        "q": f"'{folder_id}' in parents and mimeType contains 'image/'",
        "fields": "files(id,name)",
        "key": os.getenv("GOOGLE_API_KEY")
    }).json()
    return r.get("files", [])

@app.post("/import")
def import_images(data: ImportData):
    files = fetch_images(extract_id(data.folder_url))
    count = 0
    for f in files:
        img = requests.get(f"https://drive.google.com/uc?export=download&id={f['id']}").content
        s3.put_object(Bucket=BUCKET, Key=f["name"], Body=img)
        count += 1
    return {"status":"success","images":count}

@app.get("/images")
def list_images():
    return [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET).get("Contents",[])]
