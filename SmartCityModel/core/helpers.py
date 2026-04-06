import time
from typing import Any


def smooth_print(text: str, print_func, char_delay: float = 0.02, line_delay: float = 0.05):
    """
    Плавный посимвольный вывод текста (typewriter-эффект).

    :param text: текст для вывода
    :param print_func: функция для вывода (например, print)
    :param char_delay: задержка между символами в секундах
    :param line_delay: дополнительная задержка после каждой строки
    """
    for line in text.split('\n'):
        for char in line:
            print_func(char, end='', flush=True)
            time.sleep(char_delay)
        print_func()
        time.sleep(line_delay)


def show_menu(options: list, get_user_input, print_func, prompt: str = "Выберите опцию:") -> Any | None:
    """
    Универсальная функция для вывода меню.
    options: список кортежей [(ключ, название), ...]
    Возвращает выбранный ключ или None при ошибке.
    """
    print_func()

    options_with_exit = options + [('', "Выход")]

    print_func(prompt)
    for i, (key, label) in enumerate(options_with_exit, 1):
        print_func(f"{i}. {label}")

    print_func()
    while True:
        try:
            choice = int(get_user_input())
            if 1 <= choice <= len(options_with_exit):
                return options_with_exit[choice - 1][0]
            print_func(f"Ошибка: введите число от 1 до {len(options_with_exit)}")
        except ValueError:
            print_func("Ошибка: нужно ввести число")
        except KeyboardInterrupt:
            print_func("\nВвод прерван пользователем.")
            return None


def print_help(options: list, print_func) -> None:
    for (option, desc) in options:
        print_func(f"{option}     {desc}")


def print_detailed_help(module: str, command: str, ui, print_func) -> None:
    """
    Выводит подробную справку по команде с учетом текущего состояния города.
    ui — это конкретный UI (TrafficManagementUI, TransportSystemUI, PublicServiceUI, SensorUI, EnergyUI и т.д.)
    """
    city = ui.city

    if command == 'unknown':
        raise ValueError("")

    header = f"\n=== Справка: {module} {command} ===\n"
    usage = ""
    context = ""

    if module == "energy":
        if command == "--optimize":
            usage = "energy --optimize"
            context = "Запускает оптимизацию энергопотребления во всех системах города."

            if city and hasattr(city, 'energy_grid'):
                grid = city.energy_grid
                if hasattr(grid, 'consumers'):
                    consumers = grid.consumers
                    context += "\n\nПодключенные системы-потребители:"
                    for i, system in enumerate(consumers):
                        system_name = type(system).__name__
                        if hasattr(system, 'device_id'):
                            dev_id = system.device_id
                        else:
                            dev_id = f"{system.address[0]} {system.address[1]}"
                        context += f"\n  {i + 1}. {system_name} {dev_id}"

            context += "\n\nСовет: Запускайте оптимизацию после изменения настроек сенсоров энергии."

    elif module == "traffic":
        if command == "--add-intersection":
            usage = "traffic --add-intersection --district <ID> [--type <simple|smart>]"
            context = "Создает новый перекресток в указанном районе."
            if city and hasattr(city, 'districts'):
                dists = list(city.districts.keys())
                context += f"\nДоступные районы: {', '.join(dists) if dists else 'Нет'}"
            context += "\nТипы перекрестков: simple (2 светофора), smart (4 светофора)"
            context += "\nПо умолчанию тип: simple"

        elif command == "--accident":
            usage = "traffic --accident --id <ID перекрестка>"
            context = "Симулирует аварию на перекрестке (срабатывает камера)."
            if city and hasattr(city, 'traffic_manager'):
                intersections = list(city.traffic_manager.intersections.keys())
                context += f"\nДоступные перекрестки: {', '.join(intersections) if intersections else 'Нет'}"
            elif city and hasattr(city, 'districts'):
                all_intersections = []
                for dist in city.districts.values():
                    if hasattr(dist, 'intersections'):
                        for inter_id in dist.intersections.keys():
                            all_intersections.append(inter_id)
                context += f"\nДоступные перекрестки: {', '.join(all_intersections) if all_intersections else 'Нет'}"

        elif command == "--manage-flow":
            usage = "traffic --manage-flow"
            context = "Управление транспортным потоком."

    elif module == "tms":
        if command == "--add-stop":
            usage = "tms --add-stop --name <Название>"
            context = "Добавляет новую физическую остановку."

        elif command == "--add-route":
            usage = "tms --add-route --stops <ID1,ID2,ID3>"
            context = "Создает маршрут. Нужны ID существующих остановок."
            if city and hasattr(city, 'tms') and hasattr(city.tms, 'physical_stops'):
                stops = [f"{sid} ({s.name})" for sid, s in city.tms.physical_stops.items()]
                context += f"\nДоступные остановки: {', '.join(stops) if stops else 'Нет'}"

        elif command == "--add-vehicle":
            usage = "tms --add-vehicle --type <bus|tram|trolleybus> --route <ID>"
            context = "Добавляет транспорт на маршрут."
            if city and hasattr(city, 'tms'):
                if hasattr(city.tms, 'routes'):
                    routes = [str(r.route_id) for r in city.tms.routes.values()]
                    context += f"\nДоступные маршруты: {', '.join(routes) if routes else 'Нет'}"
                context += "\nТипы транспорта: bus, tram, trolleybus"

        elif command == "--update-location":
            usage = "tms --update-location --vehicle <ID> --stop-index <Число>"
            context = "Обновляет местоположение транспортного средства."
            if city and hasattr(city, 'tms') and hasattr(city.tms, 'vehicles'):
                vehs = [f"{v.device_id} ({v.vehicle_type.value}), маршрут: {v.route_id}" for v in
                        city.tms.vehicles.values()]
                context += f"\nТранспорт: {', '.join(vehs) if vehs else 'Нет'}"
                context += f"\nЧтобы узнать остановки маршрута транспорта, посмотрите маршруты: tms --view-routes"

        elif command == "--arrive-stop":
            usage = "tms --arrive-stop --stop <ID>"
            context = "Транспорт прибывает на остановку."
            if city and hasattr(city, 'tms') and hasattr(city.tms, 'physical_stops'):
                stops = [f"{sid} ({s.name}),\n" for sid, s in city.tms.physical_stops.items()]
                context += f"\nДоступные остановки: {''.join(stops) if stops else 'Нет'}"

        elif command == "--view-routes":
            usage = "tms --view-routes"
            context = "Показывает все маршруты и их остановки."

        elif command == "--list-vehicles":
            usage = "tms --list-vehicles"
            context = "Показать список всех транспортных средств."

        elif command == "--list-stops":
            usage = "tms --list-stops"
            context = "Показать список всех остановок с количеством пассажиров."

    elif module == "env":
        if command == "--state":
            usage = "env --state"
            context = "Получить текущее состояние окружающей среды по всем районам."

    elif module == "data":
        if command == "--print-report":
            usage = "data --print-report"
            context = "Распечатать отчет по анализу данных города."

    elif module == "sensors":
        if command == "--list-districts":
            usage = "sensors --list-districts"
            context = "Показать список всех районов."

        elif command == "--list-sensors":
            usage = "sensors --list-sensors --district <ID> --category <type>"
            context = "Показать список сенсоров в районе."

            if city and hasattr(city, 'districts'):
                dists = list(city.districts.keys())
                context += f"\nДоступные районы: {', '.join(dists) if dists else 'Нет'}"

            context += "\nДоступные категории:"
            context += "\n  air          — Датчики качества воздуха"
            context += "\n  temperature  — Датчики температуры"
            context += "\n  humidity     — Датчики влажности"
            context += "\n  noise        — Датчики уровня шума"
            context += "\n  lights       — Уличные фонари"
            context += "\n  smart_homes  — Умные дома"
            context += "\n  traffic      — Дорожное движение"

        elif command == "--set":
            usage = "sensors --set --district <ID> --type <type> --value <N> [--home-index <N>] [--light-index <N>] [--sensor-index <N>]"
            context = "Установить значение сенсора."

            if city and hasattr(city, 'districts'):
                dists = list(city.districts.keys())
                context += f"\nДоступные районы: {', '.join(dists) if dists else 'Нет'}"

            context += "\nДоступные типы сенсоров:"
            context += "\n  water       — Счетчик воды (требуется --home-index)"
            context += "\n  thermostat  — Термостат (требуется --home-index)"
            context += "\n  light       — Светильник (требуется --home-index, --light-index)"
            context += "\n  solar       — Солнечная панель"
            context += "\n  wind        — Ветрогенератор"
            context += "\n  air         — Качество воздуха (требуется --sensor-index)"
            context += "\n  temperature — Температура (требуется --sensor-index)"
            context += "\n  humidity    — Влажность (требуется --sensor-index)"
            context += "\n  noise       — Уровень шума (требуется --sensor-index)"

            if city and hasattr(city, 'districts'):
                context += "\n\nДиапазон индексов умных домов (--home-index) по районам:"
                for dist_id, dist in city.districts.items():
                    if hasattr(dist, 'smart_homes'):
                        count = len(dist.smart_homes)
                        context += f"\n  {dist_id}: 0-{count - 1}" if count > 0 else f"\n  {dist_id}: нет умных домов"

            context += "\n\nДиапазон значений: 0-100 (для большинства сенсоров)"

        elif command == "--traffic":
            usage = "sensors --traffic --district <ID> --intersection <N> --light <ID> --type <type> --value <N>"
            context = "Установить значение транспортного сенсора на перекрестке."

            if city and hasattr(city, 'districts'):
                dists = list(city.districts.keys())
                context += f"\nДоступные районы: {', '.join(dists) if dists else 'Нет'}"

            if city and hasattr(city, 'districts'):
                context += "\nДиапазон индексов перекрестков (--intersection) по районам:"
                for dist_id, dist in city.districts.items():
                    if hasattr(dist, 'intersections'):
                        count = len(dist.intersections)
                        if count > 0:
                            context += f"\n  {dist_id}: 0-{count - 1}"

                            for i in range(len(dist.intersections)):
                                inter = dist.intersections[i]
                                if hasattr(inter, 'lights'):
                                    light_ids = [light.device_id for light in inter.lights.keys()]
                                    context += f"\n    Перекресток {inter.intersection_id}, индекс {i}; светофоры: {', '.join(light_ids)}"
                        else:
                            context += f"\n  {dist_id}: нет перекрестков"

            context += "\n\nТипы сенсоров (--type):"
            context += "\n  camera     — Камера (используйте --camera-event для событий)"
            context += "\n  flow       — Датчик потока транспорта"
            context += "\n  pedestrian — Датчик пешеходов"

            context += "\n\nДиапазон значений: 0-100"

        elif command == "--camera-event":
            usage = "sensors --camera-event --district <ID> --intersection <N> --light <ID> --vehicle <type> [--incident <true|false>]"
            context = "Симулировать событие камеры (проезд транспорта или ДТП)."

            if city and hasattr(city, 'districts'):
                dists = list(city.districts.keys())
                context += f"\nДоступные районы: {', '.join(dists) if dists else 'Нет'}"

            if city and hasattr(city, 'districts'):
                context += "\nИндексы перекрестков (--intersection):"
                for dist_id, dist in city.districts.items():
                    if hasattr(dist, 'intersections'):
                        count = len(dist.intersections)
                        context += f"\n  {dist_id}: 0-{count - 1}" if count > 0 else f"\n  {dist_id}: нет перекрестков"

            context += "\n\nТипы транспорта (--vehicle):"
            context += "\n  bus        — Автобус"
            context += "\n  tram       — Трамвай"
            context += "\n  trolleybus — Троллейбус"
            context += "\n  car        — Легковой автомобиль"
            context += "\n\nПараметр --incident:"
            context += "\n  true  — Зафиксировано ДТП"
            context += "\n  false — Обычный проезд (по умолчанию)"



    elif module == "services":

        if command == "--register":
            usage = ("services --register --name <Имя> --surname <Фамилия> "
                     "--age <N> --street <Улица> --house <N> [--apartment <N>]")
            context = "Зарегистрировать нового пользователя в системе."
            context += "\nТребования:"
            context += "\n  - Имя/Фамилия: только буквы, 2-50 символов"
            context += "\n  - Возраст: 0-150"
            context += "\n  - Дом: положительное число"

        elif command == "--login":
            usage = "services --login --id <USER_ID>"
            context = "Авторизовать пользователя по ID."
            if hasattr(ui.city, 'user_repo') and ui.city.user_repo:
                context += "\nЗарегистрированные пользователи:"
                for user_id, user in ui.city.user_repo.get_all_users().items():
                    context += f"\n{user_id}: {user['name']} {user['surname']}"

        elif command == "--whoami":
            usage = "services --whoami"
            context = "Показать информацию о текущем авторизованном пользователе."
            if hasattr(ui, 'current_user_id') and ui.current_user_id:
                context += f"\nТекущий пользователь: {ui.current_user_id}"
            else:
                context += "\nПользователь не авторизован"

        elif command == "--hospital":
            usage = "services --hospital --action <action> [--doctor <key>] [--purpose <text>]"
            context = "Взаимодействие с больницей."
            context += "\nДействия:"
            context += "\n  get_ticket        — Записаться к врачу (требуется --doctor)"
            context += "\n  order_certificate — Заказать справку (требуется --purpose)"
            context += "\n  call_ambulance    — Вызвать скорую"
            context += "\n  list_doctors      — Показать список врачей и свободные места"

            if city and hasattr(city, 'hospital'):
                hospital = city.hospital
                if hasattr(hospital, 'doctors'):
                    doctors = hospital.doctors
                    context += "\n\nВрачи (ключ — для get_ticket):"
                    for key, data in doctors.items():
                        available = data['limit'] - data['current']
                        status = f"{available}/{data['limit']} мест" if available > 0 else " Нет мест"
                        context += f"\n  - {key}: {data['name']} ({status})"

            context += "\n\nСовет: Используйте --action list_doctors, чтобы увидеть актуальное количество мест перед записью."
            if hasattr(ui, 'current_user_id') and not ui.current_user_id:
                context += "\nТребуется авторизация (services --login)"

        elif command == "--school":
            usage = "services --school --action <action> [--course <name>] [--subject <name>] [--grade <1-10>]"
            context = "Взаимодействие со школой/образованием."
            context += "\nДействия:"
            context += "\n  enroll_course — Записаться на курс (требуется --course)"
            context += "\n  set_grade     — Установить оценку (требуется --subject, --grade)"
            context += "\n  get_grades    — Получить свои оценки"
            context += "\n  list_courses  — Показать доступные курсы"

            if city and hasattr(city, 'educational_service'):
                edu_service = city.educational_service
                if hasattr(edu_service, 'courses'):
                    courses = edu_service.courses
                    context += "\n\nДоступные курсы:"
                    for course_name, seats in courses.items():
                        status = f"{seats} мест" if seats > 0 else "Нет мест"
                        context += f"\n  - {course_name}: {status}"

            context += "\n\nОценки: диапазон 1-10"
            if hasattr(ui, 'current_user_id') and not ui.current_user_id:
                context += "\nТребуется авторизация (services --login)"

        elif command == "--utility":
            usage = "services --utility --action <action> [--description <text>]"
            context = "Взаимодействие с коммунальными службами."
            context += "\nДействия:"
            context += "\n  view_metrics   — Просмотреть показатели потребления"
            context += "\n  report_issue   — Сообщить о проблеме (требуется --description)"
            if hasattr(ui, 'current_user_id') and not ui.current_user_id:
                context += "\nТребуется авторизация (services --login)"

        elif command == "--exit":
            usage = "services --exit"
            context = "Выйти из меню общественных сервисов."

    print_func(header)
    print_func(f"Использование:\n  {usage}\n")
    if context:
        print_func(f"Контекст:\n{context}\n")
    print_func("Флаги:\n  --help : Показать эту справку")
    print_func("==============================\n")
