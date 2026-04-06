from datetime import datetime

from ..core import SmartDevice, Domain, VehicleType, TransportException


class BusStop(SmartDevice):
    """Остановка общественного транспорта"""

    def __init__(self, name: str) -> None:
        super().__init__("stop_", Domain.TRANSPORTATION)
        self.name = name
        self._waiting_passengers = 0
        self._display_message = ""

    def update_passengers(self, count: int) -> None:
        if count < 0:
            raise TransportException("Количество пассажиров не может быть отрицательным.")
        self._waiting_passengers = count

    def set_display(self, message: str) -> None:
        self._display_message = message

    def get_status(self) -> dict:
        return {
            "stop_id": self.device_id,
            "name": self.name,
            "display": self._display_message,
            "passengers": self._waiting_passengers
        }


class RouteStop:
    """Связка: Остановка + её порядковый номер на конкретном маршруте"""

    def __init__(self, bus_stop: BusStop, index: int) -> None:
        self.bus_stop = bus_stop
        self.index = index


class PublicTransportVehicle(SmartDevice):
    """Транспортное средство общественного транспорта"""

    def __init__(self, vehicle_type: VehicleType, route_id: str) -> None:
        super().__init__(f"{vehicle_type.value}_", Domain.TRANSPORTATION)
        self.vehicle_type = vehicle_type
        self.route_id = route_id

        self._last_passed_stop_index = -1
        self._last_update = datetime.now()
        self._passenger_count = 0

    def report_stop_passed(self, stop_index: int) -> str | None:
        """
        Транспорт сообщает: 'Я проехал остановку с индексом X'.
        Это заменяет отправку GPS координат.
        """
        if stop_index > self._last_passed_stop_index:
            self._last_passed_stop_index = stop_index
            self._last_update = datetime.now()
            return f"[{self.device_id}] Пройдена остановка индекса  
        else:
            return None

    def update_passengers(self, count: int) -> None:
        if count < 0:
            raise TransportException("Количество пассажиров не может быть отрицательным.")
        elif count > 60:
            raise TransportException("Количество пассажиров слишком большое.")
        self._passenger_count = count

    @property
    def get_last_stop_index(self) -> int:
        return self._last_passed_stop_index

    def get_status(self) -> dict:
        return {
            "vehicle_id": self.device_id,
            "type": self.vehicle_type.value,
            "route_id": self.route_id,
            "last_passed_stop_index": self._last_passed_stop_index,
            "passengers": self._passenger_count
        }


class TransportRoute:
    """Маршрут общественного транспорта"""

    def __init__(self, route_id: str, stops: list[RouteStop], avg_time_between_stops: int = 3) -> None:
        self.route_id = route_id
        self.stops = stops
        self.vehicles: list[PublicTransportVehicle] = []

        self.avg_time_between_stops = avg_time_between_stops

    def add_vehicle(self, vehicle: PublicTransportVehicle) -> None:
        if vehicle.route_id == self.route_id:
            self.vehicles.append(vehicle)

    def get_status(self) -> dict:
        return {
            "route_id": self.route_id,
            "total_stops": len(self.stops),
            "active_vehicles": len(self.vehicles)
        }
