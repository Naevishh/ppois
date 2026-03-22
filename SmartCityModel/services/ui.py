import uuid
from typing import Optional

from citizens import UserRepository, Human
from city import SmartCity
from core.utils import NAME_VALIDATOR, AGE_VALIDATOR, ADDRESS_VALIDATOR, HOUSE_NUMBER_VALIDATOR, SafeInput, \
    NumberValidationError
from ui import show_menu


class PublicServiceUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.user_repo = UserRepository()  # Подключаем базу
        self.current_user_id: Optional[str] = None  # Храним только ID
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

    def register(self, get_user_input, print_func) -> str:
        name = SafeInput.get_string(
            "Введите имя: ",
            self.name_validator,
            get_user_input,
            print_func
        )
        # ВАЛИДАЦИЯ: Фамилия
        surname = SafeInput.get_string(
            "Введите фамилию: ",
            self.name_validator,
            get_user_input,
            print_func
        )
        # ВАЛИДАЦИЯ: Возраст
        age = SafeInput.get_int(
            "Введите возраст: ",
            self.age_validator,
            get_user_input,
            print_func
        )
        street = SafeInput.get_string(
            "Введите улицу: ",
            self.address_validator,
            get_user_input,
            print_func
        )
        # ВАЛИДАЦИЯ: Номер дома
        house = SafeInput.get_int(
            "Введите номер дома: ",
            self.house_validator,
            get_user_input,
            print_func
        )
        # ВАЛИДАЦИЯ: Квартира (опционально)
        print_func("Введите номер квартиры/комнаты (если нет, нажмите Enter):")
        apart_raw = get_user_input()
        apart = None
        if apart_raw.strip():
            try:
                apart = self.house_validator.validate_int(apart_raw)
            except NumberValidationError:
                print_func("Некорректный номер квартиры, игнорируется.")

        address = (street, house, apart) if apart else (street, house)
        person_id = str(uuid.uuid4())[:6]
        new_user = Human(name, surname, age, address, person_id)
        self.user_repo.add_user(new_user)
        print_func(f"Пользователь зарегистрирован! Ваш ID: {person_id}")
        return person_id

    def login(self, get_user_input, print_func) -> bool:
        print_func("Введите ваш ID для авторизации:")
        pid = get_user_input().strip()

        if self.user_repo.authenticate(pid):
            self.current_user_id = pid
            print_func("Авторизация успешна!")
            return True
        else:
            print_func("Пользователь не найден. Нужно загестрироваться.")
            pid = self.register(get_user_input, print_func)
            self.current_user_id = pid
            return True

    def menu(self, get_user_input, print_func) -> None:
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