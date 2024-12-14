from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import app.database.requests as db
import app.keyboards as kb
from app.algorithms import token_generator
from dotenv import load_dotenv
import os

load_dotenv()
MASTER_ADMIN_ID=int(os.getenv('MASTER_ADMIN'))

master_router = Router()
router = master_router

@router.message(F.text == '/master_admin')
async def cmd_start(message: Message):
    if message.from_user.id == MASTER_ADMIN_ID:
        await message.answer('Привет, супер админ', reply_markup=kb.main_master_admin)
    else:
        await message.answer('Неизвестная команда')


@router.message(F.text == 'Выдать токен админа')
async def cmd_start(message: Message):
    if message.from_user.id == MASTER_ADMIN_ID:
        token = await token_generator()
        await message.answer(f'Новый токен админа: {str(token)}')
        await db.insert_new_admin_token(token)
    else:
        await message.answer('Неизвестная команда')