"""
Юнит-тесты для модуля energy SmartCityModel
Покрытие: devices.py, generation.py, grid.py, lighting.py
"""

from unittest.mock import Mock

import pytest
from SmartCityModel.core.exceptions import SensorValueError
from SmartCityModel.energy.devices import SmartThermostat, SmartLight, SmartHome
from SmartCityModel.energy.generation import SolarPanel, WindTurbine, BatteryStorage
from SmartCityModel.energy.grid import CityEnergyGrid
from SmartCityModel.energy.lighting import SmartLightningSystem
from SmartCityModel.sensors.energy_sensors import WaterMeter, ElectricityMeter, LightLevelSensor, MotionSensor
from SmartCityModel.sensors.environment_sensors import TemperatureSensor


class MockTemperatureSensor:
    """Моковый температурный сенсор"""

    def __init__(self, temperature: int = 20):
        self._temperature = temperature

    def get_temperature(self) -> int:
        return self._temperature

    def set_value(self, temperature: int) -> None:
        self._temperature = temperature


class MockLightLevelSensor:
    """Моковый сенсор уровня освещения"""

    def __init__(self, level: int = 50):
        self._level = level

    def get_status(self) -> int:
        return self._level

    def set_value(self, level: int) -> None:
        self._level = level


class MockMotionSensor:
    """Моковый сенсор движения"""

    def __init__(self):
        self.movement = False
        self._callback = None

    def set_callback(self, func) -> None:
        self._callback = func

    def detect_motion(self, is_moving: bool) -> None:
        self.movement = is_moving
        if self.movement and self._callback:
            self._callback()


class MockWaterMeter:
    """Моковый счётчик воды"""

    def __init__(self, volume: int = 5000):
        self._volume = volume

    def get_water_volume(self) -> int:
        return self._volume

    def set_value(self, volume: int) -> None:
        self._volume = volume


class MockElectricityMeter:
    """Моковый счётчик электроэнергии"""

    def __init__(self, energy: float = 5000):
        self._energy = energy

    def get_energy(self) -> float:
        return self._energy

    def set_value(self, energy: float) -> None:
        self._energy = energy


class TestSmartThermostat:
    """Тесты класса SmartThermostat"""

    def test_init_creates_thermostat(self):
        """Проверка инициализации термостата"""
        sensor = MockTemperatureSensor(20)
        thermostat = SmartThermostat(sensor)

        assert thermostat.temp_sensor == sensor
        assert thermostat._is_heating is False
        assert thermostat.device_id.startswith("therm_")

    def test_optimize_climate_heating_on_when_cold(self):
        """Отопление включается при температуре ниже 22°C"""
        sensor = MockTemperatureSensor(20)
        thermostat = SmartThermostat(sensor)

        thermostat.optimize_climate()

        assert thermostat._is_heating is True

    def test_optimize_climate_heating_off_when_warm(self):
        """Отопление выключается при температуре выше 22°C"""
        sensor = MockTemperatureSensor(25)
        thermostat = SmartThermostat(sensor)

        thermostat.optimize_climate()

        assert thermostat._is_heating is False

    def test_optimize_climate_boundary_at_22(self):
        """Проверка граничного значения 22°C"""
        sensor = MockTemperatureSensor(22)
        thermostat = SmartThermostat(sensor)

        thermostat.optimize_climate()

        assert thermostat._is_heating is True

    def test_get_energy_consumption_high_when_heating(self):
        """Высокое потребление при включённом отоплении"""
        sensor = MockTemperatureSensor(20)
        thermostat = SmartThermostat(sensor)
        thermostat.optimize_climate()

        consumption = thermostat.get_energy_consumption()

        assert consumption == 500

    def test_get_energy_consumption_low_when_not_heating(self):
        """Низкое потребление при выключенном отоплении"""
        sensor = MockTemperatureSensor(25)
        thermostat = SmartThermostat(sensor)
        thermostat.optimize_climate()

        consumption = thermostat.get_energy_consumption()

        assert consumption == 10


class TestSmartLight:
    """Тесты класса SmartLight"""

    def test_init_creates_smart_light(self):
        """Проверка инициализации умного света"""
        light_sensor = MockLightLevelSensor(50)
        motion_sensor = MockMotionSensor()

        light = SmartLight(light_sensor, motion_sensor)

        assert light._light_level == 50
        assert light._is_on is False
        assert motion_sensor._callback is not None
        assert light.device_id.startswith("smrtlight_")

    def test_turn_on_sets_light_level(self):
        """Метод turn_on устанавливает уровень света"""
        light_sensor = MockLightLevelSensor(30)
        motion_sensor = MockMotionSensor()
        light = SmartLight(light_sensor, motion_sensor)

        light.turn_on()

        assert light._is_on is True
        assert light._light_level == 70

    def test_set_level_turns_off_when_bright(self):
        """Свет выключается при высоком уровне освещения (>=70)"""
        light_sensor = MockLightLevelSensor(80)
        motion_sensor = MockMotionSensor()
        light = SmartLight(light_sensor, motion_sensor)

        light.set_level()

        assert light._is_on is False

    def test_set_level_turns_on_when_dark(self):
        """Свет включается при низком уровне освещения (<70)"""
        light_sensor = MockLightLevelSensor(40)
        motion_sensor = MockMotionSensor()
        light = SmartLight(light_sensor, motion_sensor)

        light.set_level()

        assert light._is_on is True
        assert light._light_level == 60

    def test_get_energy_consumption_calculation(self):
        """Расчёт потребления энергии"""
        light_sensor = MockLightLevelSensor(50)
        motion_sensor = MockMotionSensor()
        light = SmartLight(light_sensor, motion_sensor)
        light.set_level()

        consumption = light.get_energy_consumption()

        assert consumption == 50 * 0.95

    def test_motion_sensor_callback_triggers_turn_on(self):
        """Сенсор движения вызывает turn_on при обнаружении"""
        light_sensor = MockLightLevelSensor(30)
        motion_sensor = MockMotionSensor()
        light = SmartLight(light_sensor, motion_sensor)

        motion_sensor.detect_motion(True)

        assert light._is_on is True


class TestSmartHome:
    """Тесты класса SmartHome"""

    def test_init_creates_smart_home(self):
        """Проверка инициализации умного дома"""
        water_meter = MockWaterMeter(5000)
        electricity_meter = MockElectricityMeter(5000)
        thermostat = Mock()
        thermostat.get_energy_consumption.return_value = 100
        lightning_system = Mock()
        lightning_system.get_energy_consumption.return_value = 50

        home = SmartHome(
            address=("Moscow", "Lenina str", 1),
            water_meter=water_meter,
            electricity_meter=electricity_meter,
            thermostat=thermostat,
            lightning_system=lightning_system
        )

        assert home.address == ("Moscow", "Lenina str", 1)
        assert home.water_meter == water_meter
        assert home.electricity_meter == electricity_meter

    def test_get_energy_consumption_summation(self):
        """Потребление энергии - сумма термостата и освещения"""
        water_meter = MockWaterMeter()
        electricity_meter = Mock()
        thermostat = Mock()
        thermostat.get_energy_consumption.return_value = 300
        lightning_system = Mock()
        lightning_system.get_energy_consumption.return_value = 150

        home = SmartHome(
            address=("Test",),
            water_meter=water_meter,
            electricity_meter=electricity_meter,
            thermostat=thermostat,
            lightning_system=lightning_system
        )

        consumption = home.get_energy_consumption()

        assert consumption == 450
        electricity_meter.set_value.assert_called_once_with(450)

    def test_get_metrics_returns_water_and_electricity(self):
        """Метрики возвращают воду и электричество"""
        water_meter = MockWaterMeter(8000)
        electricity_meter = MockElectricityMeter(6000)
        thermostat = Mock()
        thermostat.get_energy_consumption.return_value = 100
        lightning_system = Mock()
        lightning_system.get_energy_consumption.return_value = 50

        home = SmartHome(
            address=("Test",),
            water_meter=water_meter,
            electricity_meter=electricity_meter,
            thermostat=thermostat,
            lightning_system=lightning_system
        )

        metrics = home.get_metrics()

        assert metrics["water"] == 8000
        assert metrics["electricity"] == 6000


class TestSolarPanel:
    """Тесты класса SolarPanel"""

    def test_init_creates_solar_panel(self):
        """Проверка инициализации солнечной панели"""
        sensor = MockLightLevelSensor(50)
        panel = SolarPanel(sensor)

        assert panel.light_level_sensor == sensor

    def test_produce_electricity_proportional_to_light(self):
        """Выработка пропорциональна уровню освещения"""
        sensor = MockLightLevelSensor(100)
        panel = SolarPanel(sensor)

        production = panel.produce_electricity()

        assert production == 50.0

    def test_produce_electricity_zero_when_dark(self):
        """Нулевая выработка в темноте"""
        sensor = MockLightLevelSensor(0)
        panel = SolarPanel(sensor)

        production = panel.produce_electricity()

        assert production == 0.0

    def test_produce_electricity_partial_light(self):
        """Частичная выработка при неполном освещении"""
        sensor = MockLightLevelSensor(60)
        panel = SolarPanel(sensor)

        production = panel.produce_electricity()

        assert production == 30.0


class TestWindTurbine:
    """Тесты класса WindTurbine"""

    def test_init_creates_wind_turbine(self):
        """Проверка инициализации ветряной турбины"""
        turbine = WindTurbine()

        assert turbine._wind_speed == 0

    def test_set_wind_speed_valid(self):
        """Установка корректной скорости ветра"""
        turbine = WindTurbine()

        turbine.set_wind_speed(10)

        assert turbine._wind_speed == 10

    def test_set_wind_speed_negative_raises_error(self):
        """Отрицательная скорость вызывает исключение"""
        turbine = WindTurbine()

        with pytest.raises(SensorValueError):
            turbine.set_wind_speed(-5)

    def test_set_wind_speed_too_high_raises_error(self):
        """Слишком высокая скорость вызывает исключение"""
        turbine = WindTurbine()

        with pytest.raises(SensorValueError):
            turbine.set_wind_speed(30)

    def test_produce_electricity_no_wind(self):
        """Нет выработки при слабом ветре (<3 м/с)"""
        turbine = WindTurbine()
        turbine.set_wind_speed(2)

        production = turbine.produce_electricity()

        assert production == 0

    def test_produce_electricity_with_wind(self):
        """Выработка начинается с 3 м/с"""
        turbine = WindTurbine()
        turbine.set_wind_speed(10)

        production = turbine.produce_electricity()

        assert production == 70

    def test_produce_electricity_boundary_at_3(self):
        """Граничное значение 3 м/с"""
        turbine = WindTurbine()
        turbine.set_wind_speed(3)

        production = turbine.produce_electricity()

        assert production == 0

    def test_set_wind_speed_boundary_values(self):
        """Граничные значения скорости ветра"""
        turbine = WindTurbine()

        turbine.set_wind_speed(0)
        assert turbine._wind_speed == 0

        turbine.set_wind_speed(25)
        assert turbine._wind_speed == 25


class TestBatteryStorage:
    """Тесты класса BatteryStorage"""

    def test_init_creates_battery(self):
        """Проверка инициализации батареи"""
        battery = BatteryStorage(capacity=1000)

        assert battery.capacity == 1000
        assert battery.current_charge == 0
        assert battery._is_charging is False
        assert battery.device_id.startswith("battery_")

    def test_store_energy_fits_in_capacity(self):
        """Зарядка в пределах ёмкости"""
        battery = BatteryStorage(capacity=1000)

        stored = battery.store_energy(500)

        assert stored == 500
        assert battery.current_charge == 500

    def test_store_energy_exceeds_capacity(self):
        """Зарядка превышает ёмкость"""
        battery = BatteryStorage(capacity=1000)
        battery.store_energy(800)

        stored = battery.store_energy(500)

        assert stored == 200
        assert battery.current_charge == 1000

    def test_store_energy_full_battery(self):
        """Зарядка полностью заряженной батареи"""
        battery = BatteryStorage(capacity=1000)
        battery.current_charge = 1000

        stored = battery.store_energy(100)

        assert stored == 0
        assert battery.current_charge == 1000

    def test_release_energy_available(self):
        """Разрядка при достаточном заряде"""
        battery = BatteryStorage(capacity=1000)
        battery.current_charge = 500

        released = battery.release_energy(300)

        assert released == 300
        assert battery.current_charge == 200

    def test_release_energy_insufficient(self):
        """Разрядка при недостаточном заряде"""
        battery = BatteryStorage(capacity=1000)
        battery.current_charge = 100

        released = battery.release_energy(300)

        assert released == 0
        assert battery.current_charge == 100

    def test_release_energy_empty_battery(self):
        """Разрядка пустой батареи"""
        battery = BatteryStorage(capacity=1000)

        released = battery.release_energy(100)

        assert released == 0

    def test_get_charge_percentage(self):
        """Процент заряда батареи"""
        battery = BatteryStorage(capacity=1000)
        battery.current_charge = 750

        percentage = battery.get_charge_percentage()

        assert percentage == 75.0

    def test_get_charge_percentage_full(self):
        """Процент заряда полной батареи"""
        battery = BatteryStorage(capacity=1000)
        battery.current_charge = 1000

        percentage = battery.get_charge_percentage()

        assert percentage == 100.0

    def test_get_charge_percentage_empty(self):
        """Процент заряда пустой батареи"""
        battery = BatteryStorage(capacity=1000)

        percentage = battery.get_charge_percentage()

        assert percentage == 0.0


class TestSmartLightningSystem:
    """Тесты класса SmartLightningSystem"""

    def test_init_creates_lightning_system(self):
        """Проверка инициализации системы освещения"""
        lights = [Mock(), Mock()]
        system = SmartLightningSystem(lights)

        assert system.smart_lights == lights

    def test_optimize_lightning_calls_set_level(self):
        """Оптимизация вызывает set_level для всех светильников"""
        light1 = Mock()
        light2 = Mock()
        system = SmartLightningSystem([light1, light2])

        system.optimize_lightning()

        light1.set_level.assert_called_once()
        light2.set_level.assert_called_once()

    def test_get_energy_consumption_summation(self):
        """Потребление - сумма всех светильников"""
        light1 = Mock()
        light1.get_energy_consumption.return_value = 50.0
        light2 = Mock()
        light2.get_energy_consumption.return_value = 30.0

        system = SmartLightningSystem([light1, light2])

        consumption = system.get_energy_consumption()

        assert consumption == 80.0

    def test_get_energy_consumption_empty_system(self):
        """Потребление пустой системы"""
        system = SmartLightningSystem([])

        consumption = system.get_energy_consumption()

        assert consumption == 0


class TestCityEnergyGrid:
    """Тесты класса CityEnergyGrid"""

    def test_init_creates_energy_grid(self):
        """Проверка инициализации энергосети"""
        generators = [Mock()]
        storages = [Mock()]
        consumers = [Mock()]

        grid = CityEnergyGrid(generators, storages, consumers)

        assert grid.generators == generators
        assert grid.storages == storages
        assert grid.consumers == consumers

    def test_balance_energy_surplus(self):
        """Балансировка с излишками энергии"""
        generator = Mock()
        generator.produce_electricity.return_value = 1000

        battery = Mock()
        battery.store_energy.return_value = 500

        consumer = Mock()
        consumer.get_energy_consumption.return_value = 500

        grid = CityEnergyGrid(
            generators=[generator],
            storages=[battery],
            consumers=[consumer]
        )

        result = grid.balance_energy()

        assert result["production"] == 1000
        assert result["consumption"] == 500
        assert result["result"] == "Излишки распределены."
        battery.store_energy.assert_called_once()

    def test_balance_energy_deficit(self):
        """Балансировка с дефицитом энергии"""
        generator = Mock()
        generator.produce_electricity.return_value = 300

        battery = Mock()
        battery.release_energy.return_value = 200

        consumer = Mock()
        consumer.get_energy_consumption.return_value = 700

        grid = CityEnergyGrid(
            generators=[generator],
            storages=[battery],
            consumers=[consumer]
        )

        result = grid.balance_energy()

        assert result["production"] == 300
        assert result["consumption"] == 700
        assert "Дефицит" in result["result"]
        battery.release_energy.assert_called_once()

    def test_balance_energy_balanced(self):
        """Балансировка без излишков и дефицита"""
        generator = Mock()
        generator.produce_electricity.return_value = 500

        consumer = Mock()
        consumer.get_energy_consumption.return_value = 500

        grid = CityEnergyGrid(
            generators=[generator],
            storages=[],
            consumers=[consumer]
        )

        result = grid.balance_energy()

        assert result["production"] == 500
        assert result["consumption"] == 500
        assert result["surplus"] == 0
        assert result["result"] == "Производство покрыло потребление."

    def test_optimize_all_calls_lightning_optimization(self):
        lightning_system = Mock(spec=SmartLightningSystem)
        lightning_system.get_energy_consumption.return_value = 0
        consumer = Mock()
        consumer.get_energy_consumption.return_value = 0

        grid = CityEnergyGrid(
            generators=[],
            storages=[],
            consumers=[lightning_system, consumer]
        )

        grid.optimize_all()

        lightning_system.optimize_lightning.assert_called_once()
        consumer.optimize_lightning.assert_not_called()

    def test_balance_energy_multiple_storages(self):
        """Балансировка с несколькими накопителями"""
        generator = Mock()
        generator.produce_electricity.return_value = 1500

        battery1 = Mock()
        battery1.store_energy.side_effect = lambda x: min(x, 500)

        battery2 = Mock()
        battery2.store_energy.side_effect = lambda x: min(x, 500)

        consumer = Mock()
        consumer.get_energy_consumption.return_value = 500

        grid = CityEnergyGrid(
            generators=[generator],
            storages=[battery1, battery2],
            consumers=[consumer]
        )

        result = grid.balance_energy()

        assert result["production"] == 1500
        assert result["consumption"] == 500
        assert battery1.store_energy.called
        assert battery2.store_energy.called


class TestEnergyModuleIntegration:
    """Интеграционные тесты модуля energy"""

    def test_full_energy_cycle(self):
        """Полный цикл работы энергосистемы"""

        light_sensor = MockLightLevelSensor(80)
        temp_sensor = MockTemperatureSensor(20)

        solar_panel = SolarPanel(light_sensor)
        wind_turbine = WindTurbine()
        wind_turbine.set_wind_speed(10)

        battery = BatteryStorage(capacity=2000)

        thermostat = SmartThermostat(temp_sensor)
        thermostat.optimize_climate()

        light_sensor_for_smart = MockLightLevelSensor(40)
        motion_sensor = MockMotionSensor()
        smart_light = SmartLight(light_sensor_for_smart, motion_sensor)
        smart_light.set_level()

        lightning_system = SmartLightningSystem([smart_light])

        grid = CityEnergyGrid(
            generators=[solar_panel, wind_turbine],
            storages=[battery],
            consumers=[thermostat, lightning_system]
        )

        result = grid.balance_energy()

        assert result["production"] > 0
        assert result["consumption"] > 0
        assert "production" in result
        assert "consumption" in result
        assert "surplus" in result

    def test_smart_home_with_real_components(self):
        water_meter = WaterMeter()
        electricity_meter = ElectricityMeter()
        temp_sensor = TemperatureSensor()
        thermostat = SmartThermostat(temp_sensor)

        light_sensor = LightLevelSensor()
        motion_sensor = MotionSensor()
        smart_light = SmartLight(light_sensor, motion_sensor)
        lightning_system = SmartLightningSystem([smart_light])

        home = SmartHome(
            address=("Test City", "Test Street", 1),
            water_meter=water_meter,
            electricity_meter=electricity_meter,
            thermostat=thermostat,
            lightning_system=lightning_system
        )

        consumption = home.get_energy_consumption()
        metrics = home.get_metrics()

        assert consumption >= 0
        assert "water" in metrics
        assert "electricity" in metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
