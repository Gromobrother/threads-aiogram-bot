# database/db.py

import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

async def create_tables():
    conn = await asyncpg.connect(DB_URL)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            username TEXT,
            job TEXT,
            district TEXT,
            fav_spot TEXT
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS mutes (
            user_id BIGINT PRIMARY KEY,
            count INTEGER,
            last_mute TIMESTAMP
        );
    """)

    await conn.close()
