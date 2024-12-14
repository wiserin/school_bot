from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.database.requests as db
import app.keyboards as kb


storage = MemoryStorage()
student_router = Router()
router = student_router

class Get_HW(StatesGroup):
    finish = State()

@router.message(F.text == 'Доступные ДЗ')
async def get_HW(message: Message, state: FSMContext):
    school = await db.get_school(message.from_user.id)
    groups = await db.get_subjects(school)
    keyb = await kb.student_generator_kb(groups)
    await message.answer('Виберете предмет, по которому хотите посмотреть ДЗ:', reply_markup=keyb)
    await state.set_state(Get_HW.finish)

@router.message(Get_HW.finish)
async def HW(message: Message, state: FSMContext):
    school = await db.get_school(message.from_user.id)
    group = await db.get_user_group(message.from_user.id)
    subject = message.text
    data = await db.get_HW(school, group, subject, message.from_user.id)

    if message.text == 'Вернуться в главное меню':
        await message.answer('@#@#@#@#@', reply_markup=kb.main_student)

    for i in data:
        id = i['id']
        sub = i['sub']
        photo = i['photo']
        deadline = i['deadline']

        keyb = await kb.done(id)

        if photo == 'None':
            await message.answer(text=f'Домашнее задание: {sub}\n\n'
                                 f'Выполнить до: {deadline}', parse_mode='html', reply_markup=keyb)
        else:
            await message.answer_photo(photo=photo,
                                       caption=f'Домашнее задание: {sub}\n\n'
                                       f'Выполнить до: {deadline}', parse_mode='html', reply_markup=keyb)
    await message.answer(f'Это все задания по {subject}', reply_markup=kb.main_student)
            
    await state.clear()


@router.callback_query(lambda callback_query: callback_query.data.startswith('done'))
async def done(call: CallbackQuery):
    id = int(call.data.removeprefix('done'))
    await db.done_HW(id, call.from_user.id)
    await call.message.delete()
    print(id)