from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.database.requests as db
import app.keyboards as kb
from app.date import Date

date = Date()

storage = MemoryStorage()
teacher_router = Router()
router = teacher_router

class Add_HW(StatesGroup):
    get_subject = State()
    get_HW_sub = State()
    ask_photo = State()
    get_photo = State()
    deadline = State()
    finish = State()


@router.message(F.text == 'Добавить ДЗ')
async def new_group(message: Message, state: FSMContext):
    teacher = await db.teacher_initialization(message.from_user.id)
    if teacher == 'Ok':
        school = await db.get_school(message.from_user.id)
        groups = await db.get_groups(school)
        keyb = await kb.group_generator_kb(groups)
        await message.answer('Выберите для кого ДЗ', reply_markup=keyb)
        await state.set_state(Add_HW.get_subject)

    elif teacher == 'None':
        admin = await db.admin_initialization(message.from_user.id)
        if admin == 'Ok':
            school = await db.get_school(message.from_user.id)
            groups = await db.get_groups(school)
            keyb = await kb.group_generator_kb(groups)
            await message.answer('Выберите для кого ДЗ', reply_markup=keyb)
            await state.set_state(Add_HW.get_subject)
        elif admin == 'None':
            await message.answer('Не извесная команда')


@router.callback_query(Add_HW.get_subject)
async def add(call: CallbackQuery, state: FSMContext):
    await state.update_data(group=call.data)
    school = await db.get_school(call.from_user.id)
    groups = await db.get_subjects(school)
    keyb = await kb.group_generator_kb(groups)
    await call.message.answer('Выберите предмет ДЗ', reply_markup=keyb)
    await state.set_state(Add_HW.get_HW_sub)

@router.callback_query(Add_HW.get_HW_sub)
async def add(call: CallbackQuery, state: FSMContext):
    await state.update_data(subject=call.data)
    await call.message.answer('Введите описание ДЗ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Add_HW.ask_photo)

@router.message(Add_HW.ask_photo)
async def add(message: Message, state: FSMContext):
    await state.update_data(HW_sub=message.text)
    await message.answer('Вам нужно фото? Если нет, просто нажмите пропустить', reply_markup=kb.ask)
    await state.set_state(Add_HW.deadline)

@router.message(lambda message: not message.photo and message.text != 'Пропустить', Add_HW.deadline)
async def add_item_photo(message: Message, state: FSMContext):
    await message.answer('Иди нахрен это не фото')

@router.message(Add_HW.deadline)
async def add(message: Message, state: FSMContext):

    if message.text == 'Пропустить':
        await state.update_data(photo='None')
        dates = date.date_count(30)
        key_b = await kb.days_generator_kb(dates)
        await message.answer('Выберите дату дедлайна', reply_markup=key_b)
        await state.set_state(Add_HW.finish)

    else:
        await state.update_data(photo=message.photo[-1].file_id)
        dates = date.date_count(30)
        key_b = await kb.days_generator_kb(dates)
        await message.answer('Выберите дату дедлайна', reply_markup=key_b)
        await state.set_state(Add_HW.finish)

@router.callback_query(Add_HW.finish)
async def add(call: CallbackQuery, state: FSMContext):
    await state.update_data(deadline=call.data)
    data = await state.get_data()
    school = await db.get_school(call.from_user.id)
    group = data['group']
    subject = data['subject']
    HW_sub = data['HW_sub']
    photo = data['photo']
    deadline = data['deadline']
    await db.insert_hw(school, group, subject, 'None', HW_sub, photo, deadline)
    role = await db.get_role(call.from_user.id)
    
    if role == 'admin':
        await call.message.answer('Готово', reply_markup=kb.main_admin)
    elif role == 'teacher':
        await call.message.answer('Готово', reply_markup=kb.main_teacher)
    await state.clear()

