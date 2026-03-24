from ..sensors import LightLevelSensor, MotionSensor, WaterMeter, ElectricityMeter, TemperatureSensor
from .lighting import SmartLightningSystem
from ..core import Domain, SmartDevice


class SmartThermostat(SmartDevice):
    """Умный термостат для экономии на отоплении/кондиционировании"""

    def __init__(self, temp_sensor: TemperatureSensor) -> None:
        super().__init__("therm_", Domain.HOUSING)
        self.temp_sensor = temp_sensor
        self._is_heating = False

    def optimize_climate(self) -> None:
        """Энергосберегающая логика"""
        # Если никого нет, снижаем активность отопления/кондиционирования
        if self.temp_sensor.get_temperature() > 22:
            self._is_heating = False
        else:
            self._is_heating = True

    def get_energy_consumption(self) -> int:
        # Грубая оценка: если нагрев включен, потребление высокое
        return 500 if self._is_heating else 10


class SmartHome:
    def __init__(self, address: tuple, water_meter: WaterMeter,
                 electricity_meter: ElectricityMeter,
                 thermostat: SmartThermostat,
                 lightning_system: SmartLightningSystem) -> None:
        self.address = address
        self.water_meter = water_meter
        self.electricity_meter = electricity_meter
        self.thermostat = thermostat
        self.lightning_system = lightning_system

    def get_energy_consumption(self) -> float:
        current_consumption = self.thermostat.get_energy_consumption() + self.lightning_system.get_energy_consumption()
        self.electricity_meter.set_value(current_consumption)
        return current_consumption

    def get_metrics(self) -> dict:
        return {
            "water": self.water_meter.get_water_volume(),
            "electricity": self.electricity_meter.get_energy()
        }


class SmartLight(SmartDevice):
    def __init__(self, light_level_sensor: LightLevelSensor, motion_sensor: MotionSensor) -> None:
        super().__init__("smrtlight_", Domain.INFRASTRUCTURE)
        self.light_level_sensor = light_level_sensor
        self.motion_sensor = motion_sensor
        self._light_level = 50
        self._is_on = False

        self.motion_sensor.set_callback(self.turn_on)

    def turn_on(self) -> None:
        """Метод, который вызовет сенсор при движении"""
        self.set_level()

    def set_level(self) -> None:
        status = self.light_level_sensor.get_status()
        if status >= 70:
            self._is_on = False
        else:
            self._is_on = True
            self._light_level = 100 - status

    def get_energy_consumption_estimate(self) -> float:
        return self._light_level * 0.95