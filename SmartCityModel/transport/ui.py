from core import VehicleType
from sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor
from ui import show_menu
from . import TransportMonitoringSystem, BusStop, PublicTransportVehicle, TransportRoute, RouteStop, Intersection, \
    TrafficManager, SmartTrafficLight


class TransportSystemUI:
    def __init__(self):
        self.tms = TransportMonitoringSystem()
        # Словари: ключи - строки (ID), значения - объекты
        self.tms.physical_stops = {
            "s1": BusStop("s1", "Пл. Ленина"),
            "s2": BusStop("s2", "Универмаг"),
            "s3": BusStop("s3", "Парк Горького"),
            "s4": BusStop("s4", "Вокзал"),
            "s5": BusStop("s5", "Пл. Победы"),
            "s6": BusStop("s6", "Пл. Якуба Коласа"),
            "s7": BusStop("s7", "Комаровский Рынок"),
            "s8": BusStop("s8", "Ст. метро Петровщина")
        }
        self.tms.vehicles = {
            "bus_1": PublicTransportVehicle("bus_1", VehicleType.BUS, "r1"),
            "bus_2": PublicTransportVehicle("bus_2", VehicleType.BUS, "r2"),
            "tram_3": PublicTransportVehicle("tram_3", VehicleType.TRAM, "r3")
        }
        self.tms.routes = {
            "r1": TransportRoute("r1", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i < len(self.tms.physical_stops) - 2], avg_time_between_stops=4),
            "r2": TransportRoute("r2", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i % 2 == 0], avg_time_between_stops=8),
            "r3": TransportRoute("r3", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i > 2], avg_time_between_stops=4)
        }

    PublicVehicleType = {
        VehicleType.BUS: "Автобус",
        VehicleType.TRAM: "Трамвай",
        VehicleType.TROLLEYBUS: "Троллейбус"
    }
    tms_options = [(1, "Добавить маршрут"), (2, "Добавить транспортное средство"), (3, "Добавить остановку"),
                   (4, "Обновить локацию средства"),
                   (5, "Посмотреть табло остановки"), (6, "Выйти")]

    def menu(self, get_user_input, print_func):
        while True:

            key = show_menu(self.tms_options, get_user_input, print_func)
            if not key:
                return

            match key:
                case 1:
                    stops = []
                    while True:
                        # Получаем ID уже добавленных остановок для фильтрации
                        existing_stop_ids = [route_stop.stop.stop_id for route_stop in stops]

                        # Формируем меню: только те остановки, которых нет в маршруте
                        ops = [(stop_id, stop_obj.name)
                               for stop_id, stop_obj in self.tms.physical_stops.items()
                               if stop_id not in existing_stop_ids]

                        # Если все остановки уже добавлены, завершаем выбор автоматически
                        if not ops:
                            print_func("Все остановки уже добавлены в маршрут.")
                            break

                        ops.append(("", "Закончить выбор"))

                        stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку маршрута:")

                        if stop_key is "":
                            break

                        stops.append(RouteStop(self.tms.physical_stops[stop_key], len(stops)))

                    if not stops:
                        print_func("Маршрут не может быть пустым.")
                        return

                    new_r_id = f"r{len(self.tms.routes) + 1}"

                    self.tms.register_route(TransportRoute(new_r_id, stops))
                    print_func(f"Добавлен маршрут: {new_r_id}")

                case 2:  # Добавить транспортное средство
                    # 1. Выбор типа транспорта
                    ops = [(v_type_key, v_type_val) for v_type_key, v_type_val in self.PublicVehicleType.items()]
                    v_type = show_menu(ops, get_user_input, print_func, "Выберите тип транспорта:")
                    if v_type is None: return

                    # 2. Выбор маршрута (КЛЮЧЕВОЙ МОМЕНТ)
                    # В меню передаем ID маршрутов (строки "r1", "r2"...), чтобы пользователь выбрал конкретный
                    route_ops = [(r_id, f"{r_id}") for r_id in self.tms.routes.keys()]
                    route_id = show_menu(route_ops, get_user_input, print_func, "Выберите маршрут транспорта:")

                    if route_id is None: return

                    # Генерация ID транспорта
                    new_v_id = f"{v_type.name.lower()}_{len(self.tms.vehicles) + 1}"

                    # Регистрация: привязываем транспорт к выбранному route_id
                    self.tms.register_vehicle(
                        PublicTransportVehicle(new_v_id, v_type, route_id)
                    )
                    print_func(f"Добавлен транспорт: {new_v_id} на маршрут {route_id}")

                case 3:  # Добавить остановку
                    print_func("Введите название новой остановки: ")
                    new_st_name = get_user_input()
                    new_st_id = f"s{len(self.tms.physical_stops) + 1}"
                    self.tms.physical_stops[new_st_id] = BusStop(new_st_id, new_st_name)
                    print_func(f"Добавлена остановка: {new_st_name}")

                case 4:
                    ops = [(vehicle_id, f"{self.PublicVehicleType[vehicle_obj.vehicle_type]}: {vehicle_id}")
                           for vehicle_id, vehicle_obj in self.tms.vehicles.items()]
                    v_key = show_menu(ops, get_user_input, print_func, "Выберите средство:")
                    vehicle = self.tms.vehicles[v_key]
                    ops = [(stop.index, stop.bus_stop.name) for stop in self.tms.routes[vehicle.route_id].stops]
                    stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку:")
                    print_func(self.tms.vehicles[v_key].report_stop_passed(stop_key))

                case 4:  # Посмотреть табло
                    # Выбор остановки по ключу словаря
                    ops = [(stop_id, stop_obj.name) for stop_id, stop_obj in self.tms.physical_stops.items()]
                    stop_id = show_menu(ops, get_user_input, print_func, "Выберите остановку:")

                    if stop_id is None: return

                    info = self.tms.get_arrival_info(stop_id)
                    print_func(f"Остановка: {info['stop_name']}")

                    if "arrivals" in info and info["arrivals"]:
                        print_func("Ближайший транспорт:")
                        for arrival in info["arrivals"]:
                            print_func(
                                f" - {arrival['type'].upper()} {arrival['route']}: через {arrival['eta_minutes']} мин.")
                    else:
                        print_func("Нет ближайшего транспорта.")

                    status = self.tms.physical_stops[stop_id].get_status()
                    print_func(f"\nТабло на остановке: '{status.get('display', 'Нет данных')}'")
                case 5:
                    return


class TrafficManagementUI:
    def __init__(self, tms: TransportMonitoringSystem, intersections: list[Intersection]):
        self.manager = TrafficManager(tms, intersections)
        self.available_options = [
            (1, "Добавить переход"),
            (2, "Попасть в аварию"),
            (3, "Управление транспортным потоком"),
            (4, "Выйти")
        ]

    def menu(self, get_user_input, print_func):
        key = show_menu(self.available_options, get_user_input, print_func)
        if not key:
            return
        match key:
            case 1:
                lights = []
                for _ in range(4):
                    lights.append(SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()))
                int_key = show_menu([(1, "Простой переход"), (2, "Перекресток")], get_user_input, print_func,
                                    "Вы хотите создать:")
                if key:
                    keyword = "inter_"
                    if key == 1:
                        lights = lights[:2]
                        keyword = "cross_"
                    int_id = keyword + str(len(self.manager.intersections))
                    inter = Intersection(int_id, lights)
                    self.manager.register_intersection(inter)
                    print_func(f"Добавлен переход: {int_id}")
            case 2:
                ops = [(int_id, f"Переход {int_id}") for int_id in self.manager.intersections.keys()]
                int_key = show_menu(ops, get_user_input, print_func, "Выберите переход:")
                if int_key:
                    lights = self.manager.intersections[int_key].lights
                    lights[next(iter(lights))].camera.detect_event(VehicleType.CAR, True)

            case 3:
                print_func("========== Операция управления транспортным потоком ==========")
                self.manager.prioritize_public_transport()
                for intersection in self.manager.intersections.values():
                    status = intersection.regulate_intersection()
                    if status:
                        print_func(f"Внимание! Авария на переходе {intersection.intersection_id}!")
                    else:
                        print_func(f"Движение на переходе {intersection.intersection_id} отрегулировано.")
            case 4:
                return
