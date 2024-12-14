from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from app.algorithms import token_generator
import app.database.requests as db
import app.keyboards as kb

storage = MemoryStorage()
admin_router = Router()
router = admin_router

class Add_group(StatesGroup):
    add = State()

class Add_student(StatesGroup):
    add = State()

class Add_subject(StatesGroup):
    add = State()




# --------------------------------------------------------------------------------------------------------------------------------------------
# creating a new group by admin



@router.message(F.text == 'Создать новую группу')
async def new_group(message: Message, state: FSMContext):
    admin = await db.admin_initialization(message.from_user.id)
    if admin == 'Ok':
        await message.answer('Введите название новой группы')
        await state.set_state(Add_group.add)
    elif admin == 'None':
        await message.answer('Не извесная команда')


@router.message(Add_group.add)
async def add(message: Message, state: FSMContext):
    group_name = message.text
    school = await db.get_school(message.from_user.id)
    await db.insert_new_group(school, group_name)
    await message.answer(f'Вы успешно добавили новую группу {group_name}')
    await state.clear()

# --------------------------------------------------------------------------------------------------------------------------------------------
# creating a new teacher token by admin




@router.message(F.text == 'Создать токен учителя')
async def new_teacher(message: Message):
    admin = await db.admin_initialization(message.from_user.id)
    if admin == 'Ok':
        token = await token_generator()
        school = await db.get_school(message.from_user.id)
        await message.answer(f'Новый токен админа: {str(token)}')
        await db.insert_new_teacher_token(school, token)
    elif admin == 'None':
        await message.answer('Не извесная команда')

# --------------------------------------------------------------------------------------------------------------------------------------------
# creating a new student token by admin




@router.message(F.text == 'Создать токен ученика')
async def new_student(message: Message, state: FSMContext):
    admin = await db.admin_initialization(message.from_user.id)
    if admin == 'Ok':
        school = await db.get_school(message.from_user.id)
        groups = await db.get_groups(school)
        keyb = await kb.group_generator_kb(groups)
        await message.answer('Выберите группу ученика:', reply_markup=keyb)
        await state.set_state(Add_student.add)
    elif admin == 'None':
        await message.answer('Не извесная команда')

@router.callback_query(Add_student.add)
async def new_student_token(call: CallbackQuery, state: FSMContext):
    school = await db.get_school(call.from_user.id)
    group = call.data
    token = await token_generator()
    await call.message.answer(f'Новый токен ученика группы: {group}, - {token}')
    await db.insert_new_student_token(school, group, token)


# --------------------------------------------------------------------------------------------------------------------------------------------
# creating a new subject by admin

@router.message(F.text == 'Добавить предмет')
async def new_group(message: Message, state: FSMContext):
    admin = await db.admin_initialization(message.from_user.id)
    if admin == 'Ok':
        await message.answer('Введите название нового предмета')
        await state.set_state(Add_subject.add)
    elif admin == 'None':
        await message.answer('Не извесная команда')


@router.message(Add_subject.add)
async def add(message: Message, state: FSMContext):
    subject_name = message.text
    school = await db.get_school(message.from_user.id)
    await db.insert_new_subject(school, subject_name)
    await message.answer(f'Вы успешно добавили новый предмет {subject_name}')
    await state.clear()