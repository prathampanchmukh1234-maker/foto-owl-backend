import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            name TEXT,
            google_drive_id TEXT,
            size BIGINT,
            mime_type TEXT,
            storage_path TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_metadata(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO images (name, google_drive_id, size, mime_type, storage_path)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["name"],
        data["google_drive_id"],
        data["size"],
        data["mime_type"],
        data["storage_path"]
    ))

    conn.commit()
    cur.close()
    conn.close()
