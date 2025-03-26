from aiogram import types, Router

router = Router()

@router.message()
async def welcome_new_members(message: types.Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_bot:
                continue
            await message.answer(
                f"👋 Привет, {member.full_name}!\n\n"
                "Чтобы другие участники знали, чем ты занимаешься, зарегистрируйся с помощью команды /reg\n\n"
                "Пример: Иван, программист, Юнусабад, парк Локомотив."
            )