from aiogram import Router, types
from aiogram.filters import BaseFilter
from openai import AsyncOpenAI
import os

router = Router()
openai_key = os.getenv("OPENAI_API_KEY")
openai_client = AsyncOpenAI(api_key=openai_key)

# Фильтр: реагирует только на упоминания бота
class MentionFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.entities is not None and any(
            e.type == "mention" and message.text[e.offset:e.offset+e.length].lower() == f"@{(await message.bot.me()).username.lower()}"
            for e in message.entities
        )

@router.message(MentionFilter())
async def handle_mention(message: types.Message):
    user_text = message.text.replace(f"@{(await message.bot.me()).username}", "").strip()

    response = await openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты helpful assistant в Telegram-чате по Узбекистану. Люди ищут специалистов и ты помогаешь им найти нужных, используя базу и контекст."},
            {"role": "user", "content": user_text}
        ]
    )

    await message.reply(response.choices[0].message.content)
gpt_search = router
