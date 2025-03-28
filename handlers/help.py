from aiogram import Router, types

router = Router()

@router.message(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "🧠 Доступные команды:\n"
        "/reg — Зарегистрироваться в базе\n"
        "/find — Найти специалиста\n"
        "/gpt — Задать вопрос ИИ (через Gemini)\n"
        "/help — Помощь по боту\n\n"
        "👋 После регистрации тебя смогут найти по профессии.\n"
        "📍 Пример: Иван, дизайнер, Юнусабад, парк Локомотив."
    )
