# handlers/gemini.py
from aiogram import Router, types, F
import google.generativeai as genai
import os

router = Router()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

@router.message(F.text.startswith("/gemini"))
async def gemini_command(message: types.Message):
    user_input = message.text.removeprefix("/gemini").strip()

    if not user_input:
        await message.reply("🔹 Напиши вопрос после /gemini — например: /gemini чем отличается frontend от backend")
        return

    await message.answer("⏳ Думаю...")

    try:
        response = model.generate_content(user_input)
        await message.reply(response.text)
    except Exception as e:
        await message.reply("⚠️ Ошибка при обращении к Gemini.")
        print("Gemini error:", e)
