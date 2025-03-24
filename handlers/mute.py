# handlers/mute.py

from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
from datetime import datetime, timedelta
import asyncpg
import os

router = Router()

MUTE_WORDS = ['мат1', 'мат2', 'мат3']  # заменишь на реальные слова
MUTE_TIMES = [5, 30, 60, 10080, 43200]  # в минутах

@router.message(F.text.lower().filter(lambda text: any(word in text for word in MUTE_WORDS)))
async def mute_user(message: Message):
    user_id = message.from_user.id
    now = datetime.now()

    try:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        result = await conn.fetchrow("SELECT count, last_mute FROM mutes WHERE user_id = $1", user_id)

        count = 1
        if result:
            last_mute = result["last_mute"]
            if (now - last_mute).days < 3:
                count = result["count"] + 1

        if count > 5:
            count = 5

        mute_minutes = MUTE_TIMES[count - 1]
        until = now + timedelta(minutes=mute_minutes)

        await conn.execute("""
            INSERT INTO mutes (user_id, count, last_mute)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id)
            DO UPDATE SET count = $2, last_mute = $3;
        """, user_id, count, now)

        await conn.close()

        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until
        )

        await message.reply(f"🔇 Мут на {mute_minutes} минут за плохие слова.")
    except Exception as e:
        await message.answer("Произошла ошибка при муте.")
        print(f"Ошибка мата: {e}")
