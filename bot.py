import asyncio
import logging
from handlers import registration, gpt, search, mute
from handlers.gpt_search import gpt_search
from handlers.gpt_command import router as gpt_command
from handlers.welcome_handler import router as welcome_handler
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from database.db import create_tables

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем все роутеры
    dp.include_routers(
        registration,
        gpt,
        search,
        mute,
        gpt_search,
        gpt_command,
        welcome_handler  # ✅ Обработчик новых участников
    )

    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
