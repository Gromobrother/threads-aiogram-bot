from aiogram import Router, types
from aiogram.filters import BaseFilter
from openai import AsyncOpenAI
import os

# 📌 Обязательно создаём экземпляр Router
router = Router()

# ✅ Получаем API ключ из переменной окружения
openai_key = os.getenv("OPENAI_API_KEY")
openai_client = AsyncOpenAI(api_key=openai_key)

# 🔍 Фильтр: не команды и не боты
class FreeTextFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return bool(message.text) and not message.text.startswith("/") and not message.via_bot

# 📩 Обработчик свободных сообщений
@router.message(FreeTextFilter())
async def handle_free_text(message: types.Message):
    user_text = message.text

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты helpful assistant в Telegram-чате по Узбекистану. Люди ищут специалистов и ты помогаешь им найти нужных, используя базу и контекст."},
                {"role": "user", "content": user_text}
            ]
        )

        reply_text = response.choices[0].message.content.strip()
        await message.reply(reply_text)

    except Exception as e:
        await message.reply("Произошла ошибка при обращении к GPT 🛠️\n" + str(e))
