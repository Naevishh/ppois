from ..city import SmartCity
from ..core import VehicleType
from ..core.utils import NAME_VALIDATOR, PASSENGER_VALIDATOR
from ..sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor
from ..transport.traffic_control import SmartTrafficLight, Intersection
from ..transport.models import BusStop, PublicTransportVehicle, TransportRoute, RouteStop


class TransportSystemUI:
    """UI модуль для системы управления транспортом (TMS)"""

    PublicVehicleType = {
        VehicleType.BUS: "Автобус",
        VehicleType.TRAM: "Трамвай",
        VehicleType.TROLLEYBUS: "Троллейбус"
    }

    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.stop_name_validator = NAME_VALIDATOR
        self.passenger_validator = PASSENGER_VALIDATOR

    # ============================================================
    # CLI МЕТОДЫ (принимают аргументы напрямую, без input/menu)
    # ============================================================

    def add_stop(self, name: str) -> str:
        """
        Добавить остановку по имени.
        Возвращает device_id созданной остановки.
        """
        if not self.stop_name_validator(name):
            raise ValueError(f"Некорректное название остановки: {name}")

        new_stop = BusStop(name)
        self.city.tms.physical_stops[new_stop.device_id] = new_stop
        return new_stop.device_id

    def add_route(self, stop_ids: list[str]) -> str:
        """
        Добавить маршрут со списком остановок.
        :param stop_ids: Список ID остановок (например: ["stop_1", "stop_2", "stop_3"])
        :return: ID созданного маршрута
        """
        if not stop_ids:
            raise ValueError("Маршрут не может быть пустым")

        # 1. Проверка на дубликаты остановок
        seen = set()
        duplicates = set()
        for stop_id in stop_ids:
            if stop_id in seen:
                duplicates.add(stop_id)
            else:
                seen.add(stop_id)

        if duplicates:
            raise ValueError(f"Обнаружены дубликаты остановок: {', '.join(sorted(duplicates))}")

        # 2. Валидация: все остановки должны существовать
        for stop_id in stop_ids:
            if stop_id not in self.city.tms.physical_stops.keys():
                raise ValueError(f"Остановка {stop_id} не найдена")

        # 3. Создаём RouteStop объекты
        stops = [
            RouteStop(self.city.tms.physical_stops[stop_id], index)
            for index, stop_id in enumerate(stop_ids)
        ]

        # 4. Регистрируем маршрут
        new_r_id = f"r{len(self.city.tms.routes) + 1}"
        self.city.tms.register_route(TransportRoute(new_r_id, stops))
        return new_r_id

    def add_vehicle(self, vehicle_type: str, route_id: str) -> str:
        """
        Добавить транспортное средство.
        :param vehicle_type: Тип транспорта ("bus", "tram", "trolleybus")
        :param route_id: ID маршрута (например: "r1")
        :return: device_id созданного транспорта
        """
        # Преобразуем строку в VehicleType
        type_map = {
            "bus": VehicleType.BUS,
            "tram": VehicleType.TRAM,
            "trolleybus": VehicleType.TROLLEYBUS
        }

        if vehicle_type.lower() not in type_map:
            raise ValueError(f"Неизвестный тип транспорта: {vehicle_type}. "
                             f"Допустимые: {', '.join(type_map.keys())}")

        v_type = type_map[vehicle_type.lower()]

        if route_id not in self.city.tms.routes:
            raise ValueError(f"Маршрут {route_id} не найден")

        vehicle = PublicTransportVehicle(v_type, route_id)
        self.city.tms.register_vehicle(vehicle)
        return vehicle.device_id

    def update_vehicle_location(self, vehicle_id: str, stop_index: int) -> str:
        """
        Обновить локацию транспортного средства (сообщить о прохождении остановки).
        :param vehicle_id: ID транспортного средства
        :param stop_index: Индекс остановки в маршруте (0-based)
        :return: Сообщение о результате
        """
        if vehicle_id not in self.city.tms.vehicles:
            raise ValueError(f"Транспорт {vehicle_id} не найден")

        vehicle = self.city.tms.vehicles[vehicle_id]

        route = self.city.tms.routes[vehicle.route_id]

        if stop_index < 0 or stop_index >= len(route.stops):
            raise ValueError(f"Некорректный индекс остановки: {stop_index}. "
                             f"Допустимый диапазон: 0-{len(route.stops) - 1}")

        return vehicle.report_stop_passed(stop_index)

    def arrive_at_stop(self, stop_id: str) -> dict:
        """
        Симулировать приход пассажира на остановку и получить информацию о прибытии.
        :param stop_id: ID остановки
        :return: Информация о прибытии транспорта
        """
        if stop_id not in self.city.tms.physical_stops:
            raise ValueError(f"Остановка {stop_id} не найдена")

        stop = self.city.tms.physical_stops[stop_id]

        # Симуляция прихода пассажира
        stop.update_passengers(stop.get_status()["passengers"] + 1)

        info = self.city.tms.get_arrival_info(stop_id)

        # Уменьшаем обратно (так как это просто запрос информации)
        stop.update_passengers(stop.get_status()["passengers"] - 1)

        return info

    def list_routes(self) -> list[dict]:
        """
        Получить список всех маршрутов с информацией.
        :return: Список словарей с информацией о маршрутах
        """
        routes_info = []

        for route_id, route in self.city.tms.routes.items():
            route_data = {
                "route_id": route_id,
                "stops": [stop.bus_stop.name for stop in route.stops],
                "vehicles": [veh.device_id for veh in route.vehicles]
            }
            routes_info.append(route_data)

        return routes_info

    def get_vehicle_list(self) -> list[dict]:
        """
        Получить список всех транспортных средств.
        :return: Список словарей с информацией о транспорте
        """
        vehicles_info = []

        for vehicle_id, vehicle in self.city.tms.vehicles.items():
            vehicle_data = {
                "device_id": vehicle_id,
                "type": self.PublicVehicleType.get(vehicle.vehicle_type, "неизвестный тип"),
                "route_id": vehicle.route_id
            }
            vehicles_info.append(vehicle_data)

        return vehicles_info

    def get_stop_list(self) -> list[dict]:
        """
        Получить список всех остановок.
        :return: Список словарей с информацией об остановках
        """
        stops_info = []

        for stop_id, stop in self.city.tms.physical_stops.items():
            stop_data = {
                "device_id": stop_id,
                "name": stop.name,
                "passengers": stop.get_status()["passengers"]
            }
            stops_info.append(stop_data)

        return stops_info

    # ============================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ для парсера в cli.py
    # ============================================================

    def format_routes_output(self, routes: list[dict], print_func) -> None:
        """Красиво вывести информацию о маршрутах"""
        if not routes:
            print_func("Маршруты не найдены")
            return

        for route in routes:
            print_func(f"\nМаршрут: {route['route_id']}")
            print_func("   Остановки:")
            for i, stop_name in enumerate(route['stops'], 1):
                print_func(f"     {i}. {stop_name}")
            print_func("   Транспорт:")
            if route['vehicles']:
                for veh_id in route['vehicles']:
                    print_func(f"     - {veh_id}")
            else:
                print_func("     - Нет транспорта на маршруте")

    def format_arrival_info(self, info: dict, print_func) -> None:
        """Красиво вывести информацию о прибытии"""
        print_func(f"Остановка: {info['stop_name']}")

        if "arrivals" in info and info["arrivals"]:
            just_arrived = [a for a in info["arrivals"] if a["eta_minutes"] == 0]
            upcoming = [a for a in info["arrivals"] if a["eta_minutes"] > 0]

            if just_arrived:
                print_func("\nСейчас на остановке:")
                for arrival in just_arrived:
                    print_func(f"   - {arrival['type'].upper()}, маршрут: {arrival['route']}")

            if upcoming:
                print_func("\nБлижайший транспорт:")
                for arrival in upcoming:
                    print_func(f"   - {arrival['type'].upper()}, маршрут: {arrival['route']}: "
                               f"через {arrival['eta_minutes']} мин.")
        else:
            print_func("Нет ближайшего транспорта")


class TrafficManagementUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city

    def add_intersection(self, district_id: str, type_: str):
        """Создает перекресток. Не спрашивает пользователя, не печатает меню."""
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]
        int_id = f"{dist.district_id}_{len(dist.intersections) + 1}"

        # Логика создания светофоров
        lights = []
        count = 2 if type_ == "simple" else 4
        for _ in range(count):
            lights.append(SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()))

        inter = Intersection(int_id, lights)
        dist.register_intersection(inter)
        return int_id

    def trigger_accident(self, intersection_id: str):
        """Симулирует аварию по ID."""
        if intersection_id in self.city.traffic_manager.intersections:
            lights = self.city.traffic_manager.intersections[intersection_id].lights
            next(iter(lights)).camera.detect_event(VehicleType.CAR, True)
        else:
            raise ValueError("Перекресток не найден")

    def manage_flow(self):
        result=self.city.traffic_manager.prioritize_public_transport()
        for intersection in self.city.traffic_manager.intersections.values():
            status = intersection.regulate_intersection()
            if status:
                result+= f"\nВнимание! Авария на переходе {intersection.intersection_id}!"
            else:
                result+= f"\nДвижение на переходе {intersection.intersection_id} отрегулировано."
        return result