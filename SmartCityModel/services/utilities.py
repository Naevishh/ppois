from typing import Dict, Any, Optional
from ..citizens import Human
from ..core.utils import SafeInput
from ..energy import SmartHome
from ..core import show_menu
from .base import PublicService
from ..core import Domain, RussianStringValidator


class SmartHomeRegistry:
    """Реестр умных домов"""

    def __init__(self) -> None:
        # Ключ: кортеж адреса, Значение: объект SmartHome
        self._homes: dict[tuple, SmartHome] = {}

    def register_home(self, home: SmartHome) -> None:
        self._homes[home.address] = home

    def get_home(self, address: tuple) -> Optional[SmartHome]:
        return self._homes.get(address)


class UtilitiesService(PublicService):
    """Сервис коммунальных услуг"""

    def __init__(self, name: str, address: tuple[str, int], service_id: str) -> None:
        super().__init__(name, address, service_id, Domain.HOUSING)
        # Хранилище данных: { (street, house): { water: int, electricity: int, last_update: str } }
        self.sensor_data = {}
        self.available_actions = [
            ("view_metrics", "Показания счетчиков"),
            ("report_issue", "Сообщить о проблеме (ЖКХ)")
        ]
        self.registry = SmartHomeRegistry()
        self.issue_validator = RussianStringValidator(min_length=10, max_length=500)

    # ============================================================
    # МЕТОДЫ ДЛЯ CLI (принимают аргументы, возвращают значения)
    # ============================================================

    def auto_collect_metrics(self, address: tuple) -> Dict[str, int]:
        """
        Симуляция автоматического сбора данных с IoT-датчиков.
        :param address: Адрес дома (street, house[, apartment])
        :return: Словарь с показаниями
        """
        home = self.registry.get_home(address)
        if not home:
            raise ValueError(f"Дом по адресу {address} не найден в реестре")

        metrics = home.get_metrics()
        self.sensor_data[address] = {
            "water": metrics["water"],
            "electricity": metrics["electricity"]
        }
        return self.sensor_data[address]

    def view_metrics(self, address: tuple) -> Dict[str, Any]:
        """
        Получить показания счетчиков по адресу.
        :param address: Адрес дома
        :return: Словарь с данными показаний
        """
        self.auto_collect_metrics(address)
        data = self.sensor_data.get(address)

        if not data:
            raise ValueError("Данные с датчиков еще не поступили")

        return {
            "address": address,
            "water": data["water"],
            "electricity": data["electricity"]
        }

    def report_issue(self, description: str) -> Dict[str, Any]:
        """
        Создать заявку о проблеме.
        :param description: Описание проблемы
        :return: Словарь с данными заявки
        """
        if not self.issue_validator.validate(description):
            raise ValueError(f"Описание должно быть от 10 до 500 символов")

        issue_id = hash(description) % 1000

        return {
            "issue_id": issue_id,
            "description": description,
            "status": "Передано в диспетчерскую"
        }

    def register_home(self, home: SmartHome) -> str:
        """
        Зарегистрировать умный дом в реестре.
        :param home: Объект SmartHome
        :return: Сообщение о результате
        """
        self.registry.register_home(home)
        return f"Дом по адресу {home.address} зарегистрирован"

    def format_metrics_output(self, metrics_data: Dict[str, Any]) -> str:
        """
        Отформатировать данные показаний для вывода.
        :param metrics_data: Словарь с данными показаний
        :return: Отформатированная строка
        """
        address = metrics_data["address"]

        if len(address) < 3:
            address_str = f"Улица {address[0]}, дом {address[1]}"
        else:
            address_str = f"Улица {address[0]}, дом {address[1]}, квартира {address[2]}"

        output = (
            f"Лицевой счет: {address_str}\n"
            f"Вода: {metrics_data['water']} м³\n"
            f"Электричество: {metrics_data['electricity']} кВт·ч"
        )
        return output

    def format_issue_output(self, issue_data: Dict[str, Any]) -> str:
        """
        Отформатировать данные заявки для вывода.
        :param issue_data: Словарь с данными заявки
        :return: Отформатированная строка
        """
        output = (
            f"Заявка №{issue_data['issue_id']} создана.\n"
            f"Описание: {issue_data['description']}\n"
            f"Статус: {issue_data['status']}"
        )
        return output

    def provide_service(self, person: Human, action: str = None,
                            description: str = None) -> str:
        """
        Универсальный метод для вызова из CLI.
        :param person: Объект пользователя
        :param action: Действие (view_metrics, report_issue)
        :param description: Описание проблемы (для report_issue)
        :return: Результат выполнения
        """
        address = person.address

        if action == "view_metrics":
            try:
                metrics_data = self.view_metrics(address)
                return self.format_metrics_output(metrics_data)
            except ValueError as e:
                return f"Ошибка: {e}"

        elif action == "report_issue":
            if not description:
                raise ValueError("Требуется параметр description")
            try:
                issue_data = self.report_issue(description)
                return self.format_issue_output(issue_data)
            except ValueError as e:
                return f"Ошибка: {e}"

        else:
            raise ValueError(f"Неизвестное действие: {action}")