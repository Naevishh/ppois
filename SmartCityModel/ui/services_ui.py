import uuid
from typing import Optional

from ..citizens import Human
from ..city import SmartCity
from ..core.utils import NAME_VALIDATOR, AGE_VALIDATOR, ADDRESS_VALIDATOR, HOUSE_NUMBER_VALIDATOR


class PublicServiceUI:
    """UI модуль для общественных сервисов"""

    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.current_user_id: Optional[str] = None
        self.available_actions = [
            ("hospital", self.city.hospital.name),
            ("school", self.city.educational_service.name),
            ("utility_service", self.city.utility_services.name),
            ("exit", "Выйти")
        ]
        self.name_validator = NAME_VALIDATOR
        self.age_validator = AGE_VALIDATOR
        self.address_validator = ADDRESS_VALIDATOR
        self.house_validator = HOUSE_NUMBER_VALIDATOR

    def register_user(self, name: str, surname: str, age: int, street: str,
                      house: int, apartment: Optional[int] = None) -> str:
        """
        Зарегистрировать нового пользователя.
        :param name: Имя
        :param surname: Фамилия
        :param age: Возраст
        :param street: Улица
        :param house: Номер дома
        :param apartment: Номер квартиры (опционально)
        :return: ID пользователя
        """
        if not self.name_validator.validate(name):
            raise ValueError(f"Некорректное имя: {name}")

        if not self.name_validator.validate(surname):
            raise ValueError(f"Некорректная фамилия: {surname}")

        if not self.age_validator.validate(age):
            raise ValueError(f"Некорректный возраст: {age}")

        if not self.address_validator.validate(street):
            raise ValueError(f"Некорректный адрес: {street}")

        if not self.house_validator.validate(house):
            raise ValueError(f"Некорректный номер дома: {house}")

        address = (street, house, apartment) if apartment else (street, house)
        person_id = str(uuid.uuid4())[:6]
        new_user = Human(name, surname, age, address, person_id)
        self.city.user_repo.add_user(new_user)

        return person_id

    def login_user(self, user_id: str) -> bool:
        """
        Авторизовать пользователя по ID.
        :param user_id: ID пользователя
        :return: True если успешно
        """
        if self.city.user_repo.authenticate(user_id):
            self.current_user_id = user_id
            return True
        return False

    def get_current_user(self) -> Optional[Human]:
        """
        Получить текущего авторизованного пользователя.
        :return: Объект Human или None
        """
        if self.current_user_id:
            return self.city.user_repo.get_user(self.current_user_id)
        return None

    def access_hospital(self, action: str = None, doctor_name: str = None,
                        purpose: str = None) -> str:
        """
        Получить медицинскую услугу для текущего пользователя.
        :param action: Действие (get_ticket, order_certificate, call_ambulance, list_doctors)
        :param doctor_name: Ключ врача (для get_ticket)
        :param purpose: Цель справки (для order_certificate)
        :return: Результат оказания услуги
        """
        person = self.get_current_user()
        if not person:
            raise ValueError("Пользователь не авторизован. Выполните login.")

        return self.city.hospital.provide_service(person, action, doctor_name, purpose)

    def access_school(self, action: str = None, course_name: str = None,
                      subject: str = None, grade: int = None) -> str:
        """
        Получить услугу образования для текущего пользователя.
        :param action: Действие (enroll_course, set_grade, get_grades, list_courses)
        :param course_name: Название курса (для enroll_course)
        :param subject: Название предмета (для set_grade)
        :param grade: Оценка (для set_grade)
        :return: Результат оказания услуги
        """
        person = self.get_current_user()
        if not person:
            raise ValueError("Пользователь не авторизован. Выполните login.")

        return self.city.educational_service.provide_service(
            person, action, course_name, subject, grade
        )

    def access_utility(self, action: str = None, description: str = None) -> str:
        """
        Получить коммунальную услугу для текущего пользователя.
        :param action: Действие (view_metrics, report_issue)
        :param description: Описание проблемы (для report_issue)
        :return: Результат оказания услуги
        """
        person = self.get_current_user()
        if not person:
            raise ValueError("Пользователь не авторизован. Выполните login.")

        return self.city.utility_services.provide_service(
            person, action, description
        )

    def get_user_info(self) -> Optional[dict]:
        """
        Получить информацию о текущем пользователе.
        :return: Словарь с информацией или None
        """
        person = self.get_current_user()
        if not person:
            return None

        return {
            "user_id": self.current_user_id,
            "name": person.name,
            "surname": person.surname,
            "age": person.age,
            "address": person.address
        }

    def format_user_info(self, user_data: dict) -> str:
        """Отформатировать информацию о пользователе"""
        address_str = f"{user_data['address'][0]}, д. {user_data['address'][1]}"
        if len(user_data['address']) > 2 and user_data['address'][2]:
            address_str += f", кв. {user_data['address'][2]}"

        output = (
            f"Пользователь: {user_data['name']} {user_data['surname']}\n"
            f"ID: {user_data['user_id']}\n"
            f"Возраст: {user_data['age']}\n"
            f"Адрес: {address_str}"
        )
        return output
