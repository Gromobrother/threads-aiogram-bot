import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import BotCommand
from dotenv import load_dotenv

from handlers import registration, gpt, search, mute
from handlers.gpt_search import gpt_search
from handlers.gpt_command import router as gpt_command
from handlers.welcome_handler import welcome_router
from database.db import create_tables

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def on_user_join(event: types.ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status == "member":
        await bot.send_message(
            chat_id=event.chat.id,
            text=(
                f"👋 Добро пожаловать, {event.new_chat_member.user.first_name}!\n"
                "Чтобы зарегистрироваться, используй команду:\n\n👉 /reg\n\n"
                "Это поможет найти тебя по профессии 😉"
            )
        )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Меню команд бота
    await bot.set_my_commands([
        BotCommand(command="reg", description="Зарегистрироваться в базе"),
        BotCommand(command="find", description="Найти специалиста"),
        BotCommand(command="gpt", description="Задать вопрос ИИ"),
        BotCommand(command="help", description="Помощь по боту"),
    ])

    # Приветствие при вступлении в чат
    dp.chat_member.register(on_user_join, ChatMemberUpdatedFilter(JOIN_TRANSITION))

    # Подключение роутеров
    dp.include_routers(
        registration,
        gpt,
        search,
        mute,
        gpt_search,
        gpt_command,
        welcome_router  # ✅ кнопочное приветствие
    )

    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
