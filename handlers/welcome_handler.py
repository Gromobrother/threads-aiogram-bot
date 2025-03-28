from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from aiogram import Bot

router = Router()

@router.chat_member()
async def welcome_new_member(event: ChatMemberUpdated, bot: Bot):
    if event.new_chat_member.status != "member":
        return

    welcome_text = (
        "👋 Добро пожаловать в группу!\n\n"
        "Чтобы зарегистрироваться и тебя могли найти по профессии, нажми кнопку ниже:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Зарегистрироваться", switch_inline_query_current_chat="/reg ")]
        ]
    )

    await bot.send_message(
        chat_id=event.chat.id,
        text=welcome_text,
        reply_markup=keyboard
    )

welcome_router = router
