from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import (Base, User, Bank, Admin_tokens, Teacher_tokens,
                                  Student_tokens, Schools, Groups, HW, Subjects)
import asyncio

engine = create_engine('sqlite:///bot.db')

session = sessionmaker(bind=engine)
s = session()




# initializing the user in the database
# if the user is in the database, returns his role
async def initialization(tg_id):
    user = s.query(User).filter(User.user_tg_id == tg_id).one_or_none()
    if user == None:
        return 'None'
    else:
        role = ''
        for user_role in s.query(User.role).filter(User.user_tg_id == tg_id):
            r = user_role[0]
            role = ''.join(r)
        print(role)
        return role
    s.commit()




# initializating the admin in the database
async def admin_initialization(id):
    admin = s.query(User).filter(User.user_tg_id == id).filter(User.role == 'admin').one_or_none()
    if admin == None:
        return 'None'
    else:
        return 'Ok'
    s.commit()


async def teacher_initialization(id):
    admin = s.query(User).filter(User.user_tg_id == id).filter(User.role == 'teacher').one_or_none()
    if admin == None:
        return 'None'
    else:
        return 'Ok'
    s.commit()



# adding a new admin token by the master admin to the database
async def insert_new_admin_token(token):
    new_token = Admin_tokens(tokens=token)
    s.add(new_token)
    s.commit()



async def insert_new_teacher_token(teacher_school, teacher_token):
    new_token = Teacher_tokens(school=teacher_school, token=teacher_token)
    s.add(new_token)
    s.commit()




async def insert_new_student_token(token_school, token_group, user_roken):
    new_token = Student_tokens(school=token_school, group=token_group, token=user_roken)
    s.add(new_token)
    s.commit()

async def insert_new_subject(subject_school, school_subject):
    new_subject = Subjects(school=subject_school, subject=school_subject)
    s.add(new_subject)
    s.commit()


# verification of the admin token during registration
async def check_admin_token(input_token):
    token = s.query(Admin_tokens).filter(Admin_tokens.tokens == input_token).one_or_none()
    if token == None:
        return 'None'
    else:
        return 'Ok'
    s.commit()




# verification of the teacher token during registration
async def check_teacher_token(input_token):
    token = s.query(Teacher_tokens).filter(Teacher_tokens.token == input_token).one_or_none()
    if token == None:
        return 'None'
    else:
        teacher_school = ''
        for school in s.query(Teacher_tokens.school).filter(Teacher_tokens.token == input_token):
            r = school[0]
            teacher_school = ''.join(r)
        return teacher_school
        s.commit()




async def check_student_token(input_token):
    token = s.query(Student_tokens).filter(Student_tokens.token == input_token).one_or_none()
    if token == None:
        return 'None'
    else:
        data = {}
        for student_data in s.query(Student_tokens.school, Student_tokens.group).filter(Student_tokens.token == input_token):
            data['school'] = student_data[0]
            data['group'] = student_data[1]
            print(data)
        return data




# adding a new institution when registering a new admin
async def insert_school(school_name, admin_tg_id, admin_tg_name):

    new_school = Schools(name=school_name, admin_id=admin_tg_id, admin_name=admin_tg_name)
    s.add(new_school)
    s.commit()



# adding information about a new user
async def insert_new_user(user_id, name, user_school, user_role, user_group):
    new_user = User(user_tg_id=user_id, user_name=name, school=user_school, role=user_role, group=user_group)
    s.add(new_user)
    s.commit()




# adding information about a new group
async def insert_new_group(school_name, group_name):
    new_group = Groups(school=school_name, name=group_name)
    s.add(new_group)
    s.commit()




# getting information about the user's institution
async def get_school(id):
    school = ''
    for item in s.query(User.school).filter(User.user_tg_id == id):
        i = []
        i.append(item[0])
        school = ''.join(i)
    s.commit()
    return school



async def get_role(id):
    for i in s.query(User.role).filter(User.user_tg_id == id):
        role = ''.join(i)
    return(role)
    s.commit()

async def get_groups(school):
    groups = []
    for item in s.query(Groups.name).filter(Groups.school == school):
        groups.append(item[0])
    s.commit()
    return groups

async def get_subjects(school):
    Subjec = []
    for item in s.query(Subjects.subject).filter(Subjects.school == school):
        Subjec.append(item[0])
    s.commit()
    return Subjec

async def insert_hw(h_school, h_group, h_subject, h_teacher_name, sub, h_photo, h_deadline):
    hw = HW(school=h_school, group=h_group, subject=h_subject, teacher_name=h_teacher_name,
            hw_sub=sub, photo=h_photo, deadline=h_deadline, done='None')
    s.add(hw)
    s.commit()

async def get_user_group(id):
    for group in s.query(User.group).filter(User.user_tg_id == id):
        user_group = ''.join(group[0])
    s.commit()
    return user_group

async def get_HW(user_school, user_group, user_subject, user_id):
    hw_1 = {}
    for i in s.query(HW.id, HW.done).filter(HW.school == user_school).filter(HW.group == user_group).filter(HW.subject == user_subject):
        hw_1[i[0]] = i[1]
    print(hw_1)

    keys = []
    for i in hw_1.keys():
        data = hw_1[i]
        if data == 'None':
            keys.append(i)
        
        else:
            ids = []
            ids.append(data.split('-')[0])
            print(ids)

            if str(user_id) not in ids:
                keys.append(i)
                print(keys)
    
    end = []
    for g in keys:
        for h in s.query(HW.id, HW.hw_sub, HW.photo, HW.deadline).filter(HW.id == g):
            data_end = {}
            data_end['id'] = h[0]
            data_end['sub'] = h[1]
            data_end['photo'] = h[2]
            data_end['deadline'] = h[3]

            end.append(data_end)
    s.commit()
    return end


async def done_HW(HW_id, user_id):
    done = ''
    for i in s.query(HW.done).filter(HW.id == HW_id):
        done = ''.join(i)

    if done == 'None':
        done_HW = s.query(HW).filter(HW.id == HW_id).one()
        done_HW.done = str(user_id) 
        s.add(done_HW)
        s.commit()

    else:
        done_end = s.query(HW).filter(HW.id == HW_id).one()
        done_end.done = done + '-' + str(user_id)
        s.add(done_end)
        s.commit()