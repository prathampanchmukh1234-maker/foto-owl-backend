import redis
import json
import time
import requests
import psycopg2
import os
from s3_uploader import upload_to_s3
from db import create_tables, save_metadata

REDIS_HOST = "redis"
REDIS_PORT = 6379
QUEUE_NAME = "image_import_queue"

DATABASE_URL = os.getenv("DATABASE_URL")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print("Database is ready")
            break
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(3)

def process_queue():
    _, image_data = redis_client.blpop(QUEUE_NAME)
    image = json.loads(image_data)

    file_id = image["id"]
    download_url = f"https://drive.google.com/uc?id={file_id}"

    response = requests.get(download_url, timeout=15)
    response.raise_for_status()

    s3_path = upload_to_s3(response.content, image["name"])

    save_metadata({
        "name": image["name"],
        "google_drive_id": file_id,
        "size": image.get("size", 0),
        "mime_type": image["mimeType"],
        "storage_path": s3_path
    })

    print(f"Processed image: {image['name']}")

def main():
    print("Worker service started. Listening for image import jobs...")

    wait_for_db()
    create_tables()

    while True:
        try:
            process_queue()
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
