import asyncio
import os



from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker
from handlers.user_private import user_private_router
from handlers.admin_private import admin_router

bot = Bot(token=os.getenv('TOKEN'))
# id пользователей с ролью админа
bot.my_admins_list = [1877142134]

dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

# подключаем наши роутеры
dp.include_router(user_private_router)
dp.include_router(admin_router)


async def on_startup(bot):
    await create_db()


async def on_shutdown(bot):
    print('Завершение работы бота!')


async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('')