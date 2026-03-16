from core import VehicleType
from ui import show_menu
from . import BusStop, PublicTransportVehicle, TransportRoute, RouteStop
from city import SmartCity


class TransportSystemUI:
    def __init__(self, city: SmartCity):
        self.city=city

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
                               for stop_id, stop_obj in self.city.tms.physical_stops.items()
                               if stop_id not in existing_stop_ids]

                        # Если все остановки уже добавлены, завершаем выбор автоматически
                        if not ops:
                            print_func("Все остановки уже добавлены в маршрут.")
                            break

                        ops.append(("", "Закончить выбор"))

                        stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку маршрута:")

                        if stop_key is "":
                            break

                        stops.append(RouteStop(self.city.tms.physical_stops[stop_key], len(stops)))

                    if not stops:
                        print_func("Маршрут не может быть пустым.")
                        return

                    new_r_id = f"r{len(self.city.tms.routes) + 1}"

                    self.city.tms.register_route(TransportRoute(new_r_id, stops))
                    print_func(f"Добавлен маршрут: {new_r_id}")

                case 2:  # Добавить транспортное средство
                    # 1. Выбор типа транспорта
                    ops = [(v_type_key, v_type_val) for v_type_key, v_type_val in self.PublicVehicleType.items()]
                    v_type = show_menu(ops, get_user_input, print_func, "Выберите тип транспорта:")
                    if v_type is None: return

                    # 2. Выбор маршрута (КЛЮЧЕВОЙ МОМЕНТ)
                    # В меню передаем ID маршрутов (строки "r1", "r2"...), чтобы пользователь выбрал конкретный
                    route_ops = [(r_id, f"{r_id}") for r_id in self.city.tms.routes.keys()]
                    route_id = show_menu(route_ops, get_user_input, print_func, "Выберите маршрут транспорта:")

                    if route_id is None: return

                    # Генерация ID транспорта
                    new_v_id = f"{v_type.name.lower()}_{len(self.city.tms.vehicles) + 1}"

                    # Регистрация: привязываем транспорт к выбранному route_id
                    self.city.tms.register_vehicle(
                        PublicTransportVehicle(new_v_id, v_type, route_id)
                    )
                    print_func(f"Добавлен транспорт: {new_v_id} на маршрут {route_id}")

                case 3:  # Добавить остановку
                    print_func("Введите название новой остановки: ")
                    new_st_name = get_user_input()
                    new_st_id = f"s{len(self.city.tms.physical_stops) + 1}"
                    self.city.tms.physical_stops[new_st_id] = BusStop(new_st_id, new_st_name)
                    print_func(f"Добавлена остановка: {new_st_name}")

                case 4:
                    ops = [(vehicle_id, f"{self.PublicVehicleType[vehicle_obj.vehicle_type]}: {vehicle_id}")
                           for vehicle_id, vehicle_obj in self.city.tms.vehicles.items()]
                    v_key = show_menu(ops, get_user_input, print_func, "Выберите средство:")
                    vehicle = self.city.tms.vehicles[v_key]
                    ops = [(stop.index, stop.bus_stop.name) for stop in self.city.tms.routes[vehicle.route_id].stops]
                    stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку:")
                    print_func(self.city.tms.vehicles[v_key].report_stop_passed(stop_key))

                case 4:  # Посмотреть табло
                    # Выбор остановки по ключу словаря
                    ops = [(stop_id, stop_obj.name) for stop_id, stop_obj in self.city.tms.physical_stops.items()]
                    stop_id = show_menu(ops, get_user_input, print_func, "Выберите остановку:")

                    if stop_id is None: return

                    info = self.city.tms.get_arrival_info(stop_id)
                    print_func(f"Остановка: {info['stop_name']}")

                    if "arrivals" in info and info["arrivals"]:
                        print_func("Ближайший транспорт:")
                        for arrival in info["arrivals"]:
                            print_func(
                                f" - {arrival['type'].upper()} {arrival['route']}: через {arrival['eta_minutes']} мин.")
                    else:
                        print_func("Нет ближайшего транспорта.")

                    status = self.city.tms.physical_stops[stop_id].get_status()
                    print_func(f"\nТабло на остановке: '{status.get('display', 'Нет данных')}'")
                case 5:
                    return


class TrafficManagementUI:
    def __init__(self, city: SmartCity):
        self.city=city
        self.available_options = [
            (1, "Попасть в аварию"),
            (2, "Управление транспортным потоком"),
            (3, "Выйти")
        ]

    def menu(self, get_user_input, print_func):
        key = show_menu(self.available_options, get_user_input, print_func)
        if not key:
            return
        match key:
            case 1:
                ops = [(int_id, f"Переход {int_id}") for int_id in self.city.traffic_manager.intersections.keys()]
                int_key = show_menu(ops, get_user_input, print_func, "Выберите переход:")
                if int_key:
                    lights = self.city.traffic_manager.intersections[int_key].lights
                    lights[next(iter(lights))].camera.detect_event(VehicleType.CAR, True)

            case 2:
                print_func("========== Операция управления транспортным потоком ==========")
                self.city.traffic_manager.prioritize_public_transport()
                for intersection in self.city.traffic_manager.intersections.values():
                    status = intersection.regulate_intersection()
                    if status:
                        print_func(f"Внимание! Авария на переходе {intersection.intersection_id}!")
                    else:
                        print_func(f"Движение на переходе {intersection.intersection_id} отрегулировано.")
            case 3:
                return
