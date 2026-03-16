import uuid
from typing import Optional

from citizens import UserRepository, Human
from city import SmartCity
from ui import show_menu
from . import EducationService, UtilitiesService, Hospital


class PublicServiceUI:
    def __init__(self, city: SmartCity):
        self.city=city
        self.user_repo = UserRepository()  # Подключаем базу
        self.current_user_id: Optional[str] = None  # Храним только ID
        self.available_actions = [
            ("hospital", self.city.hospital.name),
            ("school", self.city.educational_service.name),
            ("utility_service", self.city.utility_services.name),
            ("exit", "Выйти")
        ]

    def register(self, get_user_input, print_func):
        print_func(f"Введите имя:")
        name = get_user_input()
        print_func("Введите фамилию:")
        surname = get_user_input()
        print_func("Введите возраст:")
        age = get_user_input()
        print_func("Введите улицу:")
        street = get_user_input()
        print_func("Введите номер дома:")
        house = get_user_input()
        print_func("Введите номер квартиры/комнаты (если нет, нажмите Enter):")
        apart = get_user_input()
        address = (street, house, apart) if apart else (street, house)
        person_id = str(uuid.uuid4())[:6]
        new_user = Human(name, surname, age, address, person_id)
        self.user_repo.add_user(new_user)
        return person_id

    def login(self, get_user_input, print_func):
        print_func("Введите ваш ID для авторизации:")
        pid = get_user_input()

        if self.user_repo.authenticate(pid):
            self.current_user_id = pid
            print_func("Авторизация успешна!")
            return True
        else:
            print_func("Пользователь не найден. Нужно загестрироваться.")
            pid = self.register(get_user_input, print_func)
            self.current_user_id = pid
            return True

    def menu(self, get_user_input, print_func):
        print_func("Чтобы пользоваться сервисами, необходимо авторизоваться.")
        if not self.current_user_id:
            self.login(get_user_input, print_func)

        while True:
            key = show_menu(self.available_actions, get_user_input, print_func, "Выберите учреждение:")
            person = self.user_repo.get_user(self.current_user_id)
            match key:
                case "hospital":
                    self.city.hospital.provide_service(get_user_input, print_func, person)
                case "school":
                    self.city.educational_service.provide_service(get_user_input, print_func, person)
                case "utility_service":
                    self.city.utility_services.provide_service(get_user_input, print_func, person)
                case "exit":
                    return
