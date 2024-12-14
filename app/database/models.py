from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///bot.db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, nullable=False)
    user_name = Column(String)
    school = Column(String)
    role = Column(String)
    group = Column(String)


class Bank(Base):
    __tablename__ = 'Bank'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("Users.user_id"))
    name = Column(String)
    last_name = Column(String)
    balance = Column(Integer)


class Admin_tokens(Base):
    __tablename__ = 'Admin_tokens'

    id = Column(Integer, primary_key=True)
    tokens = Column(String, nullable=False)


class Teacher_tokens(Base):
    __tablename__ = 'Teacher_tokens'

    id = Column(Integer, primary_key=True)
    school = Column(String, nullable=False)
    token = Column(String, nullable=False)


class Student_tokens(Base):
    __tablename__ = 'Student_tokens'

    id = Column(Integer, primary_key=True)
    school = Column(String, nullable=False)
    group = Column(String, nullable=False)
    token = Column(String, nullable=False)


class Schools(Base):
    __tablename__ = 'Schools'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    admin_id = Column(String, nullable=False)
    admin_name = Column(String, nullable=False)


class Groups(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    school = Column(String, nullable=False)
    name = Column(String, nullable=False)

class HW(Base):
    __tablename__ = 'HW'

    id = Column(Integer, primary_key=True)
    school = Column(String)
    group = Column(String)
    subject = Column(String)
    teacher_name = Column(String)
    hw_sub = Column(String)
    photo = Column(String)
    deadline = Column(String)
    done = Column(String)

class Subjects(Base):
    __tablename__ = 'Subjects'

    id = Column(Integer, primary_key=True)
    school = Column(String)
    subject = Column(String)

start_db = Base.metadata.create_all(engine)
