from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from create_tables import Group, Student, Teacher, Subject, Grade, engine
from datetime import datetime, timedelta
import random

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація генератора випадкових даних
fake = Faker()

# Створення груп
groups = [Group(name=fake.name()) for _ in range(3)]
session.add_all(groups)
session.commit()

# Створення викладачів
teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Створення предметів і призначення викладачів
subjects = []
for i in range(7):
    subject = Subject(name=fake.name(), teacher=random.choice(teachers))
    subjects.append(subject)
session.add_all(subjects)
session.commit()

# Створення студентів
students = []
for _ in range(30):
    student = Student(fullname=fake.name(), group=random.choice(groups))
    students.append(student)
session.add_all(students)
session.commit()

# Наповнення таблиці оцінок
for student in students:
    for subject in subjects:
        grade = Grade(student=student, subject=subject, grade=random.randint(1, 100),
                      grade_date=fake.date_time_between(start_date='-1y', end_date='now'))
        session.add(grade)
session.commit()

print("Database seeded successfully!")
