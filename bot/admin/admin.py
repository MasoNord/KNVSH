from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from bot.config import admins
from bot.admin.kbs import admin_kb, main_kb

admin_router = Router()

@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(admins))
async def start_admin(call: CallbackQuery):
    await call.answer('Доступ в админ-панель разрешен!')
    await call.message.edit_text(
        text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
        reply_markup=main_kb()
    )