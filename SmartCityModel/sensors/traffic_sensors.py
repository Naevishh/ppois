from .base_sensor import Sensor
from core import Domain, MeasurementType, VehicleType, SensorValueError


class AITrafficCamera(Sensor):
    def __init__(self):
        super().__init__("aicam_", Domain.TRANSPORTATION, MeasurementType.VIDEO_ANALYTICS)
        self._last_event = {"vehicle_type": VehicleType.BICYCLE.value, "incident": None}

    def detect_event(self, vehicle_type: VehicleType, incident: bool):
        self._last_event = {"vehicle_type": vehicle_type, "incident": incident}

    def get_status(self) -> dict:
        return self._last_event


class TrafficFlowSensor(Sensor):
    def __init__(self):
        super().__init__("trfl_", Domain.TRANSPORTATION, MeasurementType.TRAFFIC_INTENSITY)
        self._vehicles_per_minute = 20

    def update_intensity(self, count: int):
        if count < 0:
            raise SensorValueError("Количество транспортных средств не может быть отрицательным.")
        elif count > 200:
            raise SensorValueError("Количество транспортных средств слишком высокое.")
        self._vehicles_per_minute = count

    def get_status(self) -> int:
        return self._vehicles_per_minute


class PedestrianCrossingSensor(Sensor):
    def __init__(self):
        super().__init__("pdstr_", Domain.TRANSPORTATION, MeasurementType.VEHICLE_PRESENCE)
        self._pedestrians_waiting = 5

    def detect_pedestrians(self, count: int):
        if count < 0:
            raise SensorValueError("Количество пешеходов не может быть отрицательным.")
        elif count > 50:
            raise SensorValueError("Количество пешеходов слишком высокое.")
        self._pedestrians_waiting = count

    def get_status(self) -> int:
        return self._pedestrians_waiting