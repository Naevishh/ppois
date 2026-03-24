from ..city import SmartCity
from ..core import VehicleType
from ..core.utils import NAME_VALIDATOR, PASSENGER_VALIDATOR, SafeInput
from ..sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor
from ..core import show_menu
from ..transport.traffic_control import SmartTrafficLight, Intersection
from ..transport.models import BusStop, PublicTransportVehicle, TransportRoute, RouteStop



class TransportSystemUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.stop_name_validator = NAME_VALIDATOR
        self.passenger_validator = PASSENGER_VALIDATOR

    PublicVehicleType = {
        VehicleType.BUS: "Автобус",
        VehicleType.TRAM: "Трамвай",
        VehicleType.TROLLEYBUS: "Троллейбус"
    }
    tms_options = [(1, "Добавить маршрут"), (2, "Добавить транспортное средство"), (3, "Добавить остановку"),
                   (4, "Обновить локацию средства"),
                   (5, "Прийти на остановку"), (6, "Посмотреть маршруты")]

    def menu(self, get_user_input, print_func) -> None:
        while True:

            key = show_menu(self.tms_options, get_user_input, print_func)

            match key:
                case 1:
                    stops = []
                    while True:
                        # Получаем ID уже добавленных остановок для фильтрации
                        existing_stop_ids = [route_stop.bus_stop.device_id for route_stop in stops]

                        # Формируем меню: только те остановки, которых нет в маршруте
                        ops = [(stop_id, stop_obj.name)
                               for stop_id, stop_obj in self.city.tms.physical_stops.items()
                               if stop_id not in existing_stop_ids]

                        # Если все остановки уже добавлены, завершаем выбор автоматически
                        if not ops:
                            print_func("Все остановки уже добавлены в маршрут.")
                            break

                        stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку маршрута:")

                        if stop_key == '':
                            break

                        stops.append(RouteStop(self.city.tms.physical_stops[stop_key], len(stops)))

                    if not stops:
                        print_func("Маршрут не может быть пустым.")
                        break

                    new_r_id = f"r{len(self.city.tms.routes) + 1}"

                    self.city.tms.register_route(TransportRoute(new_r_id, stops))
                    print_func(f"Добавлен маршрут: {new_r_id}")

                case 2:  # Добавить транспортное средство
                    # 1. Выбор типа транспорта
                    ops = [(v_type_key, v_type_val) for v_type_key, v_type_val in self.PublicVehicleType.items()]
                    v_type = show_menu(ops, get_user_input, print_func, "Выберите тип транспорта:")
                    if v_type == '':
                        break

                    # 2. Выбор маршрута (КЛЮЧЕВОЙ МОМЕНТ)
                    # В меню передаем ID маршрутов (строки "r1", "r2"...), чтобы пользователь выбрал конкретный
                    route_ops = [(r_id, f"{r_id}") for r_id in self.city.tms.routes.keys()]
                    route_id = show_menu(route_ops, get_user_input, print_func, "Выберите маршрут транспорта:")

                    if route_id == '':
                        break

                    # Регистрация: привязываем транспорт к выбранному route_id
                    self.city.tms.register_vehicle(
                        PublicTransportVehicle(v_type, route_id)
                    )
                    print_func(f"Добавлен транспорт: {list(self.city.tms.vehicles.values())[-1].device_id} на маршрут {route_id}")

                case 3:  # Добавить остановку
                    new_st_name = SafeInput.get_string(
                        "Введите название новой остановки: ",
                        self.stop_name_validator,
                        get_user_input,
                        print_func
                    )
                    new_stop = BusStop(new_st_name)
                    self.city.tms.physical_stops[new_stop.device_id] = new_stop
                    print_func(f"Добавлена остановка: {new_st_name}")

                case 4:
                    ops = [(vehicle_id, f"{self.PublicVehicleType[vehicle_obj.vehicle_type]}: {vehicle_id}")
                           for vehicle_id, vehicle_obj in self.city.tms.vehicles.items()]
                    v_key = show_menu(ops, get_user_input, print_func, "Выберите средство:")
                    if v_key == '':
                        break
                    vehicle = self.city.tms.vehicles[v_key]
                    ops = [(stop.index, stop.bus_stop.name) for stop in self.city.tms.routes[vehicle.route_id].stops]
                    stop_key = show_menu(ops, get_user_input, print_func, "Выберите остановку:")
                    if stop_key == '':
                        break
                    print_func(self.city.tms.vehicles[v_key].report_stop_passed(stop_key))

                case 5:  # Посмотреть табло
                    # Выбор остановки по ключу словаря
                    ops = [(stop_id, stop_obj.name) for stop_id, stop_obj in self.city.tms.physical_stops.items()]
                    stop_id = show_menu(ops, get_user_input, print_func, "Выберите остановку:")

                    if stop_id == '':
                        break

                    stop = self.city.tms.physical_stops[stop_id]
                    stop.update_passengers(stop.get_status()["passengers"] + 1)
                    info = self.city.tms.get_arrival_info(stop_id)
                    print_func(f"Остановка: {info['stop_name']}")

                    just_arrived = []
                    if "arrivals" in info and info["arrivals"]:
                        for arrival in info["arrivals"]:
                            if arrival["eta_minutes"] == 0:
                                just_arrived.append(arrival)
                                print_func(f"Сейчас на остановке: "
                                           f"\n - {arrival['type'].upper()}, маршрут: {arrival['route']}")
                        if len(just_arrived) != len(info["arrivals"]):
                            print_func("Ближайший транспорт:")
                            for arrival in info["arrivals"]:
                                if arrival["eta_minutes"] > 0:
                                    print_func(
                                        f" - {arrival['type'].upper()}, маршрут: {arrival['route']}: "
                                        f"через {arrival['eta_minutes']} мин.")
                    else:
                        print_func("Нет ближайшего транспорта.")

                    if just_arrived:
                        ops = [(1, "Сесть на транспорт")]
                        op_key = show_menu(ops, get_user_input, print_func)
                        if op_key == 1:
                            ops = [
                                (arrival["vehicle_id"], f"{arrival['type'].upper()}, маршрут: {arrival['route']}")
                                for arrival in just_arrived]
                            key_id = show_menu(ops, get_user_input, print_func)
                            if key_id:
                                print_func(self.city.tms.get_in_vehicle(key_id))

                    stop.update_passengers(stop.get_status()["passengers"] - 1)

                case 6:
                    for i, (route_id, route) in enumerate(self.city.tms.routes.items(), 1):
                        print_func(f"{i}) {route_id}"
                                   f"\n"
                                   f"\nОстановки:")
                        for j, stop in enumerate(route.stops, 1):
                            print_func(f"{j}. {stop.bus_stop.name}")
                        print_func(f"\nТранспорт:")
                        for j, veh in enumerate(route.vehicles, 1):
                            print_func(f"{j}. {veh.device_id}")
                            print_func()

                case '':
                    return


class TrafficManagementUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.available_options = [
            (1, "Добавить перекресток"),
            (2, "Попасть в аварию"),
            (3, "Управление транспортным потоком")
        ]

    def menu(self, get_user_input, print_func) -> None:
        while True:

            key = show_menu(self.available_options, get_user_input, print_func)
            match key:
                case 1:
                    lights = []
                    for _ in range(4):
                        lights.append(SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()))
                    int_key = show_menu([(1, "Простой переход"), (2, "Перекресток")], get_user_input, print_func,
                                        "Вы хотите создать:")
                    if int_key == '':
                        break
                    dists = [(dist_id, dist) for dist_id, dist in self.city.districts.items()]
                    dist_key = show_menu(dists, get_user_input, print_func,
                                        "Выберите, в какой район добавить перекресток:")
                    if dist_key == '':
                        break
                    dist = self.city.districts[dist_key]
                    int_id = f"{dist.district_id}_{len(dist.intersections) + 1}"
                    if int_key == 1:
                        lights = lights[:2]
                    inter = Intersection(int_id, lights)
                    dist.register_intersection(inter)
                    print_func(f"Добавлен переход: {int_id}")

                case 2:
                    ops = [(int_id, f"Переход {int_id}") for int_id in self.city.traffic_manager.intersections.keys()]
                    int_key = show_menu(ops, get_user_input, print_func, "Выберите переход:")
                    if int_key:
                        lights = self.city.traffic_manager.intersections[int_key].lights
                        next(iter(lights)).camera.detect_event(VehicleType.CAR, True)

                case 3:
                    print_func("========== Операция управления транспортным потоком ==========")
                    self.city.traffic_manager.prioritize_public_transport(print_func)
                    for intersection in self.city.traffic_manager.intersections.values():
                        status = intersection.regulate_intersection()
                        if status:
                            print_func(f"Внимание! Авария на переходе {intersection.intersection_id}!")
                        else:
                            print_func(f"Движение на переходе {intersection.intersection_id} отрегулировано.")
                case '':
                    return