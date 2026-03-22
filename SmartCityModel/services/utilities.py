from citizens import Human
from core.utils import SafeInput
from energy import SmartHome
from ui import show_menu
from .base import PublicService
from core import Domain, StringValidator


class SmartHomeRegistry:
    def __init__(self) -> None:
        # Ключ: кортеж адреса, Значение: объект SmartHome
        self._homes: dict[tuple, SmartHome] = {}

    def register_home(self, home: SmartHome) -> None:
        self._homes[home.address] = home

    def get_home(self, address: tuple) -> SmartHome | None:
        return self._homes.get(address)


class UtilitiesService(PublicService):
    def __init__(self, name: str, address: tuple[str, int], service_id: str) -> None:
        super().__init__(name, address, service_id, Domain.HOUSING)
        # Хранилище данных: { (street, house): { water: int, electricity: int, last_update: str } }
        self.sensor_data = {}
        self.available_actions = [
            ("view_metrics", "Показания счетчиков"),
            ("report_issue", "Сообщить о проблеме (ЖКХ)")
        ]
        self.registry = SmartHomeRegistry()
        self.issue_validator = StringValidator(min_length=10, max_length=500)

    def auto_collect_metrics(self, address: tuple) -> None:
        """Симуляция автоматического сбора данных с IoT-датчиков"""
        metrics = self.registry.get_home(address).get_metrics()
        self.sensor_data[address] = {
            "water": metrics["water"],
            "electricity": metrics["electricity"]
        }

    def view_metrics(self, address: tuple, print_func) -> None:
        """Просмотр показаний в личном кабинете по адресу"""
        self.auto_collect_metrics(address)
        data = self.sensor_data.get(address)
        if data:
            if len(address) < 3:
                print_func(f"Лицевой счет: Улица {address[0]}, дом {address[1]}")
            else:
                print_func(f"Лицевой счет: Улица {address[0]}, дом {address[1]}, квартира {address[2]}")
            print_func(f"Вода: {data['water']} м³")
            print_func(f"Электричество: {data['electricity']} кВт·ч")
        else:
            print_func("Данные с датчиков еще не поступили.")

    def report_issue(self, description: str, print_func) -> None:
        print_func(f"Заявка №{hash(description) % 1000} создана.")
        print_func(f"Описание: {description}")
        print_func("Статус: Передано в диспетчерскую.")

    def provide_service(self, get_user_input, print_func, person: Human) -> None:
        action_key = show_menu(self.available_actions, get_user_input, print_func)

        # Получаем адрес из профиля человека для доступа к данным
        address = person.address

        match action_key:
            case "view_metrics":
                self.view_metrics(address, print_func)
            case "report_issue":
                desc = SafeInput.get_string(
                    "Опишите проблему (прорыв, свет, мусор) - минимум 10 символов: ",
                    self.issue_validator,
                    get_user_input,
                    print_func
                )
                self.report_issue(desc, print_func)