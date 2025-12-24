import boto3
import os
from uuid import uuid4

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET = os.getenv("S3_BUCKET_NAME")

def upload_to_s3(file_bytes, filename):
    key = f"images/{uuid4()}-{filename}"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType="image/jpeg"
    )

    print("Uploaded to MinIO:", key)
    return f"s3://{BUCKET}/{key}"
