from citizens import Human
from core import Domain
from ui import show_menu
from .base import PublicService


class EducationService(PublicService):
    def __init__(self, name: str, address: tuple[str, int], service_id: str):
        super().__init__(name, address, service_id, Domain.EDUCATION)
        self.available_actions = [
            ("enroll_course", "Записаться на курс"),
            ("set_grades", "Поставить оценку"),
            ("get_grades", "Узнать оценки")
        ]
        # Хранилище успеваемости: { student_id: { subject: grade } }
        self.grade_book = {}
        self.courses = {"Python": 50, "DataScience": 30}

    def enroll_course(self, course_name: str, student: Human, print_func):
        sid = student.person_id
        if course_name in self.courses and self.courses[course_name] > 0:
            self.courses[course_name] -= 1

            # Инициализируем запись в журнале, если студент еще не записан
            if sid not in self.grade_book:
                self.grade_book[sid] = {}

            # Добавляем курс
            self.grade_book[sid][course_name] = "Зачислен"
            print_func(f"Вы записаны на курс '{course_name}'.")
        else:
            print_func(f"На курс '{course_name}' мест нет.")

    def set_grade(self, student: Human, subject, grade):
        # Получаем доступ к личному кабинету по ID
        sid = student.person_id

        if sid not in self.grade_book:
            self.grade_book[sid] = {}
        self.grade_book[sid][subject] = grade

    def get_grades(self, student: Human, print_func):
        # Получаем доступ к личному кабинету по ID
        sid = student.person_id
        record = self.grade_book.get(sid)

        print_func(f"Личный кабинет: {student.name[1]} {student.name[0][0]} (ID: {sid})")
        if record:
            for subj, grade in record.items():
                print_func(f"- {subj}: {grade}")
        else:
            print_func("Записей пока нет.")

    def provide_service(self, get_user_input, print_func, student: Human):
        action_key = show_menu(self.available_actions, get_user_input, print_func)

        match action_key:
            case "enroll_course":
                print_func("Введите название курса:")
                course = get_user_input()
                self.enroll_course(course, student, print_func)
            case "set_grade":
                print_func("Введите название предмета:")
                subject = get_user_input()
                print_func("Введите оценку:")
                grade = get_user_input
                self.set_grade(student, subject, grade)
            case "get_grades":
                self.get_grades(student, print_func)
