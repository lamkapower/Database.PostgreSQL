import psycopg2
import datetime

utc_now = datetime.datetime.now()

student_dict = {
    '1':'Иванов Анатолий Иванович',
    '2':'Захаров Петр Анатольевич',
    '3':'Петров Инокентий Игоревич',
}

def create_db(): # создаем таблицу
    cur.execute("""CREATE TABLE Student (
id serial PRIMARY KEY,
name varchar(100),
gpa numeric(10, 2) null,
birth timestamp with time zone null);
""")
    cur.execute("""CREATE TABLE Course (
id serial PRIMARY KEY,
name varchar(100));
""")
    cur.execute("""CREATE TABLE student_course (
student_id integer REFERENCES Student(id),
course_id integer REFERENCES Course(id));
""")

def get_students(course_id): # возвращает студентов определенного курса
    cur.execute("""select stud.id, stud.name, course.name from student_course sc
join student stud on stud.id = sc.student_id
join course on course.id = sc.course_id
""")
    return print(cur.fetchall())

def add_students(course_id, students): # создает студентов и записывает их на курс
    for student in students.values():
        cur.execute('insert into Student (name, birth) values (%s, %s);', (student, utc_now))
        cur.execute("select id, name from Student")
        result = [x[0] for x in cur.fetchall() if x[1] == student]
        cur.execute("""
        insert into student_course (student_id, course_id)
        values (%s, %s);
        """, (result[0], course_id))

def add_student(student): # просто создает студента
    cur.execute('insert into Student (name) values (%s);', (student, ))
    

def get_student(student_id):
    cur.execute("select id, name from Student")
    result = [x[1] for x in cur.fetchall() if x[0] == student_id]
    return print(result[0])

with psycopg2.connect(dbname='kkv', user='kkv', password='Qqwerty123456', host='pg.codecontrol.ru', port=59432) as conn:
    cur = conn.cursor()
    # cur.execute('''
    # drop table student_course
    # ''')
    # add_student('Masha')
    # cur.execute("insert into Student (name, birth) values (%s, %s)", ("Иван Иванов", "2020-07-16T 13:55:10+3"))
    # cur.execute("insert into Course (name) values (%s)", ("Digital MBA", ))
    # cur.execute("select * from Student")
    get_students(3)
    # add_students(3, student_dict)