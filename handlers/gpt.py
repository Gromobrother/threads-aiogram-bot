# handlers/gpt.py

from aiogram import Router, F
from aiogram.types import Message
import openai
import os
from datetime import datetime, timedelta

router = Router()

# Лимиты
GPT_LIMIT = 100
gpt_count = 0
reset_time = datetime.now() + timedelta(days=1)

@router.message(F.text.lower().startswith("всезнайка помоги"))
async def handle_gpt_request(message: Message):
    global gpt_count, reset_time
    now = datetime.now()

    if now >= reset_time:
        gpt_count = 0
        reset_time = now + timedelta(days=1)

    if gpt_count >= GPT_LIMIT:
        await message.answer("😔 Лимит GPT-запросов исчерпан. Попробуй завтра.")
        return

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты умный помощник. Отвечай кратко и по делу."},
                {"role": "user", "content": message.text}
            ]
        )

        reply = response.choices[0].message.content.strip()
        await message.answer(reply)
        gpt_count += 1
    except Exception as e:
        await message.answer("Произошла ошибка при обращении к GPT.")
        print(f"GPT ошибка: {e}")
