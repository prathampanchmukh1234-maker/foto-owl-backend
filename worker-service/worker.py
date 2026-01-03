from upload import upload_image
import psycopg2, os

DB = os.getenv("DATABASE_URL")

def main():
    images = [
        "https://picsum.photos/400",
        "https://picsum.photos/401",
        "https://picsum.photos/402"
    ]

    conn = psycopg2.connect(DB)
    cur = conn.cursor()

    for i, url in enumerate(images):
        path = upload_image(url, f"img{i}.jpg")
        cur.execute(
            "INSERT INTO images(name, storage_path) VALUES(%s,%s)",
            (f"img{i}.jpg", path)
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
