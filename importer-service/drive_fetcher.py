import requests

SAMPLE_IMAGES = [
    {
        "id": "img1",
        "name": "sample1.jpg",
        "mimeType": "image/jpeg",
        "size": 234567,
        "url": "https://picsum.photos/400"
    },
    {
        "id": "img2",
        "name": "sample2.jpg",
        "mimeType": "image/jpeg",
        "size": 345678,
        "url": "https://picsum.photos/401"
    },
    {
        "id": "img3",
        "name": "sample3.jpg",
        "mimeType": "image/jpeg",
        "size": 456789,
        "url": "https://picsum.photos/402"
    }
]

def fetch_images_from_drive(folder_url):
    return SAMPLE_IMAGES
