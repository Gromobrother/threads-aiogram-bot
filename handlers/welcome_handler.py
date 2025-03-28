from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION

router = Router()

@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def welcome_new_member(event: types.ChatMemberUpdated, bot: types.Bot):
    chat_id = event.chat.id

    welcome_text = (
        "👋 Добро пожаловать в группу!\n\n"
        "Чтобы зарегистрироваться и тебя могли найти по профессии, нажми кнопку ниже:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Зарегистрироваться", switch_inline_query_current_chat="/reg ")]
        ]
    )

    await bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=keyboard)
