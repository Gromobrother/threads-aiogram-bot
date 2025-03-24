# handlers/registration.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncpg
import os

router = Router()

# Состояния регистрации
class RegState(StatesGroup):
    waiting_for_data = State()

@router.message(F.text.startswith('/reg'))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Введите данные: Имя, профессия, район, любимый спот.\nПример: Иван, программист, Юнусабад, парк.")
    await state.set_state(RegState.waiting_for_data)

@router.message(RegState.waiting_for_data)
async def save_registration(message: Message, state: FSMContext):
    try:
        data = [x.strip() for x in message.text.split(',')]
        if len(data) != 4:
            await message.answer("Укажите все 4 элемента через запятую: имя, профессия, район, любимое место.")
            return

        name, job, district, fav_spot = data

        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
        await conn.execute("""
            INSERT INTO users (user_id, username, job, district, fav_spot)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id) DO UPDATE
            SET username = $2, job = $3, district = $4, fav_spot = $5;
        """, message.from_user.id, message.from_user.username, job, district, fav_spot)
        await conn.close()

        await message.answer(f"Спасибо, {name}! Вы зарегистрированы ✅")
        await state.clear()
    except Exception as e:
        await message.answer("Ошибка при регистрации.")
        print(f"Ошибка в регистрации: {e}")
