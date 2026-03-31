from ..core import SmartDevice, TrafficLightColor, VehicleType, Direction, Domain
from ..core.exceptions import TransportException
from ..sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor
from ..transport import TransportMonitoringSystem


class SmartTrafficLight(SmartDevice):
    def __init__(self,
                 flow_sensor: TrafficFlowSensor,
                 camera: AITrafficCamera,
                 pedestrian_sensor: PedestrianCrossingSensor = None) -> None:
        super().__init__("tl_", Domain.TRANSPORTATION)
        self.flow_sensor = flow_sensor
        self.camera = camera
        self._current_color = TrafficLightColor.RED
        self.pedestrian_sensor = pedestrian_sensor

    def get_traffic_request(self) -> dict:
        status = self.camera.get_status()
        intensity = self.flow_sensor.get_status()

        priority = 10  # Базовый низкий приоритет
        pedestrian_waiting = False
        reason = "FLOW"

        if status['incident']:
            priority = 100
            reason = "INCIDENT"
        elif status['vehicle_type'] in [VehicleType.AMBULANCE, VehicleType.FIRE_TRUCK, VehicleType.POLICE]:
            priority = 90
            reason = "EMERGENCY"
        elif status['vehicle_type'] in [VehicleType.TROLLEYBUS, VehicleType.TRAM, VehicleType.BUS]:
            priority = 60
            reason = "HIGH_FLOW"
        elif intensity > 15:
            priority = 50
            reason = "HIGH_FLOW"

        # Пешеходы
        if self.pedestrian_sensor:
            p_status = self.pedestrian_sensor.get_status()
            if p_status > intensity:
                pedestrian_waiting = True
                priority = 5
                reason = "PEDESTRIANS_WAITING"

        return {
            "device_id": self.device_id,
            "priority": priority,
            "pedestrian_waiting": pedestrian_waiting,
            "reason": reason
        }

    def set_color(self, color: TrafficLightColor) -> None:
        self._current_color = color


class Intersection:
    def __init__(self, intersection_id: str, lights: list[SmartTrafficLight]) -> None:
        if len(lights) == 2:
            self.conflict_map = {}
            self.lights = {lights[0]: Direction.NORTH,
                           lights[1]: Direction.SOUTH}
            self.is_intersection = False
        elif len(lights) == 4:
            self.lights = {lights[i]: key for i, key in enumerate(Direction)}
            self.conflict_map = Intersection.conflicts
            self.is_intersection = True
        else:
            raise ValueError("Перекресток должен иметь либо 2 (противоположных), либо 4 светофора.")
        self.intersection_id = intersection_id

    conflicts = {
        Direction.NORTH: [Direction.EAST, Direction.WEST],
        Direction.SOUTH: [Direction.EAST, Direction.WEST],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH],
        Direction.WEST: [Direction.NORTH, Direction.SOUTH]
    }

    def regulate_intersection(self) -> bool:
        requests = [light.get_traffic_request() for light in self.lights]

        # 2. Находим направление с самым высоким приоритетом (Лидер)
        # Сортируем: кто важнее всех (скорая, потом плотный поток)
        requests.sort(key=lambda x: x['priority'], reverse=True)
        leader_request = requests[0]
        warning = leader_request["reason"] == "INCIDENT"
        leader_direction = ""
        for light, direction in self.lights.items():
            if leader_request["device_id"] == light.device_id:
                leader_direction = direction

        # 3. Расставляем цвета
        for light, direction in self.lights.items():
            conflicts_with_leader = direction in self.conflict_map.get(leader_direction, [])

            if conflicts_with_leader:
                light.set_color(TrafficLightColor.RED)
            else:
                light.set_color(TrafficLightColor.GREEN)

        return warning


class TrafficManager:
    """
    Адаптер для связи Системы Транспорта (TMS) и Управления Трафиком.
    Реализует сценарий 'Зеленая волна' для общественного транспорта.
    """

    def __init__(self, tms: TransportMonitoringSystem) -> None:
        """
        :param tms: Экземпляр TransportMonitoringSystem
        """
        self.tms = tms
        self.intersections: dict[str, Intersection] = {}
        # Маппинг: ID остановки TMS -> ID перекрестка TrafficSystem
        self.stop_intersection_map: dict[str, tuple] = {}

    PublicVehicleType = [VehicleType.BUS, VehicleType.TRAM, VehicleType.TROLLEYBUS]

    def register_district_intersections(self, intersections: list[Intersection]) -> None:
        """Регистрирует перекрёстки района для управления"""
        for intersection in intersections:
            self.intersections[intersection.intersection_id] = intersection

    def get_all_sensors(self) -> list[TrafficFlowSensor]:
        """Возвращает все сенсоры района"""
        sensors = []
        for inter in self.intersections.values():
            for light in inter.lights.keys():
                sensors.append(light.flow_sensor)
        return sensors

    def register_intersection(self, intersection: Intersection) -> None:
        self.intersections[intersection.intersection_id] = intersection

    def link_stop_to_intersection(self, stop_id: str, intersection_id: str, stop_direction: Direction) -> str:
        """
        Связывает физическую остановку с ближайшим перекрестком.
        Когда автобус на остановке, светофор перекрестка знает об этом.
        """
        if stop_id not in self.tms.physical_stops.keys():
            raise TransportException("Остановка не найдена")
        elif intersection_id not in self.intersections:
            raise TransportException("Перекресток не найден")
        if not self.intersections[intersection_id].is_intersection:
            if (intersection_id, Direction.SOUTH) not in self.stop_intersection_map.values():
                stop_direction = Direction.SOUTH
            elif (intersection_id, Direction.NORTH) not in self.stop_intersection_map.values():
                stop_direction = Direction.NORTH
            else:
                raise TransportException("Переход уже имеет остановки со всех сторон.")
        else:
            if (intersection_id, stop_direction) in self.stop_intersection_map.values():
                raise TransportException("Перекресток уже имеет остановку с этой стороны.")
        self.stop_intersection_map[stop_id] = (intersection_id, stop_direction)
        return f"Связана остановка {stop_id} с перекрестком {intersection_id}"

    def prioritize_public_transport(self) -> str | None:
        """
        Основная операция интеграции.
        1. Спрашиваем у TMS, где сейчас транспорт.
        2. Если автобус приближается к связанному перекрестку -> даем приоритет.
        """
        # Проходим по всем маршрутам в TMS
        for route in self.tms.routes.values():
            for vehicle in route.vehicles:
                if vehicle.vehicle_type not in TrafficManager.PublicVehicleType:
                    continue

                current_stop_idx = vehicle.get_last_stop_index
                next_stop_idx = current_stop_idx + 1
                # if next_stop_idx==0: continue

                # Проверяем, есть ли следующая остановка в маршруте
                if next_stop_idx < len(route.stops):
                    next_route_stop = route.stops[next_stop_idx]
                    stop_id = next_route_stop.bus_stop.device_id

                    # Проверяем, связана ли эта остановка с перекрестком
                    if stop_id in self.stop_intersection_map:
                        stop_intersection = self.stop_intersection_map[stop_id]

                        return self._grant_green_wave(stop_intersection, vehicle)
        return None

    def _grant_green_wave(self, stop_intersection: tuple, vehicle) -> str:
        """
        Внутренний метод: запрос к TrafficManager на продление зеленого света.
        """
        # Ищем перекресток в системе трафика (предполагаем, что есть метод поиска)
        intersection = self.intersections[stop_intersection[0]]

        if intersection:
            for light, direction in intersection.lights.items():
                if direction == stop_intersection[1]:
                    light.camera.detect_event(vehicle.vehicle_type, False)

            return f"Общественный транспорт: {vehicle.vehicle_type.value.upper()} №{vehicle.route_id} на переходе {intersection.intersection_id}!"
        else:
            return f"[ОШИБКА] Перекресток {intersection.intersection_id} не найден в системе трафика."