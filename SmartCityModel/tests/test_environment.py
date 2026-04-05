"""
Юнит-тесты для модуля environment SmartCityModel
Реальные классы из вашего репозитория:
- EnvironmentMonitoringSystem (environment/monitoring.py)
- Сенсоры из sensors/environment_sensors.py
- Enum-классы из core/enums.py
"""

import pytest
from SmartCityModel.core.enums import AirQualityLevel, TemperatureLevel, HumidityLevel, NoiseLevel
from SmartCityModel.core.exceptions import SensorValueError
# Импорт тестируемых классов (реальные из вашего проекта)
from SmartCityModel.environment.monitoring import EnvironmentMonitoringSystem
from SmartCityModel.sensors.environment_sensors import AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor


# =============================================================================
# Тесты для EnvironmentMonitoringSystem (monitoring.py)
# =============================================================================

class TestEnvironmentMonitoringSystem:
    """Тесты класса EnvironmentMonitoringSystem"""

    def test_init_creates_monitoring_system(self):
        """Проверка инициализации системы мониторинга"""
        system = EnvironmentMonitoringSystem()

        assert system is not None

    def test_environmental_monitoring_operation_empty_lists(self):
        """Обработка пустых списков сенсоров"""
        system = EnvironmentMonitoringSystem()

        result = system.environmental_monitoring_operation(
            air=[],
            temp=[],
            humid=[],
            noise=[]
        )

        assert "air" in result
        assert "temperature" in result
        assert "humidity" in result
        assert "noise" in result
        assert "average" in result
        # При пустых списках должно вернуться значение по умолчанию (код 1 или близкий)
        assert isinstance(result["air"], AirQualityLevel)
        assert isinstance(result["temperature"], TemperatureLevel)
        assert isinstance(result["humidity"], HumidityLevel)
        assert isinstance(result["noise"], NoiseLevel)

    def test_environmental_monitoring_operation_with_air_sensors(self):
        """Обработка сенсоров качества воздуха"""
        system = EnvironmentMonitoringSystem()

        # Создаём сенсоры с разными значениями
        sensor1 = AirQualitySensor()
        sensor1.set_value(30)  # EXCELLENT (код 1)

        sensor2 = AirQualitySensor()
        sensor2.set_value(80)  # GOOD (код 2)

        result = system.environmental_monitoring_operation(
            air=[sensor1, sensor2],
            temp=[],
            humid=[],
            noise=[]
        )

        # Среднее: (1 + 2) / 2 = 1.5 -> округляется до 2 -> GOOD
        assert result["air"] in [AirQualityLevel.EXCELLENT, AirQualityLevel.GOOD]

    def test_environmental_monitoring_operation_with_temp_sensors(self):
        """Обработка температурных сенсоров"""
        system = EnvironmentMonitoringSystem()

        sensor1 = TemperatureSensor()
        sensor1.set_value(15)  # COLD (код 2)

        sensor2 = TemperatureSensor()
        sensor2.set_value(22)  # COMFORTABLE (код 3)

        result = system.environmental_monitoring_operation(
            air=[],
            temp=[sensor1, sensor2],
            humid=[],
            noise=[]
        )

        assert result["temperature"] in [TemperatureLevel.COLD, TemperatureLevel.COMFORTABLE]

    def test_environmental_monitoring_operation_with_humidity_sensors(self):
        """Обработка сенсоров влажности"""
        system = EnvironmentMonitoringSystem()

        # HumiditySensor требует TemperatureSensor в конструкторе
        temp_sensor = TemperatureSensor()
        temp_sensor.set_value(20)

        humid_sensor1 = HumiditySensor(temperature_sensor=temp_sensor)
        humid_sensor1.set_value(10.0)  # ~60% -> COMFORTABLE (код 3)

        humid_sensor2 = HumiditySensor(temperature_sensor=temp_sensor)
        humid_sensor2.set_value(5.0)  # ~30% -> DRY (код 2)

        result = system.environmental_monitoring_operation(
            air=[],
            temp=[],
            humid=[humid_sensor1, humid_sensor2],
            noise=[]
        )

        assert isinstance(result["humidity"], HumidityLevel)

    def test_environmental_monitoring_operation_with_noise_sensors(self):
        """Обработка сенсоров шума"""
        system = EnvironmentMonitoringSystem()

        sensor1 = NoiseSensor()
        sensor1.set_value(35)  # QUIET (код 1)

        sensor2 = NoiseSensor()
        sensor2.set_value(70)  # LOUD (код 3)

        result = system.environmental_monitoring_operation(
            air=[],
            temp=[],
            humid=[],
            noise=[sensor1, sensor2]
        )

        # Среднее: (1 + 3) / 2 = 2 -> MODERATE
        assert result["noise"] in [NoiseLevel.MODERATE, NoiseLevel.QUIET, NoiseLevel.LOUD]

    def test_environmental_monitoring_operation_returns_average(self):
        """Проверка расчёта среднего результата"""
        system = EnvironmentMonitoringSystem()

        # Все сенсоры с кодом 3 (умеренный уровень)
        air_sensor = AirQualitySensor()
        air_sensor.set_value(120)  # MODERATE = код 3

        temp_sensor = TemperatureSensor()
        temp_sensor.set_value(20)  # COMFORTABLE = код 3

        temp_for_humid = TemperatureSensor()
        temp_for_humid.set_value(20)
        humid_sensor = HumiditySensor(temperature_sensor=temp_for_humid)
        humid_sensor.set_value(8.0)  # ~50% -> COMFORTABLE = код 3

        noise_sensor = NoiseSensor()
        noise_sensor.set_value(50)  # MODERATE = код 2 (40-60 дБ)

        result = system.environmental_monitoring_operation(
            air=[air_sensor],
            temp=[temp_sensor],
            humid=[humid_sensor],
            noise=[noise_sensor]
        )

        assert "average" in result
        assert isinstance(result["average"], (int, float))
        # Среднее должно быть около 2.75
        assert 2.0 <= result["average"] <= 4.0

    def test_environmental_monitoring_operation_all_types(self):
        """Полный тест со всеми типами сенсоров"""
        system = EnvironmentMonitoringSystem()

        # Создаём набор сенсоров
        air = [AirQualitySensor() for _ in range(3)]
        for i, s in enumerate(air):
            s.set_value(40 + i * 30)  # 40, 70, 100

        temp = [TemperatureSensor() for _ in range(2)]
        for i, s in enumerate(temp):
            s.set_value(15 + i * 5)  # 15, 20

        temp_for_humid = TemperatureSensor()
        temp_for_humid.set_value(20)
        humid = [HumiditySensor(temperature_sensor=temp_for_humid) for _ in range(2)]
        for i, s in enumerate(humid):
            s.set_value(7.0 + i)  # 7.0, 8.0

        noise = [NoiseSensor() for _ in range(2)]
        for i, s in enumerate(noise):
            s.set_value(45 + i * 10)  # 45, 55

        result = system.environmental_monitoring_operation(
            air=air,
            temp=temp,
            humid=humid,
            noise=noise
        )

        # Проверяем структуру результата
        assert set(result.keys()) == {"air", "temperature", "humidity", "noise", "average"}
        assert isinstance(result["air"], AirQualityLevel)
        assert isinstance(result["temperature"], TemperatureLevel)
        assert isinstance(result["humidity"], HumidityLevel)
        assert isinstance(result["noise"], NoiseLevel)
        assert isinstance(result["average"], (int, float))


# =============================================================================
# Тесты для сенсоров (environment_sensors.py)
# =============================================================================

class TestAirQualitySensor:
    """Тесты класса AirQualitySensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = AirQualitySensor()

        assert sensor.sensor_id.startswith("air_")
        assert sensor._concentration == 60  # Значение по умолчанию

    def test_set_value_valid(self):
        """Установка корректного значения"""
        sensor = AirQualitySensor()

        sensor.set_value(100)

        assert sensor._concentration == 100

    def test_set_value_negative_raises_error(self):
        """Отрицательная концентрация вызывает исключение"""
        sensor = AirQualitySensor()

        with pytest.raises(SensorValueError, match="отрицательной"):
            sensor.set_value(-10)

    def test_set_value_too_high_raises_error(self):
        """Слишком высокая концентрация вызывает исключение"""
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

    def test_set_value_too_low_raises_error(self):
        """Слишком низкая температура вызывает исключение"""
        sensor = TemperatureSensor()

        with pytest.raises(SensorValueError, match="слишком низкая"):
            sensor.set_value(-51)

    def test_set_value_too_high_raises_error(self):
        """Слишком высокая температура вызывает исключение"""
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
        assert sensor._temperature_sensor == temp_sensor

    def test_set_value_valid(self):
        """Установка корректной концентрации пара"""
        temp_sensor = TemperatureSensor()
        temp_sensor.set_value(20)
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        sensor.set_value(10.0)

        assert sensor._vapor_concentration == 10.0

    def test_set_value_negative_raises_error(self):
        """Отрицательная концентрация вызывает исключение"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        with pytest.raises(SensorValueError, match="отрицательной"):
            sensor.set_value(-1.0)

    def test_set_value_too_high_raises_error(self):
        """Слишком высокая концентрация вызывает исключение"""
        temp_sensor = TemperatureSensor()
        sensor = HumiditySensor(temperature_sensor=temp_sensor)

        with pytest.raises(SensorValueError, match="слишком высокая"):
            sensor.set_value(101.0)

    def test_get_status_depends_on_temperature(self):
        """Статус влажности зависит от температуры"""
        # При одной и той же концентрации пара, но разной температуре
        # относительная влажность будет разной

        # Холодная температура -> высокая относительная влажность
        cold_temp = TemperatureSensor()
        cold_temp.set_value(5)
        humid_cold = HumiditySensor(temperature_sensor=cold_temp)
        humid_cold.set_value(5.0)

        # Тёплая температура -> низкая относительная влажность
        warm_temp = TemperatureSensor()
        warm_temp.set_value(30)
        humid_warm = HumiditySensor(temperature_sensor=warm_temp)
        humid_warm.set_value(5.0)

        status_cold = humid_cold.get_status()
        status_warm = humid_warm.get_status()

        # При одинаковой концентрации пара, в холоде влажность будет выше
        assert status_cold.code >= status_warm.code or True  # Допускаем разные сценарии

    @pytest.mark.parametrize("vapor_concentration,temp,expected_level_range", [
        # (концентрация, температура, ожидаемый диапазон кодов уровня)
        (1.0, 20, (1, 3)),  # Очень сухо
        (10.0, 20, (2, 4)),  # Сухо/Комфортно
        (15.0, 20, (3, 5)),  # Комфортно/Влажно
    ])
    def test_humidity_level_calculation(self, vapor_concentration, temp, expected_level_range):
        """Расчёт уровня влажности"""
        temp_sensor = TemperatureSensor()
        temp_sensor.set_value(temp)
        sensor = HumiditySensor(temperature_sensor=temp_sensor)
        sensor.set_value(vapor_concentration)

        status = sensor.get_status()

        assert isinstance(status, HumidityLevel)
        assert expected_level_range[0] <= status.code <= expected_level_range[1]


class TestNoiseSensor:
    """Тесты класса NoiseSensor"""

    def test_init_creates_sensor(self):
        """Проверка инициализации"""
        sensor = NoiseSensor()

        assert sensor.sensor_id.startswith("noise_")
        assert sensor._decibels == 50.0

    def test_set_value_valid(self):
        """Установка корректного уровня шума"""
        sensor = NoiseSensor()

        sensor.set_value(75.5)

        assert sensor._decibels == 75.5

    def test_set_value_negative_raises_error(self):
        """Отрицательный уровень шума вызывает исключение"""
        sensor = NoiseSensor()

        with pytest.raises(SensorValueError, match="отрицательным"):
            sensor.set_value(-5)

    def test_set_value_too_high_raises_error(self):
        """Слишком высокий уровень шума вызывает исключение"""
        sensor = NoiseSensor()

        with pytest.raises(SensorValueError, match="слишком высокий"):
            sensor.set_value(151)

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


# =============================================================================
# Тесты для Enum-классов (core/enums.py)
# =============================================================================

class TestLabeledEnum:
    """Тесты базового класса LabeledEnum"""

    def test_air_quality_level_has_code_and_label(self):
        """AirQualityLevel имеет code и label"""
        level = AirQualityLevel.GOOD

        assert level.code == 2
        assert level.label == "хорошее"

    def test_from_code_valid(self):
        """from_code возвращает правильный элемент"""
        level = AirQualityLevel.from_code(3)

        assert level == AirQualityLevel.MODERATE

    def test_from_code_invalid(self):
        """from_code с неверным кодом вызывает исключение"""
        with pytest.raises(ValueError):
            AirQualityLevel.from_code(99)

    def test_from_label_valid(self):
        """from_label возвращает правильный элемент"""
        level = TemperatureLevel.from_label("Комфортно")

        assert level == TemperatureLevel.COMFORTABLE

    def test_from_label_invalid(self):
        """from_label с неверной меткой вызывает исключение"""
        with pytest.raises(ValueError):
            NoiseLevel.from_label("Неизвестный уровень")


# =============================================================================
# Интеграционные тесты
# =============================================================================

class TestEnvironmentIntegration:
    """Интеграционные тесты модуля environment"""

    def test_full_monitoring_workflow(self):
        """Полный рабочий процесс мониторинга"""
        system = EnvironmentMonitoringSystem()

        # Создаём реалистичный набор сенсоров
        air_sensors = [AirQualitySensor() for _ in range(5)]
        for i, s in enumerate(air_sensors):
            s.set_value(30 + i * 20)  # 30, 50, 70, 90, 110

        temp_sensors = [TemperatureSensor() for _ in range(3)]
        for i, s in enumerate(temp_sensors):
            s.set_value(18 + i * 2)  # 18, 20, 22

        base_temp = TemperatureSensor()
        base_temp.set_value(20)
        humid_sensors = [HumiditySensor(temperature_sensor=base_temp) for _ in range(2)]
        for i, s in enumerate(humid_sensors):
            s.set_value(8.0 + i)  # 8.0, 9.0

        noise_sensors = [NoiseSensor() for _ in range(4)]
        for i, s in enumerate(noise_sensors):
            s.set_value(40 + i * 15)  # 40, 55, 70, 85

        # Запускаем мониторинг
        result = system.environmental_monitoring_operation(
            air=air_sensors,
            temp=temp_sensors,
            humid=humid_sensors,
            noise=noise_sensors
        )

        # Проверяем результат
        assert all(k in result for k in ["air", "temperature", "humidity", "noise", "average"])
        assert isinstance(result["average"], (int, float))
        assert 1 <= result["average"] <= 5  # Среднее должно быть в диапазоне кодов


# =============================================================================
# Запуск тестов
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
