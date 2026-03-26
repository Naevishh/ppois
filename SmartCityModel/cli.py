# SmartCityModel/cli.py

import typer

from core import VehicleType, SensorValueError, HospitalException
from ui import TransportSystemUI, EnvironmentMonitoringUI, UrbanPlanningDataAnalysisUI, PublicServiceUI, SensorUI
from .core.helpers import smooth_print, print_help
from .ui.city_ui import CityUI

app = typer.Typer(
    name="smartcity",
    help="Модель умного города",
    add_completion=False
)

VERSION = "1.0.0"

# Сопоставление команд с методами CityUI
MODULE_MAP = {
    "tms": ("tms_ui", "menu"),
    "traffic": ("traffic_ui", "menu"),
    "env": ("env_ui", "get_environment_state"),
    "data": ("urban_planning_ui", "print_report"),
    "sensors": ("sensors_ui", "update_sensor_data"),
}


def print_welcome():
    """Вывод приветственного экрана"""
    text = (
        "========================================\n"
        f"        SMART CITY MODEL v{VERSION}\n"
        "     Система моделирования городской\n"
        "          инфраструктуры\n"
        "========================================\n"
        "\n"
        "      > Загрузка ядра...\n"
        "      > Подключение модулей...\n"
        "      > Система готова.\n"
    )
    smooth_print(text, print, char_delay=0.015, line_delay=0.03)


modules = [
    ("tms", "Система управления общественным транспортом"),
    ("traffic", "Дорожное движение"),
    ("env", "Окружающая среда"),
    ("data", "Анализ данных города"),
    ("sensors", "Задание значений сенсоров"),
    ("services", "Общественные сервисы")
]

tms_options = [
    (1, "--add-route", "Добавить маршрут"),
    (2, "--add-vehicle", "Добавить транспортное средство"),
    (3, "--add-stop", "Добавить остановку"),
    (4, "--update-location", "Обновить локацию средства"),
    (5, "--arrive-stop", "Прийти на остановку"),
    (6, "--view-routes", "Посмотреть маршруты")
]

traffic_options = [
    (1, "--add-intersection", "Добавить перекресток"),
    (2, "--accident", "Попасть в аварию"),
    (3, "--manage-flow", "Управление транспортным потоком")
]

sensors_options = [
    ("--smart-home", "Сенсоры умного дома"),
    ("--street-lights", "Сенсоры фонарей"),
    ("--generators", "Сенсоры генераторов"),
    ("--air-quality", "Сенсоры качества воздуха"),
    ("--temperature", "Сенсоры температуры"),
    ("--humidity", "Сенсоры влажности"),
    ("--noise-level", "Сенсоры уровня шума")
]

service_actions = [
    ("--hospital", "Больница"),
    ("--school", "Школа"),
    ("--utility", "Коммунальные услуги")
]

commands = {
    "tms": {
        "--add-route": "Добавить маршрут",
        "--add-vehicle": "Добавить транспортное средство",
        "--add-stop": "Добавить остановку",
        "--update-location": "Обновить локацию средства",
        "--arrive-stop": "Прийти на остановку",
        "--view-routes": "Посмотреть маршруты"
    },

    "traffic": {
        "--add-intersection": "Добавить перекресток",
        "--accident": "Попасть в аварию",
        "--manage-flow": "Управление транспортным потоком"
    },

    "env": {"--state": "Получить состояние среды"},
    "data": {"--print-report": "Распечатать отчет"},

    "sensors": {
        "--smart-home": "Сенсоры умного дома",
        "--street-lights": "Сенсоры фонарей",
        "--generators": "Сенсоры генераторов",
        "--air-quality": "Сенсоры качества воздуха",
        "--temperature": "Сенсоры температуры",
        "--humidity": "Сенсоры влажности",
        "--noise-level": "Сенсоры уровня шума"
    },

    "services": {
        "--hospital": "Больница",
        "--school": "Школа",
        "--utility": "Коммунальные услуги",
        "--exit": "Выйти"
    }
}


def parse_flags(args_list):
    """Превращает ['--name', 'Роща', '--type', 'simple'] в {'--name': 'Роща', ...}"""
    params = {}
    i = 0
    while i < len(args_list):
        if args_list[i].startswith("--"):
            key = args_list[i]
            if i + 1 < len(args_list) and not args_list[i + 1].startswith("--"):
                params[key] = args_list[i + 1]
                i += 2
            else:
                params[key] = True
                i += 1
        else:
            i += 1
    return params


@app.command()
def run():
    """🚀 Запустить интерактивное меню (режим по умолчанию)"""
    print_welcome()
    input("\nНажмите Enter для продолжения...")
    print('\033[2J\033[H', end='')  # Очистка экрана

    print("Вы в CLI умного города\n")
    print("На выбор доступны следующие системы: \n")
    print_help(print, modules)
    print("Для справки введите --help")
    print("Для выхода введите --exit")

    while True:

        cmd = input("> ").strip()

        if cmd == "--exit":
            break
        if cmd == "--help":
            for module, command_list in commands.items():
                print(f"{module}")
                for comm, desc in command_list.items():
                    print(f"    {module} {comm} :   {desc}")
            print("Для справки по командам отдельно введите команду с флагом --help\n")
            print("Пример использования комманды:")
            print("    tms --arrive-stop --name 'Пл. Ленина'")
            print("Для справки:\n    tms --arrive-stop --help")

            print("\nexit — выход из программы")
            continue
        parts = cmd.split()

        if len(parts) < 2:
            print("Неверная команда")
            continue

        module = parts[0]
        command = parts[1]
        args = parts[2:]

        city_ui = CityUI()

        try:

            if module in commands and command in commands[module]:

                if module == "tms":
                    handle_tms(city_ui.tms_ui, args, print)
                elif module == "traffic":
                    handle_traffic(city_ui.traffic_ui, args, print)
                elif module == "env":
                    handle_env(city_ui.env_ui, args, print)
                elif module == "data":
                    handle_data(city_ui.env_ui, args, print)
                elif module == "sensors":
                    handle_services(city_ui.env_ui, args, print)
                else:
                    handle_sensors(city_ui.env_ui, args, print)

            else:
                print("Неизвестная команда")


        except KeyboardInterrupt:
            print("\nВыход...")
            break

        except Exception as e:
            print(f"Ошибка выполнения: {e}")

    city_ui.general_menu(input, print)


def handle_traffic(ui, args, print_func):
    """Парсер для модуля Traffic"""
    if not args:
        return
    cmd = args[0]
    params = parse_flags(args[1:])

    if cmd == "--add-intersection":
        district = params.get("--district")
        type_ = params.get("--type", "simple")
        if not district:
            print_func("Ошибка: требуется --district <ID>")
            return
        try:
            ui.add_intersection(district, type_)
            print_func(f"Перекресток добавлен в {district}")
        except Exception as e:
            print_func(f"Ошибка при добавлении перекрестка: {e}")

    elif cmd == "--accident":
        int_id = params.get("--id")
        if not int_id:
            print_func("Ошибка: требуется --id <ID перекрестка>")
            return
        try:
            ui.trigger_accident(int_id)
            print_func(f"Авария на {int_id}")
        except Exception as e:
            print_func(f"Ошибка при создании аварии: {e}")

    else:
        print_func(f"Неизвестная команда traffic: {cmd}")


def handle_tms(ui: TransportSystemUI, args: list[str], print_func) -> None:
    """Обработчик команд модуля TMS"""
    if not args:
        print_func("Не указана команда. Пример: tms --add-stop --name 'Роща'")
        return

    cmd = args[0]
    params = parse_flags(args[1:])

    if cmd == "--add-stop":
        name = params.get("--name")
        if not name:
            print_func("Требуется --name <Название>")
            return
        try:
            stop_id = ui.add_stop(name)
            print_func(f"Остановка добавлена: {stop_id}")
        except Exception as e:
            print_func(f"Ошибка при добавлении остановки: {e}")

    elif cmd == "--add-route":
        stops_str = params.get("--stops")
        if not stops_str:
            print_func("Требуется --stops <ID1,ID2,ID3>")
            return
        stop_ids = [s.strip() for s in stops_str.split(",")]
        try:
            route_id = ui.add_route(stop_ids)
            print_func(f"Маршрут создан: {route_id}")
        except Exception as e:
            print_func(f"Ошибка при создании маршрута: {e}")

    elif cmd == "--add-vehicle":
        v_type = params.get("--type")
        route_id = params.get("--route")
        if not v_type or not route_id:
            print_func("Требуется --type <bus|tram|trolleybus> и --route <ID>")
            return
        try:
            veh_id = ui.add_vehicle(v_type, route_id)
            print_func(f"Транспорт добавлен: {veh_id}")
        except Exception as e:
            print_func(f"Ошибка при добавлении транспорта: {e}")

    elif cmd == "--update-location":
        veh_id = params.get("--vehicle")
        stop_idx = params.get("--stop-index")
        if not veh_id or not stop_idx:
            print_func("Требуется --vehicle <ID> и --stop-index <число>")
            return
        try:
            result = ui.update_vehicle_location(veh_id, int(stop_idx))
            print_func(result)
        except ValueError:
            print_func("Ошибка: --stop-index должен быть числом")
        except Exception as e:
            print_func(f"Ошибка при обновлении локации: {e}")

    elif cmd == "--arrive-stop":
        stop_id = params.get("--stop")
        if not stop_id:
            print_func("Требуется --stop <ID>")
            return
        try:
            info = ui.arrive_at_stop(stop_id)
            ui.format_arrival_info(info, print_func)
        except Exception as e:
            print_func(f"Ошибка при прибытии на остановку: {e}")

    elif cmd == "--view-routes":
        try:
            routes = ui.list_routes()
            ui.format_routes_output(routes, print_func)
        except Exception as e:
            print_func(f"Ошибка при получении списка маршрутов: {e}")

    elif cmd == "--list-vehicles":
        try:
            vehicles = ui.get_vehicle_list()
            for v in vehicles:
                print_func(f"[Транспорт] {v['device_id']} ({v['type']}) - маршрут {v['route_id']}")
        except Exception as e:
            print_func(f"Ошибка при получении списка транспорта: {e}")

    elif cmd == "--list-stops":
        try:
            stops = ui.get_stop_list()
            for s in stops:
                print_func(f"[Остановка] {s['device_id']}: {s['name']} (пассажиров: {s['passengers']})")
        except Exception as e:
            print_func(f"Ошибка при получении списка остановок: {e}")

    else:
        print_func(f"Неизвестная команда tms: {cmd}")


def handle_env(ui: EnvironmentMonitoringUI, args: list, print_func) -> None:
    """Обработчик команд модуля Environment"""
    if not args:
        print_func("Не указана команда. Пример: env --state")
        return

    cmd = args[0]

    if cmd == "--state":
        results = ui.get_environment_state()
        output = ui.format_environment_state(results)
        print_func(output)
    else:
        print_func(f"Неизвестная команда env: {cmd}")


def handle_data(ui: UrbanPlanningDataAnalysisUI, args: list, print_func) -> None:
    """Обработчик команд модуля Data Analysis"""
    if not args:
        print_func("Не указана команда. Пример: data --print-report")
        return

    cmd = args[0]

    if cmd == "--print-report":
        report = ui.generate_report()
        output = ui.format_report(report)
        print_func(output)
    else:
        print_func(f"Неизвестная команда data: {cmd}")


def handle_services(ui: PublicServiceUI, args: list, print_func) -> None:
    """Обработчик команд модуля Services"""
    if not args:
        print_func("Не указана команда. Пример: services --register --name Иван --surname Иванов ...")
        return

    cmd = args[0]
    params = parse_flags(args[1:])

    if cmd == "--register":
        name = params.get("--name")
        surname = params.get("--surname")
        age = params.get("--age")
        street = params.get("--street")
        house = params.get("--house")
        apartment = params.get("--apartment")

        if not all([name, surname, age, street, house]):
            print_func("Требуется: --name, --surname, --age, --street, --house")
            return

        try:
            user_id = ui.register_user(name, surname, int(age), street, int(house),
                                       int(apartment) if apartment else None)
            print_func(f"Пользователь зарегистрирован! Ваш ID: {user_id}")
        except ValueError as e:
            print_func(f"Ошибка валидации: {e}")
        except Exception as e:
            print_func(f"Ошибка при регистрации пользователя: {e}")

    elif cmd == "--login":
        user_id = params.get("--id")
        if not user_id:
            print_func("Требуется: --id <USER_ID>")
            return

        if ui.login_user(user_id):
            print_func("Авторизация успешна!")
        else:
            print_func("Пользователь не найден.")

    elif cmd == "--whoami":
        user_data = ui.get_user_info()
        if user_data:
            output = ui.format_user_info(user_data)
            print_func(output)
        else:
            print_func("Пользователь не авторизован.")

    elif cmd == "--hospital":
        action = params.get("--action")  # get_ticket, order_certificate, call_ambulance, list_doctors

        if not action:
            print_func("Требуется: --action <get_ticket|order_certificate|call_ambulance|list_doctors>")
            return

        try:
            if action == "get_ticket":
                doctor_name = params.get("--doctor")
                if not doctor_name:
                    print_func("Требуется: --doctor <psychiatrist|therapist|surgeon>")
                    return
                result = ui.access_hospital(action=action, doctor_name=doctor_name)

            elif action == "order_certificate":
                purpose = params.get("--purpose")
                if not purpose:
                    print_func("Требуется: --purpose <Цель справки>")
                    return
                result = ui.access_hospital(action=action, purpose=purpose)

            elif action == "call_ambulance":
                result = ui.access_hospital(action=action)

            elif action == "list_doctors":
                result = ui.access_hospital(action=action)

            else:
                print_func(f"Неизвестное действие: {action}")
                return

            print_func(result)
        except (ValueError, HospitalException) as e:
            print_func(f"Ошибка: {e}")


    elif cmd == "--school":
        action = params.get("--action")  # enroll_course, set_grade, get_grades, list_courses

        if not action:
            print_func("Требуется: --action <enroll_course|set_grade|get_grades|list_courses>")
            return

        try:
            if action == "enroll_course":
                course_name = params.get("--course")
                if not course_name:
                    print_func("Требуется: --course <Название>")
                    return
                result = ui.access_school(action=action, course_name=course_name)

            elif action == "set_grade":
                subject = params.get("--subject")
                grade = params.get("--grade")
                if not subject or not grade:
                    print_func("Требуется: --subject <Название> и --grade <1-10>")
                    return
                result = ui.access_school(action=action, subject=subject, grade=int(grade))

            elif action == "get_grades":
                result = ui.access_school(action=action)

            elif action == "list_courses":
                result = ui.access_school(action=action)
            else:
                print_func(f"Неизвестное действие: {action}")
                return

            print_func(result)

        except ValueError as e:
            print_func(f"Ошибка: {e}")

    elif cmd == "--utility":
        action = params.get("--action")  # view_metrics, report_issue

        if not action:
            print_func("Требуется: --action <view_metrics|report_issue>")
            return

        try:
            if action == "view_metrics":
                result = ui.access_utility(action=action)

            elif action == "report_issue":
                description = params.get("--description")
                if not description:
                    print_func("Требуется: --description <Текст проблемы>")
                    return
                result = ui.access_utility(action=action, description=description)

            else:
                print_func(f"Неизвестное действие: {action}")
                return

            print_func(result)
        except ValueError as e:
            print_func(f"Ошибка: {e}")

    else:
        print_func(f"Неизвестная команда services: {cmd}")


# SmartCityModel/cli.py (фрагмент)

def handle_sensors(ui: SensorUI, args: list, print_func) -> None:
    """Обработчик команд модуля Sensors"""
    if not args:
        print_func("Не указана команда. Пример: sensors --set --district center --type temperature --value 25")
        return

    cmd = args[0]
    params = parse_flags(args[1:])

    if cmd == "--list-districts":
        districts = ui.get_district_list()
        output = ui.format_district_list(districts)
        print_func(output)

    elif cmd == "--list-sensors":
        district_id = params.get("--district")
        category = params.get("--category")  # air, temperature, humidity, noise, lights, smart_homes
        if not district_id or not category:
            print_func("Требуется: --district <ID> и --category <type>")
            return

        try:
            sensors = ui.get_sensor_list(district_id, category)
            output = ui.format_sensor_list(sensors)
            print_func(output)
        except ValueError as e: #:))))
            print_func(f"Ошибка: {e}")

    elif cmd == "--set":

        district_id = params.get("--district")
        sensor_type = params.get("--type")
        value = params.get("--value")

        if not all([district_id, sensor_type, value]):
            print_func("Требуется: --district, --type, --value")
            return

        try:
            if sensor_type in ["water", "thermostat"]:
                home_index = int(params.get("--home-index", 0))
                result = ui.set_smart_home_sensor(district_id, home_index, sensor_type, int(value))
            elif sensor_type == "light":
                # Для света нужны индексы дома и светильника
                home_index = int(params.get("--home-index", 0))
                light_index = int(params.get("--light-index", 0))
                result = ui.set_smart_home_sensor(district_id, home_index, sensor_type, int(value), light_index)
            elif sensor_type in ["solar", "wind"]:
                result = ui.set_generator_sensor(district_id, sensor_type, int(value))
            elif sensor_type in ["air", "temperature", "humidity", "noise"]:
                sensor_index = int(params.get("--sensor-index", 0))
                result = ui.set_district_sensor(district_id, sensor_type, sensor_index, int(value))
            else:
                print_func(f"Неизвестный тип сенсора: {sensor_type}")
                return
            print_func(result)

        except ValueError as e:
            print_func(f"Ошибка: {e}")
        except SensorValueError as e:
            print_func(f"Выход за предел значений показаний: {e}")

    elif cmd == "--traffic":
        district_id = params.get("--district")
        intersection_index = params.get("--intersection")
        light_id = params.get("--light")
        sensor_type = params.get("--type")  # camera, flow, pedestrian
        value = params.get("--value")

        if not all([district_id, intersection_index, light_id, sensor_type]):
            print_func("Требуется: --district, --intersection, --light, --type")
            return

        try:
            if sensor_type == "camera":
                # Для камеры нужна дополнительная логика
                print_func("Для камеры используйте отдельную команду --camera-event")
                return
            else:
                result = ui.set_traffic_sensor(district_id, int(intersection_index),
                                               light_id, sensor_type, int(value))
                print_func(result)
        except ValueError as e:
            print_func(f"Ошибка: {e}")
        except SensorValueError as e:
            print_func(f"Выход за предел значений показаний: {e}")

    elif cmd == "--camera-event":
        district_id = params.get("--district")
        intersection_index = params.get("--intersection")
        light_id = params.get("--light")
        vehicle_type = params.get("--vehicle")  # bus, tram, trolleybus, car
        is_incident = params.get("--incident", "false").lower() == "true"

        if not all([district_id, intersection_index, light_id, vehicle_type]):
            print_func("Требуется: --district, --intersection, --light, --vehicle")
            return

        # Маппинг типов транспорта
        vehicle_type_key = None
        for veh in VehicleType:
            if veh.value == vehicle_type.lower():
                vehicle_type_key = veh
        if not vehicle_type_key:
            print_func(f"Неизвестный тип транспорта: {vehicle_type}")
            return

        try:
            dist = ui.city.districts[district_id]
            inter = dist.intersections[int(intersection_index)]
            camera = inter.lights[light_id].camera
            result = ui.detect_camera_event(camera, vehicle_type_key, is_incident)
            print_func(result)
        except Exception as e:
            print_func(f"Ошибка: {e}")

    else:
        print_func(f"Неизвестная команда sensors: {cmd}")


if __name__ == "__main__":
    app()
