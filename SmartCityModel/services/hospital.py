from citizens import Human
from core import Domain
from core import HospitalException
from core.utils import NAME_VALIDATOR, SafeInput
from ui import show_menu
from .base import PublicService


class Hospital(PublicService):
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

    def order_ticket_to_doctor(self, doctor_name: str, patient: Human) -> str:
        doctor = self.doctors[doctor_name]
        if doctor['current'] >= doctor['limit']:
            raise HospitalException(f"Все талоны к врачу {doctor['name']} были выписаны")
        else:
            doctor['current'] += 1
            return (f"Талон к врачу {doctor['name']} №{doctor['current']}."
                    f"\nПациент: {patient.name[1]} {patient.name[0][0]}.")

    def order_ticket(self, get_user_input, print_func, patient: Human) -> None:
        options = [(key, doc['name']) for key, doc in self.doctors.items()]

        doctor_key = show_menu(
            options,
            get_user_input,
            print_func,
            "Выберите врача:"
        )

        if doctor_key:
            doctor_name = options[doctor_key][0]
            try:
                result = self.order_ticket_to_doctor(doctor_name, patient)
                print_func(result)
            except HospitalException as e:
                print_func(f"Ошибка: {e}")

    def order_certificate(self, purpose: str, patient: Human, print_func) -> None:
        address = patient.address
        print_func(f"Справка {purpose}"
                   f"\nУчреждение {self.name}"
                   f"\nВыдана пациенту: {patient.name[1]} {patient.name[0]}"
                   f"\nПроживающему по адресу: Улица {address[0]}, дом {address[1]}")

    def call_ambulance(self, address: tuple, print_func) -> None:
        print_func(f"Скорая выехала на адрес: Улица {address[0]}, дом {address[1]}")

    def provide_service(self, get_user_input, print_func, patient: Human) -> None:
        action_key = show_menu(self.available_actions, get_user_input, print_func)
        match action_key:
            case "get_ticket":
                self.order_ticket(get_user_input, print_func, patient)
            case "order_certificate":
                purpose = SafeInput.get_string(
                    "Укажите цель справки (в школу, в университет, по месту работы и т.д.): ",
                    self.purpose_validator,
                    get_user_input,
                    print_func
                )
                self.order_certificate(purpose, patient, print_func)
            case "call_ambulance":
                self.call_ambulance(patient.address, print_func)