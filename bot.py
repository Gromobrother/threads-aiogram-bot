import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from dotenv import load_dotenv

from handlers import registration, gpt, search, mute
from handlers.gpt_search import gpt_search
from handlers.gpt_command import router as gpt_command
from database.db import create_tables

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Приветствие новых участников
async def on_user_join(event: types.ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == "member":
        await bot.send_message(
            chat_id=event.chat.id,
            text=(
                f"👋 Привет, {event.new_chat_member.user.first_name}!\n"
                "Чтобы зарегистрироваться, используй команду:\n\n👉 /reg\n\n"
                "Это поможет другим найти тебя по профессии 😉"
            )
        )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Слушаем вступление новых участников
    dp.chat_member.register(on_user_join, ChatMemberUpdatedFilter(JOIN_TRANSITION))

    # Подключаем все роутеры
    dp.include_routers(
        registration,
        gpt,
        search,
        mute,
        gpt_search,
        gpt_command  # ✅ это для /gpt
    )

    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
