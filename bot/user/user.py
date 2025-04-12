from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.dao import UserDAO
from bot.user.schemas import TelegramIDModel, UserModel
from bot.user.kbs import main_user_kb

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession):
    user_id = message.from_user.id

    user_info = await UserDAO.find_one_or_none(
        session = session_with_commit,
        filters = TelegramIDModel(telegram_id=user_id)
    )

    if user_info:
        return await message.answer(
            f"👋 Привет, {message.from_user.full_name}! Выберите необходимое действие",
            reply_markup=main_user_kb(user_id)
        )
    
    values = UserModel (
        telegram_id = user_id,
        username = message.from_user.username,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name
    )

    await UserDAO.add(session = session_with_commit, values=values)
    await message.answer(f"🎆🎇🎈🎉 <b>Благодарим за регистрацию!</b> Теперь выберите необходимое действие.",
                         reply_markup=main_user_kb(user_id))