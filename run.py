import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from app.handlers.main import main_router
from app.handlers.admin import admin_router
from app.handlers.master_admin import master_router
from app.handlers.teacher import teacher_router
from app.handlers.student import student_router
from app.database.models import start_db



# Launching a bot, getting a token
async def main():
    start_db
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(master_router)
    dp.include_router(teacher_router)
    dp.include_router(student_router)
    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())