from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# З'єднання з базою даних PostgreSQL
DB_URI = "postgresql://postgres:12345678@localhost/postgres"
engine = create_engine(DB_URI, echo=True)  # echo=True включає вивід SQL-запитів у консоль

Base = declarative_base()

# Визначення моделі таблиці Group
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

# Визначення моделі таблиці Student
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship("Group", backref="students")

# Визначення моделі таблиці Teacher
class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)

# Визначення моделі таблиці Subject
class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String(175), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship("Teacher", backref="subjects")

# Визначення моделі таблиці Grade
class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship("Student", backref="grades")
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))
    subject = relationship("Subject", backref="grades")
    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'), nullable=False)
    grade_date = Column(Date, nullable=False)

# Створення таблиць у базі даних
Base.metadata.create_all(engine)
