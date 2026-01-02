import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def ensure_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        name TEXT,
        google_drive_id TEXT,
        size BIGINT,
        mime_type TEXT,
        storage_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
