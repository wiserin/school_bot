from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
import app.database.requests as db



role_kb = [
    [KeyboardButton(text='Ученик')],
    [KeyboardButton(text='Учитель')],
    [KeyboardButton(text='Администратор')]
]
role = ReplyKeyboardMarkup(keyboard=role_kb,
                           resize_keyboard=True)


main_admin_kb = [
    [KeyboardButton(text='Создать новую группу'),
     KeyboardButton(text='Посмотреть доступные группы')],
    [KeyboardButton(text='Добавить ДЗ'),
     KeyboardButton(text='Сделать рассылку')],
    [KeyboardButton(text='Добавить предмет'),
     KeyboardButton(text='Удалить предмет')],
    [KeyboardButton(text='Создать токен учителя')],
    [KeyboardButton(text='Создать токен ученика')]
]
main_admin = ReplyKeyboardMarkup(keyboard=main_admin_kb,
                                 resize_keyboard=True)

main_teacher_kb = [
    [KeyboardButton(text='Добавить ДЗ')],
    [KeyboardButton(text='Сделать рассылку')]
]
main_teacher = ReplyKeyboardMarkup(keyboard=main_teacher_kb,
                                      resize_keyboard=True)

main_student_kb = [
    [KeyboardButton(text='Доступные ДЗ')]
]
main_student = ReplyKeyboardMarkup(keyboard=main_student_kb,
                                   resize_keyboard=True)

main_master_admin_kb = [
    [KeyboardButton(text='Выдать токен админа')],
    [KeyboardButton(text='Получить список админов'),
     KeyboardButton(text='Удалить админа')]
]
main_master_admin = ReplyKeyboardMarkup(keyboard=main_master_admin_kb,
                                        resize_keyboard=True)

ask_kb = [
    [KeyboardButton(text='Пропустить')]
]
ask = ReplyKeyboardMarkup(keyboard=ask_kb,
                          resize_keyboard=True)


async def group_generator_kb(data):
    kb = []
    for i in data:
        kb.append([InlineKeyboardButton(text=i, callback_data=i)])
    new_kb = InlineKeyboardMarkup(inline_keyboard=kb)
    return new_kb

async def student_generator_kb(data):
    kb = []
    for i in data:
        kb.append([KeyboardButton(text=i)])
    kb.append([KeyboardButton(text='Вернуться в главное меню')])
    new_kb = ReplyKeyboardMarkup(keyboard=kb, 
                                 resize_keyboard=True)
    return new_kb

async def days_generator_kb(data):
    kb = []
    whole = []
    call = []
    count = 0
    for i in data.keys():
        whole.append(data[i])
        call.append(i)

    for i in range(0, 6):
        kb.append(
            [InlineKeyboardButton(text=whole[count], callback_data=call[count]),
             InlineKeyboardButton(text=whole[count + 1], callback_data=call[count + 1]),
             InlineKeyboardButton(text=whole[count + 2], callback_data=call[count + 2]),
             InlineKeyboardButton(text=whole[count + 3], callback_data=call[count + 3]),
             InlineKeyboardButton(text=whole[count + 4], callback_data=call[count + 4])
            ]
        )
        count += 5
    new_kb = InlineKeyboardMarkup(inline_keyboard=kb)
    return new_kb


async def done(HW_id):
    kb = [
        [InlineKeyboardButton(text='Выполнено', callback_data=f'done{str(HW_id)}')]
    ]

    new_kb = InlineKeyboardMarkup(inline_keyboard=kb)
    return new_kb




    
