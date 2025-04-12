import asyncio
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit
from bot.config import bot, admins, dp
from bot.admin.admin import admin_router
from bot.user.user import user_router

async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен 🥳')
        except:
            pass
    logging.info("Бот успешно запущен")

async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass
    await bot.session.close()
    logging.error("Бот остановлен!")


# чтобы запустить бота, через командную строку, с корневой папки запустить
# python -m bot.main

async def main():

    # Регистрация мидлварей
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())


    # Регистрация роутеров
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

        # Запуск бота в режиме long polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())