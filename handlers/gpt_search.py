from aiogram import Router, types
from aiogram.filters import BaseFilter
from openai import AsyncOpenAI
import os

router = Router()
openai_key = os.getenv("OPENAI_API_KEY")
openai_client = AsyncOpenAI(api_key=openai_key)

class FreeTextFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return not message.text.startswith("/") and not message.via_bot

@router.message(FreeTextFilter())
async def handle_free_text(message: types.Message):
    user_text = message.text

    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты helpful assistant в Telegram-чате по Узбекистану. Люди ищут специалистов и ты помогаешь им найти нужных, используя базу и контекст."},
            {"role": "user", "content": user_text}
        ]
    )

    await message.reply(response.choices[0].message.content)
