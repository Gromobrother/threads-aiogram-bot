from aiogram import Router, types, F
from openai import AsyncOpenAI
import os

router = Router()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.message(F.text.startswith("/gpt"))
async def gpt_command(message: types.Message):
    user_input = message.text.removeprefix("/gpt").strip()

    if not user_input:
        await message.reply("🔹 Напиши вопрос после /gpt — например: /gpt кто такие дизайнеры")
        return

    await message.answer("⏳ Думаю...")

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты helpful Telegram-бот, помогаешь участникам группы, даёшь точные и дружелюбные ответы."},
                {"role": "user", "content": user_input},
            ]
        )
        reply = response.choices[0].message.content.strip()
        await message.reply(reply)

    except Exception as e:
        await message.reply("⚠️ Ошибка при обращении к GPT. Попробуй позже.")
        print("GPT error:", e)
