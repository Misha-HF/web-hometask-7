from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from create_tables import Group, Student, Teacher, Subject, Grade, engine

Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Запит на знаходження 5 студентів з найбільшим середнім балом
    top_students = session.query(Student, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

    # Вивід результатів
    print("Top 5 students with highest average grade:")
    for student, avg_grade in top_students:
        print(f"Student ID: {student.id}, Fullname: {student.fullname}, Average Grade: {avg_grade}")

def select_2(subject_name):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    top_student = session.query(Student, func.avg(Grade.grade).label('avg_grade')).\
        join(Grade).join(Subject).filter(Subject.name == subject_name).\
        group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    
    if top_student:
        student, avg_grade = top_student
        print(f"Top student in {subject_name}:")
        print(f"Student ID: {student.id}, Fullname: {student.fullname}, Average Grade: {avg_grade}")
    else:
        print(f"No data found for subject: {subject_name}")

def select_3(subject_name):
    """
    Знайти середній бал у групах з певного предмета.
    """
    avg_grade_per_group = session.query(Group.name, func.avg(Grade.grade).label('avg_grade')).\
        select_from(Group).\
        join(Student).join(Grade).join(Subject).\
        filter(Subject.name == subject_name).\
        group_by(Group.name).all()
    
    print(f"Average grade by group in {subject_name}:")
    for group_name, avg_grade in avg_grade_per_group:
        print(f"Group: {group_name}, Average Grade: {avg_grade}")

def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    avg_grade_overall = session.query(func.avg(Grade.grade).label('avg_grade')).scalar()
    
    print(f"Overall average grade: {avg_grade_overall}")

def select_5(teacher_id):
    """
    Знайти які курси читає певний викладач за його id.
    """
    courses_taught = session.query(Subject.name).join(Subject.teacher).\
        filter(Teacher.id == teacher_id).all()
    
    print(f"Courses taught by teacher with ID {teacher_id}:")
    for course in courses_taught:
        print(course[0])



def select_6(group_name):
    """
    Знайти список студентів у певній групі.
    """
    students_in_group = session.query(Student).join(Group).filter(Group.name == group_name).all()
    
    print(f"Students in {group_name}:")
    for student in students_in_group:
        print(f"Student ID: {student.id}, Fullname: {student.fullname}")

def select_7(group_name, subject_name):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    grades_in_group = session.query(Student.fullname, Grade.grade).\
        join(Grade).join(Subject).join(Group).filter(Group.name == group_name, Subject.name == subject_name).all()
    
    print(f"Grades in {group_name} for {subject_name}:")
    for fullname, grade in grades_in_group:
        print(f"Student Fullname: {fullname}, Grade: {grade}")

def select_8(teacher_id):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів за його id.
    """
    # Здійснюємо запит, щоб знайти середній бал, який ставить певний викладач
    avg_grade_by_teacher = session.query(func.avg(Grade.grade).label('avg_grade')).\
        join(Subject).join(Teacher).\
        filter(Teacher.id == teacher_id).scalar()

    # Виводимо результати запиту
    if avg_grade_by_teacher is not None:
        print(f"Середній бал, який ставить викладач з ID {teacher_id}: {avg_grade_by_teacher}")
    else:
        print(f"Дані відсутні для викладача з ID {teacher_id}")



def select_9(student_name):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    courses_attended = session.query(Subject.name).join(Grade).join(Student).\
        filter(Student.fullname == student_name).distinct().all()
    
    print(f"Courses attended by {student_name}:")
    for course in courses_attended:
        print(course[0])

def select_10(student_id, teacher_id):
    """
    Список курсів, які певному студенту читає певний викладач за їх id.
    """
    courses_for_student_by_teacher = session.query(Subject.name).join(Grade).join(Student).\
        join(Subject.teacher).filter(Student.id == student_id, Subject.teacher_id == teacher_id).distinct().all()
    
    print(f"Courses attended by student with ID {student_id} and taught by teacher with ID {teacher_id}:")
    for course in courses_for_student_by_teacher:
        print(course[0])

if __name__ == "__main__":
    select_1()
    select_2('Julie Wilson')
    select_3('Billy Wong')
    select_4()
    select_5(1)
    select_6('Sarah Taylor')
    select_7('James Miller', 'Natalie Flores')
    select_8(1)
    select_9('Mark Drake')
    select_10(3, 1)
