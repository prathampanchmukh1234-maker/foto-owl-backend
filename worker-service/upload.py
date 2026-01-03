import boto3, os, requests

s3 = boto3.client(
    "s3",
    endpoint_url="https://s3.us-west-002.backblazeb2.com",
    aws_access_key_id=os.getenv("B2_KEY_ID"),
    aws_secret_access_key=os.getenv("B2_APP_KEY"),
)

BUCKET = os.getenv("BUCKET_NAME")

def upload_image(url, name):
    data = requests.get(url).content
    s3.put_object(Bucket=BUCKET, Key=name, Body=data)
    return f"{BUCKET}/{name}"
