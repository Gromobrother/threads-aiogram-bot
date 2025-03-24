# handlers/search.py

from aiogram import Router, F
from aiogram.types import Message
import asyncpg
import os

router = Router()

@router.message(F.text.lower().startswith("@threadstashkentbot"))
async def find_specialist(message: Message):
    query = message.text.lower().replace("@threadstashkentbot", "").strip()
    if not query:
        await message.answer("Кого ищем? Уточни профессию или навык.")
        return

    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        result = await conn.fetch("SELECT username, job FROM users WHERE job ILIKE $1", f"%{query}%")
        await conn.close()

        if result:
            response = "Вот кого я нашёл:\n" + "\n".join([f"@{r['username']} — {r['job']}" for r in result])
        else:
            response = f"Никого не нашёл по запросу: {query}"

        await message.answer(response)

    except Exception as e:
        await message.answer("Ошибка при поиске.")
        print(f"Поиск ошибка: {e}")
