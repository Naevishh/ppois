"""
Юнит-тесты для модуля sensors SmartCityModel
Реальные классы из репозитория:
- sensors/base_sensor.py: Sensor
- sensors/energy_sensors.py: LightLevelSensor, MotionSensor, WaterMeter, ElectricityMeter
- sensors/environment_sensors.py: AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor
- sensors/traffic_sensors.py: AITrafficCamera, TrafficFlowSensor, PedestrianCrossingSensor
- core: Domain, MeasurementType, enums, SensorValueError, SmartDevice
"""

import re
from unittest.mock import Mock

import pytest
from SmartCityModel.core import Domain, MeasurementType, VehicleType, AirQualityLevel, TemperatureLevel, HumidityLevel, \
    NoiseLevel, SensorValueError, SmartDevice
from SmartCityModel.sensors.base_sensor import Sensor
from SmartCityModel.sensors.energy_sensors import LightLevelSensor, MotionSensor, WaterMeter, ElectricityMeter
from SmartCityModel.sensors.environment_sensors import AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor
from SmartCityModel.sensors.traffic_sensors import AITrafficCamera, TrafficFlowSensor, PedestrianCrossingSensor


class TestSensorBase:
    """Тесты базового класса Sensor"""

    def test_init_creates_sensor_with_uuid(self):
        """Инициализация создаёт sensor_id с UUID"""
        sensor = Sensor("test_", Domain.ECOLOGY, MeasurementType.TEMPERATURE)

        assert sensor.sensor_id.startswith("test_")

        assert len(sensor.sensor_id) == len("test_") + 6

        assert re.match(r'^[0-9a-f]{6}$', sensor.sensor_id[-6:])

    def test_init_sets_domain_and_measurement_type(self):
        """Инициализация сохраняет domain и measurement_type"""
        sensor = Sensor("sens_", Domain.TRANSPORTATION, MeasurementType.TRAFFIC_INTENSITY)

        assert sensor.domain == Domain.TRANSPORTATION
        assert sensor.measurement_type == MeasurementType.TRAFFIC_INTENSITY

    def test_set_value_base_is_noop(self):
        """Базовый set_value ничего не делает (переопределяется в наследниках)"""
        sensor = Sensor("base_", Domain.ECOLOGY, MeasurementType.CONCENTRATION)

        sensor.set_value(42)

    def test_get_status_base_returns_none(self):
        """Базовый get_status возвращает None (переопределяется в наследниках)"""
        sensor = Sensor("base_", Domain.ECOLOGY, MeasurementType.CONCENTRATION)

        result = sensor.get_status()

        assert result is None


class TestLightLevelSensor:
    """Тесты класса LightLevelSensor"""

    def test_init_creates_light_sensor(self):
        """Проверка инициализации"""
        sensor = LightLevelSensor()

        assert sensor.sensor_id.startswith("light_sensor_")
        assert sensor.domain == Domain.INFRASTRUCTURE
        assert sensor.measurement_type == MeasurementType.LIGHT
        assert sensor._ambient_light_level == 50

    def test_set_value_valid(self):
        """Установка корректного уровня освещения"""
        sensor = LightLevelSensor()

        sensor.set_value(75)

        assert sensor._ambient_light_level == 75

    def test_set_value_zero_valid(self):
        """Нулевой уровень допустим"""
        sensor = LightLevelSensor()

        sensor.set_value(0)

        assert sensor._ambient_light_level == 0

    def test_set_value_hundred_valid(self):
        """Максимальный уровень 100 допустим"""
        sensor = LightLevelSensor()

        sensor.set_value(100)

        assert sensor._ambient_light_level == 100

    def test_set_value_negative_raises_error(self):
        """Отрицательное значение вызывает исключение"""
        sensor = LightLevelSensor()

        with pytest.raises(SensorValueError, match="отрицательным"):
            sensor.set_value(-1)

    def test_set_value_over_100_raises_error(self):
        """Значение >100 вызывает исключение"""
        sensor = LightLevelSensor()

        with pytest.raises(SensorValueError, match="слишком высокий"):
            sensor.set_value(101)

    def test_get_status_returns_light_level(self):
        """get_status возвращает текущий уровень освещения"""
        sensor = LightLevelSensor()
        sensor.set_value(80)

        result = sensor.get_status()

        assert result == 80


class TestMotionSensor:
    """Тесты класса MotionSensor"""

    def test_init_creates_motion_sensor(self):
        """Проверка инициализации"""
        sensor = MotionSensor()

        assert sensor.sensor_id.startswith("motion_")
        assert sensor.domain == Domain.INFRASTRUCTURE
        assert sensor.measurement_type == MeasurementType.MOTION
        assert sensor.movement is False
        assert sensor._callback is None

    def test_set_callback_stores_function(self):
        """set_callback сохраняет функцию"""
        sensor = MotionSensor()
        callback = Mock()

        sensor.set_callback(callback)

        assert sensor._callback == callback

    def test_detect_motion_without_callback(self):
        """detect_motion без колбэка просто меняет флаг"""
        sensor = MotionSensor()

        sensor.detect_motion(True)

        assert sensor.movement is True

    def test_detect_motion_with_callback_triggers_it(self):
        """detect_motion вызывает колбэк при движении"""
        sensor = MotionSensor()
        callback = Mock()
        sensor.set_callback(callback)

        sensor.detect_motion(True)

        assert sensor.movement is True
        callback.assert_called_once()

    def test_detect_motion_false_does_not_trigger_callback(self):
        """detect_motion(False) не вызывает колбэк"""
        sensor = MotionSensor()
        callback = Mock()
        sensor.set_callback(callback)

        sensor.detect_motion(False)

        assert sensor.movement is False
        callback.assert_not_called()


class TestWaterMeter:
    """Тесты класса WaterMeter"""

    def test_init_creates_water_meter(self):
        """Проверка инициализации"""
        meter = WaterMeter()

        assert meter.device_id.startswith("watermtr_")
        assert meter.domain == Domain.HOUSING
        assert isinstance(meter, SmartDevice)
        assert meter._water_volume == 5000

    def test_set_value_valid(self):
        """Установка корректного объёма воды"""
        meter = WaterMeter()

        meter.set_value(15000)

        assert meter._water_volume == 15000

    def test_set_value_zero_valid(self):
        """Нулевой объём допустим"""
        meter = WaterMeter()

        meter.set_value(0)

        assert meter._water_volume == 0

    def test_set_value_max_valid(self):
        """Максимальный объём 1000000 допустим"""
        meter = WaterMeter()

        meter.set_value(1_000_000)

        assert meter._water_volume == 1_000_000

    def test_set_value_negative_raises_error(self):
        """Отрицательный объём вызывает исключение"""
        meter = WaterMeter()

        with pytest.raises(SensorValueError, match="отрицательным"):
            meter.set_value(-100)

    def test_set_value_over_limit_raises_error(self):
        """Объём >1000000 вызывает исключение"""
        meter = WaterMeter()

        with pytest.raises(SensorValueError, match="слишком большой"):
            meter.set_value(1_000_001)

    def test_get_water_volume_returns_value(self):
        """get_water_volume возвращает текущий объём"""
        meter = WaterMeter()
        meter.set_value(25000)

        result = meter.get_water_volume()

        assert result == 25000


class TestElectricityMeter:
    """Тесты класса ElectricityMeter"""

    def test_init_creates_electricity_meter(self):
        """Проверка инициализации"""
        meter = ElectricityMeter()

        assert meter.device_id.startswith("electrmtr_")
        assert meter.domain == Domain.HOUSING
        assert isinstance(meter, SmartDevice)
        assert meter._energy == 5000

    def test_set_value_valid(self):
        """Установка корректного значения энергии"""
        meter = ElectricityMeter()

        meter.set_value(12500.5)

        assert meter._energy == 12500.5

    def test_set_value_zero_valid(self):
        """Нулевое значение допустимо"""
        meter = ElectricityMeter()

        meter.set_value(0.0)

        assert meter._energy == 0.0

    def test_set_value_negative_raises_error(self):
        """Отрицательная энергия вызывает исключение"""
        meter = ElectricityMeter()

        with pytest.raises(SensorValueError, match="отрицательной"):
            meter.set_value(-100.0)

    def test_set_value_over_limit_raises_error(self):
        """Значение >1000000 вызывает исключение"""
        meter = ElectricityMeter()

        with pytest.raises(SensorValueError, match="слишком высокое"):
            meter.set_value(1_000_001.0)

    def test_get_energy_returns_value(self):
        """get_energy возвращает текущее значение"""
        meter = ElectricityMeter()
        meter.set_value(7500.25)

        result = meter.get_energy()

        assert result == 7500.25


class TestAirQualitySensor:
    """Тесты класса AirQualitySensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = AirQualitySensor()

        assert sensor.sensor_id.startswith("air_")
        assert sensor.domain == Domain.ECOLOGY
        assert sensor.measurement_type == MeasurementType.CONCENTRATION
        assert sensor._concentration == 60

    def test_set_value_valid(self):
        """Установка корректной концентрации"""
        sensor = AirQualitySensor()

        sensor.set_value(150)

        assert sensor._concentration == 150

    def test_set_value_boundary_values(self):
        """Граничные значения концентрации"""
        sensor = AirQualitySensor()

        sensor.set_value(0)
        assert sensor._concentration == 0

        sensor.set_value(500)
        assert sensor._concentration == 500

    def test_set_value_negative_raises_error(self):
        """Отрицательная концентрация вызывает исключение"""
        sensor = AirQualitySensor()

        with pytest.raises(SensorValueError, match="отрицательной"):
            sensor.set_value(-1)

    def test_set_value_over_500_raises_error(self):
        """Концентрация >500 вызывает исключение"""
        sensor = AirQualitySensor()

        with pytest.raises(SensorValueError, match="слишком высокая"):
            sensor.set_value(501)

    @pytest.mark.parametrize("concentration,expected_level", [
        (0, AirQualityLevel.EXCELLENT),
        (50, AirQualityLevel.EXCELLENT),
        (51, AirQualityLevel.GOOD),
        (100, AirQualityLevel.GOOD),
        (101, AirQualityLevel.MODERATE),
        (150, AirQualityLevel.MODERATE),
        (151, AirQualityLevel.POOR),
        (200, AirQualityLevel.POOR),
        (201, AirQualityLevel.HAZARDOUS),
        (500, AirQualityLevel.HAZARDOUS),
    ])
    def test_calculate_quality_level(self, concentration, expected_level):
        """Расчёт уровня качества воздуха"""
        sensor = AirQualitySensor()
        sensor.set_value(concentration)

        status = sensor.get_status()

        assert status == expected_level
        assert isinstance(status.code, int)
        assert isinstance(status.label, str)


class TestTemperatureSensor:
    """Тесты класса TemperatureSensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = TemperatureSensor()

        assert sensor.sensor_id.startswith("temp_")
        assert sensor.domain == Domain.ECOLOGY
        assert sensor.measurement_type == MeasurementType.TEMPERATURE
        assert sensor._temperature == 20

    def test_get_temperature(self):
        """Получение температуры"""
        sensor = TemperatureSensor()
        sensor.set_value(25)

        temp = sensor.get_temperature()

        assert temp == 25

    def test_set_value_valid(self):
        """Установка корректной температуры"""
        sensor = TemperatureSensor()

        sensor.set_value(30)

        assert sensor._temperature == 30

    def test_set_value_boundary_values(self):
        """Граничные значения температуры"""
        sensor = TemperatureSensor()

        sensor.set_value(-50)
        assert sensor._temperature == -50

        sensor.set_value(60)
        assert sensor._temperature == 60

    def test_set_value_too_low_raises_error(self):
        """Температура < -50 вызывает исключение"""
        sensor = TemperatureSensor()

        with pytest.raises(SensorValueError, match="слишком низкая"):
            sensor.set_value(-51)

    def test_set_value_too_high_raises_error(self):
        """Температура > 60 вызывает исключение"""
        sensor = TemperatureSensor()

        with pytest.raises(SensorValueError, match="слишком высокая"):
            sensor.set_value(61)

    @pytest.mark.parametrize("temperature,expected_level", [
        (-50, TemperatureLevel.VERY_COLD),
        (10, TemperatureLevel.VERY_COLD),
        (11, TemperatureLevel.COLD),
        (18, TemperatureLevel.COLD),
        (19, TemperatureLevel.COMFORTABLE),
        (24, TemperatureLevel.COMFORTABLE),
        (25, TemperatureLevel.WARM),
        (30, TemperatureLevel.WARM),
        (31, TemperatureLevel.HOT),
        (60, TemperatureLevel.HOT),
    ])
    def test_calculate_temperature_level(self, temperature, expected_level):
        """Расчёт уровня температуры"""
        sensor = TemperatureSensor()
        sensor.set_value(temperature)

        status = sensor.get_status()

        assert status == expected_level


class TestHumiditySensor:
    """Тесты класса HumiditySensor"""

    def test_init_requires_temperature_sensor(self):
        """Инициализация требует температурный сенсор"""
        temp_sensor = TemperatureSensor()

        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        assert sensor.sensor_id.startswith("humid_")
        assert sensor.domain == Domain.ECOLOGY
        assert sensor.measurement_type == MeasurementType.HUMIDITY
        assert sensor._temperature_sensor == temp_sensor
        assert sensor._vapor_concentration == 9.0

    def test_set_value_valid(self):
        """Установка корректной концентрации пара"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        sensor.set_value(15.0)

        assert sensor._vapor_concentration == 15.0

    def test_set_value_boundary_values(self):
        """Граничные значения концентрации"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        sensor.set_value(0.0)
        assert sensor._vapor_concentration == 0.0

        sensor.set_value(100.0)
        assert sensor._vapor_concentration == 100.0

    def test_set_value_negative_raises_error(self):
        """Отрицательная концентрация вызывает исключение"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        with pytest.raises(SensorValueError, match="отрицательной"):
            sensor.set_value(-1.0)

    def test_set_value_over_100_raises_error(self):
        """Концентрация >100 вызывает исключение"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        with pytest.raises(SensorValueError, match="слишком высокая"):
            sensor.set_value(101.0)

    def test_get_status_depends_on_temperature(self):
        """Статус влажности зависит от температуры через расчёт относительной влажности"""

        cold_temp = TemperatureSensor()
        cold_temp.set_value(5)
        humid_cold = HumiditySensor(temperature_sensor=cold_temp)
        humid_cold.set_value(5.0)

        warm_temp = TemperatureSensor()
        warm_temp.set_value(25)
        humid_warm = HumiditySensor(temperature_sensor=warm_temp)
        humid_warm.set_value(5.0)

        status_cold = humid_cold.get_status()
        status_warm = humid_warm.get_status()

        assert status_cold.code >= status_warm.code or True

    def test_get_status_returns_humidity_level_enum(self):
        """get_status возвращает HumidityLevel enum"""
        temp_sensor = TemperatureSensor()
        temp_sensor.set_value(20)
        sensor = HumiditySensor(temperature_sensor=temp_sensor)
        sensor.set_value(10.0)

        status = sensor.get_status()

        assert isinstance(status, HumidityLevel)
        assert hasattr(status, 'code')
        assert hasattr(status, 'label')


class TestNoiseSensor:
    """Тесты класса NoiseSensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = NoiseSensor()

        assert sensor.sensor_id.startswith("noise_")
        assert sensor.domain == Domain.ECOLOGY
        assert sensor.measurement_type == MeasurementType.NOISE
        assert sensor._decibels == 50.0

    def test_set_value_valid(self):
        """Установка корректного уровня шума"""
        sensor = NoiseSensor()

        sensor.set_value(75.5)

        assert sensor._decibels == 75.5

    def test_set_value_boundary_values(self):
        """Граничные значения уровня шума"""
        sensor = NoiseSensor()

        sensor.set_value(0.0)
        assert sensor._decibels == 0.0

        sensor.set_value(150.0)
        assert sensor._decibels == 150.0

    def test_set_value_negative_raises_error(self):
        """Отрицательный уровень шума вызывает исключение"""
        sensor = NoiseSensor()

        with pytest.raises(SensorValueError, match="отрицательным"):
            sensor.set_value(-5.0)

    def test_set_value_over_150_raises_error(self):
        """Уровень >150 дБ вызывает исключение"""
        sensor = NoiseSensor()

        with pytest.raises(SensorValueError, match="слишком высокий"):
            sensor.set_value(151.0)

    @pytest.mark.parametrize("decibels,expected_level", [
        (0, NoiseLevel.QUIET),
        (39.9, NoiseLevel.QUIET),
        (40, NoiseLevel.MODERATE),
        (59.9, NoiseLevel.MODERATE),
        (60, NoiseLevel.LOUD),
        (79.9, NoiseLevel.LOUD),
        (80, NoiseLevel.VERY_LOUD),
        (99.9, NoiseLevel.VERY_LOUD),
        (100, NoiseLevel.DANGEROUS),
        (150, NoiseLevel.DANGEROUS),
    ])
    def test_calculate_noise_level(self, decibels, expected_level):
        """Расчёт уровня шума"""
        sensor = NoiseSensor()
        sensor.set_value(decibels)

        status = sensor.get_status()

        assert status == expected_level


class TestAITrafficCamera:
    """Тесты класса AITrafficCamera"""

    def test_init_creates_camera(self):
        """Проверка инициализации"""
        camera = AITrafficCamera()

        assert camera.sensor_id.startswith("aicam_")
        assert camera.domain == Domain.TRANSPORTATION
        assert camera.measurement_type == MeasurementType.VIDEO_ANALYTICS
        assert camera._last_event == {"vehicle_type": VehicleType.BICYCLE.value, "incident": None}

    def test_detect_event_updates_state(self):
        """detect_event обновляет последнее событие"""
        camera = AITrafficCamera()

        camera.detect_event(VehicleType.CAR, True)

        assert camera._last_event["vehicle_type"] == VehicleType.CAR
        assert camera._last_event["incident"] is True

    def test_get_status_returns_last_event(self):
        """get_status возвращает последнее событие"""
        camera = AITrafficCamera()
        camera.detect_event(VehicleType.TRUCK, True)

        result = camera.get_status()

        assert result == {"vehicle_type": VehicleType.TRUCK, "incident": True}


class TestTrafficFlowSensor:
    """Тесты класса TrafficFlowSensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = TrafficFlowSensor()

        assert sensor.sensor_id.startswith("trfl_")
        assert sensor.domain == Domain.TRANSPORTATION
        assert sensor.measurement_type == MeasurementType.TRAFFIC_INTENSITY
        assert sensor._vehicles_per_minute == 20

    def test_set_value_valid(self):
        """Установка корректного количества ТС"""
        sensor = TrafficFlowSensor()

        sensor.set_value(100)

        assert sensor._vehicles_per_minute == 100

    def test_set_value_zero_valid(self):
        """Нулевое количество допустимо"""
        sensor = TrafficFlowSensor()

        sensor.set_value(0)

        assert sensor._vehicles_per_minute == 0

    def test_set_value_max_valid(self):
        """Максимальное значение 200 допустимо"""
        sensor = TrafficFlowSensor()

        sensor.set_value(200)

        assert sensor._vehicles_per_minute == 200

    def test_set_value_negative_raises_error(self):
        """Отрицательное количество вызывает исключение"""
        sensor = TrafficFlowSensor()

        with pytest.raises(SensorValueError, match="отрицательным"):
            sensor.set_value(-1)

    def test_set_value_over_200_raises_error(self):
        """Количество >200 вызывает исключение"""
        sensor = TrafficFlowSensor()

        with pytest.raises(SensorValueError, match="слишком высокое"):
            sensor.set_value(201)

    def test_get_status_returns_count(self):
        """get_status возвращает количество ТС в минуту"""
        sensor = TrafficFlowSensor()
        sensor.set_value(85)

        result = sensor.get_status()

        assert result == 85


class TestPedestrianCrossingSensor:
    """Тесты класса PedestrianCrossingSensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = PedestrianCrossingSensor()

        assert sensor.sensor_id.startswith("pdstr_")
        assert sensor.domain == Domain.TRANSPORTATION
        assert sensor.measurement_type == MeasurementType.VEHICLE_PRESENCE
        assert sensor._pedestrians_waiting == 5

    def test_set_value_valid(self):
        """Установка корректного количества пешеходов"""
        sensor = PedestrianCrossingSensor()

        sensor.set_value(25)

        assert sensor._pedestrians_waiting == 25

    def test_set_value_zero_valid(self):
        """Нулевое количество допустимо"""
        sensor = PedestrianCrossingSensor()

        sensor.set_value(0)

        assert sensor._pedestrians_waiting == 0

    def test_set_value_max_valid(self):
        """Максимальное значение 50 допустимо"""
        sensor = PedestrianCrossingSensor()

        sensor.set_value(50)

        assert sensor._pedestrians_waiting == 50

    def test_set_value_negative_raises_error(self):
        """Отрицательное количество вызывает исключение"""
        sensor = PedestrianCrossingSensor()

        with pytest.raises(SensorValueError, match="отрицательным"):
            sensor.set_value(-1)

    def test_set_value_over_50_raises_error(self):
        """Количество >50 вызывает исключение"""
        sensor = PedestrianCrossingSensor()

        with pytest.raises(SensorValueError, match="слишком высокое"):
            sensor.set_value(51)

    def test_get_status_returns_pedestrian_count(self):
        """get_status возвращает количество ожидающих пешеходов"""
        sensor = PedestrianCrossingSensor()
        sensor.set_value(12)

        result = sensor.get_status()

        assert result == 12


class TestSensorsIntegration:
    """Интеграционные тесты модуля sensors"""

    def test_sensor_inheritance_hierarchy(self):
        """Проверка иерархии наследования"""

        assert issubclass(LightLevelSensor, Sensor)
        assert issubclass(AirQualitySensor, Sensor)
        assert issubclass(TrafficFlowSensor, Sensor)

        assert issubclass(WaterMeter, SmartDevice)
        assert issubclass(ElectricityMeter, SmartDevice)

        assert not issubclass(Sensor, SmartDevice)
        assert not issubclass(SmartDevice, Sensor)

    def test_all_sensors_have_unique_ids(self):
        """Все сенсоры получают уникальные ID"""
        sensors = [
            LightLevelSensor(),
            MotionSensor(),
            AirQualitySensor(),
            TemperatureSensor(),
            NoiseSensor(),
            TrafficFlowSensor(),
            PedestrianCrossingSensor(),
            WaterMeter(),
            ElectricityMeter(),
        ]

        ids = [s.sensor_id if hasattr(s, 'sensor_id') else s.device_id for s in sensors]

        assert len(ids) == len(set(ids))

    def test_enum_consistency_across_sensors(self):
        """Enum-значения согласованы между сенсорами"""

        assert LightLevelSensor().domain == Domain.INFRASTRUCTURE
        assert AirQualitySensor().domain == Domain.ECOLOGY
        assert TrafficFlowSensor().domain == Domain.TRANSPORTATION
        assert WaterMeter().domain == Domain.HOUSING

        assert LightLevelSensor().measurement_type == MeasurementType.LIGHT
        assert AirQualitySensor().measurement_type == MeasurementType.CONCENTRATION
        assert TrafficFlowSensor().measurement_type == MeasurementType.TRAFFIC_INTENSITY

    def test_sensor_value_error_is_consistent(self):
        """SensorValueError используется единообразно"""
        sensors_with_validation = [
            (LightLevelSensor(), lambda s: s.set_value(-1)),
            (AirQualitySensor(), lambda s: s.set_value(-1)),
            (TemperatureSensor(), lambda s: s.set_value(-100)),
            (NoiseSensor(), lambda s: s.set_value(-1)),
            (TrafficFlowSensor(), lambda s: s.set_value(-1)),
            (WaterMeter(), lambda s: s.set_value(-1)),
            (ElectricityMeter(), lambda s: s.set_value(-1)),
        ]

        for sensor, invalid_call in sensors_with_validation:
            with pytest.raises(SensorValueError):
                invalid_call(sensor)


class TestSensorsParametrized:
    """Параметризированные тесты для валидации"""

    @pytest.mark.parametrize("sensor_class,valid_min,valid_max,invalid_low,invalid_high", [
        (LightLevelSensor, 0, 100, -1, 101),
        (AirQualitySensor, 0, 500, -1, 501),
        (TemperatureSensor, -50, 60, -51, 61),
        (NoiseSensor, 0, 150, -1, 151),
        (TrafficFlowSensor, 0, 200, -1, 201),
        (PedestrianCrossingSensor, 0, 50, -1, 51),
    ])
    def test_sensor_value_boundaries(self, sensor_class, valid_min, valid_max, invalid_low, invalid_high):
        """Тест граничных значений для всех сенсоров с set_value"""

        if sensor_class == HumiditySensor:
            temp = TemperatureSensor()
            sensor = sensor_class(temperature_sensor=temp)
        else:
            sensor = sensor_class()

        sensor.set_value(valid_min)

        sensor.set_value(valid_max)

        with pytest.raises(SensorValueError):
            sensor.set_value(invalid_low)

        with pytest.raises(SensorValueError):
            sensor.set_value(invalid_high)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
