import redis
import json
from drive_fetcher import fetch_images_from_drive

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE_NAME = "image_import_queue"

def enqueue_images(folder_url):
    images = fetch_images_from_drive(folder_url)

    print("Fetched images:", images)

    for img in images:
        redis_client.rpush(QUEUE_NAME, json.dumps(img))

    print("Queued", len(images), "images")
    return len(images)
