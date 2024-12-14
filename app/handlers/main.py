from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import app.database.requests as db
import app.keyboards as kb


storage = MemoryStorage()
main_router = Router()
router = main_router


class Info(StatesGroup):
    finish = State()

class Admin(StatesGroup):
    token_verification = State()
    add_school = State()

class Teacher(StatesGroup):
    token_verification = State()

class Student(StatesGroup):
    token_verification = State()



# Handler of the start command, user initialization
@router.message(F.text == '/start')
async def cmd_start(message: Message, state: FSMContext):
    entrance = await db.initialization(message.from_user.id)

    if entrance == 'None':
        await message.answer(text='Не нашел вас среди пользователей.\n'
                            'Пожалуйста, выберите вашу роль и продолжите регистрацию', parse_mode='html', reply_markup=kb.role)
        await state.set_state(Info.finish)

    elif entrance == 'admin':
        await message.answer('Добро пожаловать, администратор.', reply_markup=kb.main_admin)
    
    elif entrance == 'teacher':
        await message.answer('Добро пожаловать, учитель!', reply_markup=kb.main_teacher)
    
    elif entrance == 'student':
        await message.answer('Добро пожаловать, ученик!', reply_markup=kb.main_student)






# Registration of the user, if he isn't already registered
@router.message(Info.finish)
async def cmd(message: Message, state: FSMContext):

    if message.text == 'Ученик':
        await state.clear()
        await message.answer('Введите токен, полученный от админа', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Student.token_verification)

    elif message.text == 'Учитель':
        await state.clear()
        await message.answer('Введите токен, полученный от админа', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Teacher.token_verification)

    elif message.text == 'Администратор':
        await state.clear()
        await message.answer('Введите токен, полученный от мастер-админа', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Admin.token_verification)

    else:
        await message.answer('Выбери роль')
        await state.set_state(Info.finish)
    



# --------------------------------------------------------------------------------------------------------------------------------------------
# Registration and verification of the admin, adding his institution

@router.message(Admin.token_verification)
async def token_ver(message: Message, state: FSMContext):
    check = await db.check_admin_token(message.text)

    if check == 'Ok':
        await message.answer('Токен найден. Введите название вашего учереждения:')
        await state.set_state(Admin.add_school)

    elif check == 'None':
        await state.clear()
        await message.answer('Токен не найден.', reply_markup=kb.role)
        await state.set_state(Info.finish)
    
    
@router.message(Admin.add_school)
async def school(message: Message, state: FSMContext):
    school = message.text

    await message.answer(f'Вы добавили школу {school}', reply_markup=kb.main_admin)
    await db.insert_school(school, message.from_user.id, message.from_user.first_name)
    await db.insert_new_user(message.from_user.id, message.from_user.first_name,
                             school, 'admin', None)
    await state.clear()

# --------------------------------------------------------------------------------------------------------------------------------------------
# Registration and verification of the teacher, adding his institution



@router.message(Teacher.token_verification)
async def token_ver(message: Message, state: FSMContext):
    check = await db.check_teacher_token(message.text)

    if check == 'None':
        await state.clear()
        await message.answer('Токен не найден.', reply_markup=kb.role)
        await state.set_state(Info.finish)

    else:
        school = check
        await db.insert_new_user(message.from_user.id, message.from_user.first_name,
                                 school, 'teacher', None)
        
        await message.answer('Вы успешно зарегистрированы!', reply_markup=kb.main_teacher)
        await state.clear()
        
# --------------------------------------------------------------------------------------------------------------------------------------------
# Registration and verification of the student, adding his institution





@router.message(Student.token_verification)
async def token_ver(message: Message, state: FSMContext):
    check = await db.check_student_token(message.text)

    if check == 'None':
        await state.clear()
        await message.answer('Токен не найден.', reply_markup=kb.role)
        await state.set_state(Info.finish)

    else:
        school = check['school']
        group = check['group']
        await db.insert_new_user(message.from_user.id, message.from_user.first_name,
                                 school, 'student', group)
        
        await message.answer('Вы успешно зарегистрированы!', reply_markup=kb.main_student)
        await state.clear()

# --------------------------------------------------------------------------------------------------------------------------------------------

@router.message(F.text == '/day')
async def send(message: Message):
    await message.answer('ad', reply_markup=kb.day)

@router.message()
async def nothing(message: Message):
    await message.answer('Неизвесная команда')