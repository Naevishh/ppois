# SmartCityModel/services/hospital.py

from typing import Optional, Dict, Any
from ..citizens import Human
from ..core import Domain
from ..core import HospitalException
from ..core.utils import NAME_VALIDATOR, SafeInput
from .base import PublicService


class Hospital(PublicService):
    """Сервис медицинских услуг"""

    def __init__(self, name: str, address: tuple[str, int], service_id: str) -> None:
        super().__init__(name, address, service_id, Domain.HEALTHCARE)
        self.doctors = {
            'psychiatrist': {'name': 'Окулист', 'limit': 30, 'current': 0, 'serving': 0},
            'therapist': {'name': 'Терапевт', 'limit': 50, 'current': 0, 'serving': 0},
            'surgeon': {'name': 'Хирург', 'limit': 10, 'current': 0, 'serving': 0},
        }
        self.available_actions = [
            ("get_ticket", "Записаться к врачу"),
            ("order_certificate", "Заказать справку"),
            ("call_ambulance", "Вызов скорой")
        ]
        self.purpose_validator = NAME_VALIDATOR

    # ============================================================
    # МЕТОДЫ ДЛЯ CLI (принимают аргументы, возвращают значения)
    # ============================================================

    def order_ticket_to_doctor(self, doctor_name: str, patient: Human) -> str:
        """
        Записать пациента к врачу.
        :param doctor_name: Ключ врача (psychiatrist, therapist, surgeon)
        :param patient: Объект пациента
        :return: Сообщение о результате
        """
        if doctor_name not in self.doctors:
            available = ', '.join(self.doctors.keys())
            raise ValueError(f"Некорректное имя врача: {doctor_name}. Доступные: {available}")

        doctor = self.doctors[doctor_name]

        if doctor['current'] >= doctor['limit']:
            raise HospitalException(f"Все талоны к врачу {doctor['name']} были выписаны")

        doctor['current'] += 1
        return (f"Талон к врачу {doctor['name']} №{doctor['current']}.\n"
                f"Пациент: {patient.surname} {patient.name[0][0]}.")

    def order_certificate(self, purpose: str, patient: Human) -> str:
        """
        Заказать справку.
        :param purpose: Цель справки
        :param patient: Объект пациента
        :return: Текст справки
        """
        if not self.purpose_validator.validate(purpose):
            raise ValueError(f"Некорректная цель справки: {purpose}")

        address = patient.address
        address_str = f"Улица {address[0]}, дом {address[1]}"
        if len(address) > 2 and address[2]:
            address_str += f", квартира {address[2]}"

        return (f"Справка: {purpose}\n"
                f"Учреждение: {self.name}\n"
                f"Выдана пациенту: {patient.surname} {patient.name}\n"
                f"Проживающему по адресу: {address_str}")

    def call_ambulance(self, address: tuple) -> str:
        """
        Вызвать скорую помощь.
        :param address: Адрес вызова
        :return: Сообщение о результате
        """
        address_str = f"Улица {address[0]}, дом {address[1]}"
        if len(address) > 2 and address[2]:
            address_str += f", квартира {address[2]}"

        return f"Скорая выехала на адрес: {address_str}"

    def get_available_doctors(self) -> Dict[str, Dict[str, Any]]:
        """
        Получить список доступных врачей.
        :return: Словарь с информацией о врачах
        """
        result = {}
        for key, data in self.doctors.items():
            result[key] = {
                "name": data["name"],
                "available": data["limit"] - data["current"],
                "total": data["limit"]
            }
        return result

    def format_doctors_output(self, doctors: Dict[str, Dict[str, Any]]) -> str:
        """
        Отформатировать список врачей для вывода.
        :param doctors: Словарь с данными о врачах
        :return: Отформатированная строка
        """
        lines = ["Доступные врачи:"]

        for key, data in doctors.items():
            status = f"{data['available']}/{data['total']} мест"
            lines.append(f"- {key}: {data['name']} ({status})")

        return "\n".join(lines)

    # ============================================================
    # МЕТОДЫ ДЛЯ ИНТЕРАКТИВНОГО МЕНЮ (используют input)
    # ============================================================

    def provide_service(self, patient: Human, action: str = None,
                            doctor_name: str = None, purpose: str = None) -> str:
        """
        Универсальный метод для вызова из CLI.
        :param patient: Объект пациента
        :param action: Действие (get_ticket, order_certificate, call_ambulance, list_doctors)
        :param doctor_name: Ключ врача (для get_ticket)
        :param purpose: Цель справки (для order_certificate)
        :return: Результат выполнения
        """
        if action == "get_ticket":
            if not doctor_name:
                raise ValueError("Требуется параметр doctor_name")
            return self.order_ticket_to_doctor(doctor_name, patient)

        elif action == "order_certificate":
            if not purpose:
                raise ValueError("Требуется параметр purpose")
            return self.order_certificate(purpose, patient)

        elif action == "call_ambulance":
            return self.call_ambulance(patient.address)

        elif action == "list_doctors":
            doctors = self.get_available_doctors()
            return self.format_doctors_output(doctors)

        else:
            raise ValueError(f"Неизвестное действие: {action}")