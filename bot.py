### bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from handlers import registration, gpt, search, mute
from database.db import create_tables

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем роутеры
    dp.include_routers(
        registration.router,
        gpt.router,
        search.router,
        mute.router
    )

    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
