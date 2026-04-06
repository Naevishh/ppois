from .base_sensor import Sensor
from ..core import MeasurementType, Domain, SmartDevice, SensorValueError


class LightLevelSensor(Sensor):
    def __init__(self) -> None:
        super().__init__("light_sensor_", Domain.INFRASTRUCTURE, MeasurementType.LIGHT)
        self._ambient_light_level = 50

    def set_value(self, level: int) -> None:
        if level < 0:
            raise SensorValueError("Уровень освещения не может быть отрицательным.")
        elif level > 100:
            raise SensorValueError("Уровень освещения слишком высокий.")
        self._ambient_light_level = level

    def get_status(self) -> int:
        return self._ambient_light_level


class MotionSensor(Sensor):
    def __init__(self) -> None:
        super().__init__("motion_", Domain.INFRASTRUCTURE, MeasurementType.MOTION)
        self.movement = False
        self._callback = None

    def set_callback(self, func) -> None:
        """Устанавливаем функцию, которая сработает при движении"""
        self._callback = func

    def detect_motion(self, is_moving: bool) -> None:
        """Симуляция получения сигнала от сенсора"""
        self.movement = is_moving
        if self.movement and self._callback:
            self._callback()


class WaterMeter(SmartDevice):
    def __init__(self) -> None:
        super().__init__("watermtr_", Domain.HOUSING)
        self._water_volume = 5000

    def set_value(self, volume: int) -> None:
        if volume < 0:
            raise SensorValueError("Объем воды не может быть отрицательным.")
        elif volume > 1000000:
            raise SensorValueError("Объем воды слишком большой.")
        self._water_volume = volume

    def get_water_volume(self) -> int:
        return self._water_volume


class ElectricityMeter(SmartDevice):
    def __init__(self) -> None:
        super().__init__("electrmtr_", Domain.HOUSING)
        self._energy = 5000

    def set_value(self, energy: float) -> None:
        if energy < 0:
            raise SensorValueError("Энергия не может быть отрицательной.")
        elif energy > 1000000:
            raise SensorValueError("Значение энергии слишком высокое.")
        self._energy = energy

    def get_energy(self) -> int:
        return self._energy
