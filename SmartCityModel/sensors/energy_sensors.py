from core import MeasurementType, Domain, Sensor, SmartDevice


class LightLevelSensor(Sensor):
    def __init__(self):
        super().__init__("light_", Domain.INFRASTRUCTURE, MeasurementType.LIGHT)
        self._ambient_light_level = 50

    def set_light_level(self, level: int):
        self._ambient_light_level = level

    def get_status(self):
        return self._ambient_light_level


class MotionSensor(Sensor):
    def __init__(self):
        super().__init__("motion_", Domain.INFRASTRUCTURE, MeasurementType.MOTION)
        self.movement = False
        self._callback = None  # Храним функцию-реакцию

    def set_callback(self, func):
        """Устанавливаем функцию, которая сработает при движении"""
        self._callback = func

    def detect_motion(self, is_moving: bool):
        """Симуляция получения сигнала от сенсора"""
        self.movement = is_moving
        if self.movement and self._callback:
            self._callback()  # Вызываем фонарь сразу же


class WaterMeter(SmartDevice):
    def __init__(self, device_id: str):
        super().__init__(device_id, Domain.HOUSING)
        self._water_volume = 5000

    def set_water_volume(self, volume: int):
        self._water_volume = volume

    def get_water_volume(self):
        return self._water_volume


class ElectricityMeter(SmartDevice):
    def __init__(self, device_id: str):
        super().__init__(device_id, Domain.HOUSING)
        self._energy = 5000

    def set_energy(self, energy: int):
        self._energy = energy

    def get_energy(self):
        return self._energy
