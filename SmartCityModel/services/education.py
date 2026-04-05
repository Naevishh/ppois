from typing import Dict, Any

from .base import PublicService
from ..citizens import Human
from ..core import Domain
from ..core.utils import NAME_VALIDATOR, GRADE_VALIDATOR, LATIN_STR_VALIDATOR


class EducationService(PublicService):
    """Сервис образовательных услуг"""

    def __init__(self, name: str, address: tuple[str, int], service_id: str) -> None:
        super().__init__(name, address, service_id, Domain.EDUCATION)
        self.available_actions = [
            ("enroll_course", "Записаться на курс"),
            ("set_grades", "Поставить оценку"),
            ("get_grades", "Узнать оценки")
        ]
        # Хранилище успеваемости: { student_id: { subject: grade } }
        self.grade_book = {}
        self.courses = {"Python": 50, "DataScience": 30}
        self.course_validator = LATIN_STR_VALIDATOR
        self.subject_validator = NAME_VALIDATOR
        self.grade_validator = GRADE_VALIDATOR

    # ============================================================
    # МЕТОДЫ ДЛЯ CLI (принимают аргументы, возвращают значения)
    # ============================================================

    def enroll_course(self, course_name: str, student: Human) -> str:
        """
        Записать студента на курс.
        :param course_name: Название курса
        :param student: Объект студента
        :return: Сообщение о результате
        """
        if not self.course_validator.validate(course_name):
            raise ValueError(f"Некорректное название курса: {course_name}.")
        sid = student.person_id

        if course_name not in self.courses:
            return f"Курс '{course_name}' не найден."

        if self.courses[course_name] <= 0:
            return f"На курс '{course_name}' мест нет."

        self.courses[course_name] -= 1

        # Инициализируем запись в журнале, если студент еще не записан
        if sid not in self.grade_book:
            self.grade_book[sid] = {}

        # Добавляем курс
        self.grade_book[sid][course_name] = "Зачислен"
        return f"Вы записаны на курс '{course_name}'."

    def set_grade(self, student: Human, subject: str, grade: int) -> str:
        """
        Поставить оценку студенту.
        :param student: Объект студента
        :param subject: Название предмета
        :param grade: Оценка (1-10)
        :return: Сообщение о результате
        """
        if not self.subject_validator.validate(subject) and not self.course_validator.validate(subject):
            raise ValueError(f"Некорректное название предмета: {subject}.")

        if not self.grade_validator.validate_int(grade):
            raise ValueError(f"Некорректная оценка: {grade}. Допустимый диапазон 1-10.")

        sid = student.person_id

        if sid not in self.grade_book:
            self.grade_book[sid] = {}

        self.grade_book[sid][subject] = grade
        return f"Оценка {grade} по предмету '{subject}' установлена."

    def get_grades(self, student: Human) -> Dict[str, Any]:
        """
        Получить оценки студента.
        :param student: Объект студента
        :return: Словарь с информацией об оценках
        """
        sid = student.person_id
        record = self.grade_book.get(sid, {})

        return {
            "student_id": sid,
            "student_name": f"{student.surname} {student.name[0][0]}.",
            "grades": record
        }

    def get_available_courses(self) -> Dict[str, int]:
        """
        Получить список доступных курсов.
        :return: Словарь {название_курса: количество_мест}
        """
        return self.courses.copy()

    def format_grades_output(self, grades_data: Dict[str, Any]) -> str:
        """
        Отформатировать данные об оценках для вывода.
        :param grades_data Словарь с данными об оценках
        :return: Отформатированная строка
        """
        lines = [f"Личный кабинет: {grades_data['student_name']} (ID: {grades_data['student_id']})"]

        if grades_data['grades']:
            for subj, grade in grades_data['grades'].items():
                lines.append(f"- {subj}: {grade}")
        else:
            lines.append("Записей пока нет.")

        return "\n".join(lines)

    def format_courses_output(self, courses: Dict[str, int]) -> str:
        """
        Отформатировать список курсов для вывода.
        :param courses: Словарь курсов
        :return: Отформатированная строка
        """
        lines = ["Доступные курсы:"]

        for course_name, seats in courses.items():
            status = f"{seats} мест" if seats > 0 else "Нет мест"
            lines.append(f"- {course_name}: {status}")

        return "\n".join(lines)

    # ============================================================
    # МЕТОДЫ ДЛЯ ИНТЕРАКТИВНОГО МЕНЮ (используют input)
    # ============================================================

    def provide_service(self, student: Human, action: str = None,
                        course_name: str = None, subject: str = None,
                        grade: int = None) -> str:
        """
        Универсальный метод для вызова из CLI.
        :param student: Объект студента
        :param action: Действие (enroll_course, set_grade, get_grades, list_courses)
        :param course_name: Название курса (для enroll_course)
        :param subject: Название предмета (для set_grade)
        :param grade: Оценка (для set_grade)
        :return: Результат выполнения
        """
        if action == "enroll_course":
            if not course_name:
                raise ValueError("Требуется параметр course_name")
            return self.enroll_course(course_name, student)

        elif action == "set_grade":
            if not subject or grade is None:
                raise ValueError("Требуются параметры subject и grade")
            return self.set_grade(student, subject, grade)

        elif action == "get_grades":
            grades_data = self.get_grades(student)
            return self.format_grades_output(grades_data)

        elif action == "list_courses":
            courses = self.get_available_courses()
            return self.format_courses_output(courses)

        else:
            raise ValueError(f"Неизвестное действие: {action}")
