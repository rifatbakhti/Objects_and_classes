class Student:
    students_list = []

    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.finished_courses = []
        self.courses_progress = []
        self.grade = {}
        self.students_list.append(self)

    def add_finish_courses(self, course):
        if course not in self.finished_courses:
            self.finished_courses.append(course)
        else:
            print('Ошибка')

    def rate_hw(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in self.courses_progress and course in lecturer.courses_attached
                or course in self.finished_courses):
            if course in lecturer.lecture_grade:
                lecturer.lecture_grade[course] += [grade]
            else:
                lecturer.lecture_grade[course] = [grade]
        else:
            return 'Ошибка'

    def average_grade(self): # нахождение среднего значения ДЗ
        avg_stu = {val: round((sum(items) / len(items)), 2) for val, items in self.grade.items()} # расчет срднего значения по грейду студентов, где subject - это курс, а values - это оценка
        res = []
        for key, val in avg_stu.items():
            res.append(f'Средняя оценка домашних заданий по курсу {key}: {val}')
        return '\n'.join(res)

    def general_average(self):
        avg_gen = [i for val in self.grade.values() for i in val]
        return round(sum(avg_gen) / len(avg_gen), 2)

    def __str__(self):
        res = f'\nИмя: {self.first_name} \nФамилия: {self.last_name} \n{self.average_grade()}\n' \
              f'Общая средняя оценка: {self.general_average()} \n' \
              f'Курсы в процессе изучения: {",".join(self.courses_progress)} \n' \
              f'Завершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.general_average() < other.general_average()
        else:
            print(other, 'not Student!')
            return

class Mentor:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.courses_attached = []

class Lecturer(Mentor):
    lecturer_list = []

    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.lecture_grade = {}
        self.lecturer_list.append(self)

    def add_courses(self, course):
        if course not in self.courses_attached:
            self.courses_attached.append(course)
        else:
            print('Ошибка')

    def average_grade(self):
        avg_lec = {val: round((sum(items) / len(items)), 2) for val, items in self.lecture_grade.items()}
        res = []
        for key, val in avg_lec.items():
            res.append(f'Средняя оценка домашних заданий по курсу {key}: {val}')
        return '\n'.join(res)

    def general_average(self):
        avg_gen = [i for val in self.lecture_grade.values() for i in val]
        return round(sum(avg_gen) / len(avg_gen), 2)

    def __str__(self):
        res = f'Имя: {self.first_name} \nФамилия: {self.last_name} \n{self.average_grade()} \n' \
              f'Общая средняя оценка лекций {self.general_average()}'
        return res

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.general_average() < other.general_average()
        else:
            print(other, 'not Lecturer!')
            return

class Reviewer(Mentor):  # Эксперты
    def __str__(self):
        res = f'Имя: {self.first_name} \nФамилия: {self.last_name}'
        return res

    def add_courses(self, course):
        Lecturer.add_courses(self, course)

    def _rate_hw(self, students, course, grade):
        if isinstance(students, Student) and course in self.courses_attached and course in students.courses_progress:
            if course in students.grade:
                students.grade[course] += [grade]
            else:
                students.grade[course] = [grade]
        else:
            print('Ошибка')

anton = Student('Антон', 'Иванов', 'man')
anton.finished_courses += ['sql', 'git']
anton.courses_progress += ['python']
anton.grade['python'] = [10, 9, 8, 7, 6]
anton.grade['sql'] = [10, 9, 8, 7, 6]

petr = Student('Пётр', 'Петров', 'man')
petr.finished_courses += ['sql', 'git']
petr.courses_progress += ['python']
petr.grade['python'] = [10, 9, 8, 7, 6]
petr.grade['sql'] = [10, 9, 8, 7, 6]

rifat = Lecturer('Рифат', 'Дебров')
rifat.courses_attached = ['python']
rifat.add_courses('git')
rifat.add_courses('sql')

ivan = Lecturer('Иван', 'Иванов')
ivan.courses_attached = ['python']
ivan.add_courses('git')
ivan.add_courses('sql')

anton.rate_hw(rifat, 'python', 10)  # реализовали метод класса Студент, позволяющий оценивать лекции
anton.rate_hw(rifat, 'python', 9)
anton.rate_hw(rifat, 'git', 10)
anton.rate_hw(rifat, 'sql', 7)

petr.rate_hw(ivan, 'python', 6)
petr.rate_hw(ivan, 'python', 9)
petr.rate_hw(ivan, 'git', 1)
petr.rate_hw(ivan, 'sql', 10)

some_reviewer = Reviewer('Отличный', 'Эксперт')  # объявили экземпляр класса Эксперт
some_reviewer.courses_attached.append('python')  # в явном виде добавили курс, который Эксперт может оценивать
some_reviewer.add_courses('git')  # с помощью прямого наследования метода из класса Лектора добавляем курс
some_reviewer._rate_hw(anton, 'python', 9)  # реализация метода класса Эксперт оценивание студента

def averege_greade_courses_students(students, course):
    grade = []
    for i in students:
        for courses, grades in i.grade.items():
            if courses == course:
                grade.extend(grades)
    if len(grade) > 0:
        res = f'Средняя оценка студентов по курсу {course}: {round(sum(grade) / len(grade), 2)}'
        return res
    else:
        res = f'Курс {course} еще не оценивался преподавателем'
        return res

def averege_greade_courses_lecturers(lecturers, course):
    grade = []
    for lector in lecturers:
        for courses, grades in lector.lecture_grade.items():
            if courses == course:
                grade.extend(grades)
    if len(grade) > 0:
        res = f'Средняя оценка лекторов по курсу {course}: {round(sum(grade) / len(grade), 2)}'
        return res
    else:
        res = f'Курс {course} еще не оценивался студентами'
        return res

print()
print('Эксперт:')
print(some_reviewer)

print()
print('Лекторы:')
print(rifat)
print(ivan)

print()
print('Студент:')
print(anton)

print()
print('Сравнение:')
print(anton < petr)
print(rifat > ivan)

print()
print('Общая средняя:')
print(averege_greade_courses_students(Student.students_list, 'sql'))
print(averege_greade_courses_lecturers(Lecturer.lecturer_list, 'python'))