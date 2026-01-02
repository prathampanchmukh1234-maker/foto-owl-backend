import redis, json
from drive_fetcher import fetch_images_from_drive

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

QUEUE_NAME = "image_import_queue"

def enqueue_images(folder_url):
    images = fetch_images_from_drive(folder_url)

    for image in images:
        redis_client.rpush(QUEUE_NAME, json.dumps(image))

    return len(images)
