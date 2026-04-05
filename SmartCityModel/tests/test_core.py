"""
Юнит-тесты для модуля SmartCityModel.core
Классы: SmartDevice, валидаторы, исключения, Enum-классы
Запуск: pytest tests/test_core.py -v
"""

import pytest
import uuid
from decimal import Decimal, InvalidOperation
from typing import Optional, Union

# Импорты тестируемых компонентов
from SmartCityModel.core import (
    # Enums
    Domain, VehicleType, Direction, TrafficLightColor, PlanningMetricType,
    MeasurementType, AirQualityLevel, TemperatureLevel, HumidityLevel, NoiseLevel,
    # Base
    SmartDevice,
    # Exceptions
    HospitalException, TransportException, SensorValueError, ObjectNotFoundError,
    # Validators
    ValidationError, NumberValidationError,
    RussianStringValidator, NumberValidator, LatinStringValidator, IdentifierValidator,
)


# =============================================================================
# ТЕСТЫ ДЛЯ ENUM-КЛАССОВ
# =============================================================================

class TestDomainEnum:
    """Тесты для Enum Domain"""

    def test_domain_values(self):
        """Проверка значений доменов"""
        assert Domain.TRANSPORTATION.value == "transportation"
        assert Domain.ECOLOGY.value == "ecology"
        assert Domain.INFRASTRUCTURE.value == "infrastructure"
        assert Domain.SAFETY.value == "safety"
        assert Domain.HEALTHCARE.value == "healthcare"
        assert Domain.EDUCATION.value == "education"
        assert Domain.HOUSING.value == "housing"

    def test_domain_membership(self):
        """Проверка принадлежности значений к Enum"""
        assert Domain("transportation") is Domain.TRANSPORTATION
        assert Domain("ecology") is Domain.ECOLOGY

    def test_domain_invalid_value_raises(self):
        """Проверка ошибки при неверном значении"""
        with pytest.raises(ValueError):
            Domain("invalid_domain")


class TestVehicleTypeEnum:
    """Тесты для Enum VehicleType"""

    def test_vehicle_type_values(self):
        """Проверка значений типов транспорта"""
        assert VehicleType.CAR.value == "car"
        assert VehicleType.BUS.value == "bus"
        assert VehicleType.TRAM.value == "tram"
        assert VehicleType.AMBULANCE.value == "ambulance"
        assert VehicleType.FIRE_TRUCK.value == "fire_truck"

    def test_vehicle_type_count(self):
        """Проверка количества типов транспорта"""
        assert len(list(
            VehicleType)) == 10  # CAR, BUS, TRAM, TROLLEYBUS, TRUCK, AMBULANCE, FIRE_TRUCK, POLICE, BICYCLE, MOTORCYCLE

    def test_vehicle_type_from_string(self):
        """Проверка создания из строки"""
        assert VehicleType("bicycle") is VehicleType.BICYCLE


class TestDirectionEnum:
    """Тесты для Enum Direction"""

    def test_direction_values(self):
        """Проверка значений направлений"""
        assert Direction.NORTH.value == "N"
        assert Direction.SOUTH.value == "S"
        assert Direction.EAST.value == "E"
        assert Direction.WEST.value == "W"

    def test_direction_iteration(self):
        """Проверка итерации по направлениям"""
        directions = [d.value for d in Direction]
        assert set(directions) == {"N", "S", "E", "W"}


class TestTrafficLightColorEnum:
    """Тесты для Enum TrafficLightColor"""

    def test_color_values(self):
        """Проверка значений цветов светофора"""
        assert TrafficLightColor.GREEN.value == "green"
        assert TrafficLightColor.YELLOW.value == "yellow"
        assert TrafficLightColor.RED.value == "red"


class TestPlanningMetricTypeEnum:
    """Тесты для Enum PlanningMetricType"""

    def test_metric_values(self):
        """Проверка значений метрик планирования"""
        assert PlanningMetricType.ECOLOGY_SCORE.value == "ecology_score"
        assert PlanningMetricType.TRANSPORT_LOAD.value == "transport_load"
        assert PlanningMetricType.INFRASTRUCTURE_DENSITY.value == "infrastructure_density"
        assert PlanningMetricType.LIVEABILITY_INDEX.value == "liveability_index"


class TestMeasurementTypeEnum:
    """Тесты для Enum MeasurementType"""

    def test_measurement_types(self):
        """Проверка типов измерений"""
        assert MeasurementType.TEMPERATURE.value == "temperature"
        assert MeasurementType.HUMIDITY.value == "humidity"
        assert MeasurementType.NOISE.value == "noise"
        assert MeasurementType.AIR_QUALITY.value == "air_quality"
        assert MeasurementType.TRAFFIC_INTENSITY.value == "traffic_intensity"


class TestLabeledEnumBase:
    """Тесты для базового класса LabeledEnum"""

    def test_air_quality_level_codes(self):
        """Проверка кодов уровней качества воздуха"""
        assert AirQualityLevel.EXCELLENT.code == 1
        assert AirQualityLevel.GOOD.code == 2
        assert AirQualityLevel.MODERATE.code == 3
        assert AirQualityLevel.POOR.code == 4
        assert AirQualityLevel.HAZARDOUS.code == 5

    def test_air_quality_level_labels(self):
        """Проверка меток уровней качества воздуха"""
        assert AirQualityLevel.EXCELLENT.label == "отличное"
        assert AirQualityLevel.GOOD.label == "хорошее"
        assert AirQualityLevel.HAZARDOUS.label == "ужасное"

    def test_from_code_success(self):
        """Проверка получения элемента по коду"""
        level = AirQualityLevel.from_code(3)
        assert level is AirQualityLevel.MODERATE
        assert level.label == "умеренное"

    def test_from_code_invalid(self):
        """Проверка ошибки при неверном коде"""
        with pytest.raises(ValueError, match="Нет элемента.*с кодом 99"):
            AirQualityLevel.from_code(99)

    def test_from_label_success(self):
        """Проверка получения элемента по метке"""
        level = TemperatureLevel.from_label("Комфортно")
        assert level is TemperatureLevel.COMFORTABLE
        assert level.code == 3

    def test_from_label_invalid(self):
        """Проверка ошибки при неверной метке"""
        with pytest.raises(ValueError, match="Нет элемента.*с меткой"):
            HumidityLevel.from_label("Неизвестно")

    @pytest.mark.parametrize("enum_class,expected_count", [
        (TemperatureLevel, 5),
        (HumidityLevel, 5),
        (NoiseLevel, 5),
        (AirQualityLevel, 5),
    ])
    def test_labeled_enum_members_count(self, enum_class, expected_count):
        """Проверка количества элементов в перечислениях"""
        assert len(list(enum_class)) == expected_count


class TestNoiseLevelEnum:
    """Тесты для Enum NoiseLevel"""

    def test_noise_levels_range(self):
        """Проверка диапазонов уровней шума по кодам"""
        assert NoiseLevel.QUIET.code == 1  # < 40 дБ
        assert NoiseLevel.MODERATE.code == 2  # 40-60 дБ
        assert NoiseLevel.LOUD.code == 3  # 60-80 дБ
        assert NoiseLevel.VERY_LOUD.code == 4  # 80-100 дБ
        assert NoiseLevel.DANGEROUS.code == 5  # > 100 дБ


# =============================================================================
# ТЕСТЫ ДЛЯ КЛАССА SmartDevice
# =============================================================================

class TestSmartDevice:
    """Тесты для базового класса устройств"""

    def test_smart_device_initialization(self):
        """Проверка инициализации устройства"""
        device = SmartDevice("sensor_", Domain.ECOLOGY)

        assert device.domain is Domain.ECOLOGY
        assert device.device_id.startswith("sensor_")
        # Проверяем, что device_id имеет формат: keyword + 6 символов UUID
        assert len(device.device_id) == len("sensor_") + 6

    def test_smart_device_unique_ids(self):
        """Проверка уникальности ID при создании нескольких устройств"""
        device1 = SmartDevice("dev_", Domain.TRANSPORTATION)
        device2 = SmartDevice("dev_", Domain.TRANSPORTATION)

        assert device1.device_id != device2.device_id
        assert device1.domain is device2.domain

    def test_smart_device_different_keywords(self):
        """Проверка устройств с разными ключевыми словами"""
        sensor = SmartDevice("sensor_", Domain.ECOLOGY)
        light = SmartDevice("light_", Domain.INFRASTRUCTURE)

        assert sensor.device_id.startswith("sensor_")
        assert light.device_id.startswith("light_")
        assert sensor.domain is Domain.ECOLOGY
        assert light.domain is Domain.INFRASTRUCTURE

    def test_smart_device_id_format(self):
        """Проверка формата device_id (keyword + hex из UUID)"""
        device = SmartDevice("test_", Domain.SAFETY)
        suffix = device.device_id[len("test_"):]

        # suffix должен быть 6 символов из hex-представления UUID
        assert len(suffix) == 6
        assert all(c in "0123456789abcdef" for c in suffix.lower())


# =============================================================================
# ТЕСТЫ ДЛЯ ИСКЛЮЧЕНИЙ
# =============================================================================

class TestCoreExceptions:
    """Тесты для кастомных исключений"""

    def test_hospital_exception_inheritance(self):
        """Проверка наследования HospitalException"""
        assert issubclass(HospitalException, Exception)

        exc = HospitalException("Тест")
        assert str(exc) == "Тест"

    def test_transport_exception_inheritance(self):
        """Проверка наследования TransportException"""
        assert issubclass(TransportException, Exception)

        exc = TransportException("Ошибка транспорта")
        assert "транспорта" in str(exc)

    def test_sensor_value_error_inheritance(self):
        """Проверка наследования SensorValueError"""
        assert issubclass(SensorValueError, Exception)

        exc = SensorValueError("Неверное значение")
        assert "Неверное" in str(exc)

    def test_object_not_found_error_inheritance(self):
        """Проверка наследования ObjectNotFoundError"""
        assert issubclass(ObjectNotFoundError, Exception)

        exc = ObjectNotFoundError("Объект не найден")
        assert "не найден" in str(exc)

    def test_exceptions_can_be_raised_and_caught(self):
        """Проверка возможности выброса и перехвата исключений"""

        def raise_hospital_error():
            raise HospitalException("Критическая ошибка")

        with pytest.raises(HospitalException) as exc_info:
            raise_hospital_error()

        assert "Критическая" in str(exc_info.value)


# =============================================================================
# ТЕСТЫ ДЛЯ VALIDATIONERROR И NumberValidationError
# =============================================================================

class TestValidationError:
    """Тесты для базовых исключений валидации"""

    def test_validation_error_message(self):
        """Проверка сообщения ошибки валидации"""
        exc = ValidationError("Неверный ввод")
        assert str(exc) == "Неверный ввод"

    def test_number_validation_error_message(self):
        """Проверка сообщения ошибки валидации числа"""
        exc = NumberValidationError("Число вне диапазона")
        assert str(exc) == "Число вне диапазона"

    def test_validation_error_inheritance(self):
        """Проверка иерархии исключений"""
        assert issubclass(ValidationError, Exception)
        assert issubclass(NumberValidationError, Exception)


# =============================================================================
# ТЕСТЫ ДЛЯ RussianStringValidator
# =============================================================================

class TestRussianStringValidator:
    """Тесты для валидатора русских строк"""

    def test_init_default_params(self):
        """Проверка инициализации с параметрами по умолчанию"""
        validator = RussianStringValidator()
        assert validator.min_length == 1
        assert validator.max_length == 100

    def test_init_custom_params(self):
        """Проверка инициализации с кастомными параметрами"""
        validator = RussianStringValidator(min_length=3, max_length=50)
        assert validator.min_length == 3
        assert validator.max_length == 50

    def test_init_invalid_min_length(self):
        """Проверка ошибки при min_length < 1"""
        with pytest.raises(ValueError, match="Минимальная длина"):
            RussianStringValidator(min_length=0)

    def test_init_max_less_than_min(self):
        """Проверка ошибки при max_length < min_length"""
        with pytest.raises(ValueError, match="Максимальная длина"):
            RussianStringValidator(min_length=10, max_length=5)

    @pytest.mark.parametrize("valid_string", [
        "Анна",
        "Иван Петров",
        "г. Москва",
        "ул.Ленина",
        "Ёлки-Палки",  # с буквой Ё
        "Тест.Строка",  # с точками
    ])
    def test_validate_success(self, valid_string):
        """Проверка успешной валидации корректных строк"""
        validator = RussianStringValidator(allow_spaces=True)
        result = validator.validate(valid_string)
        assert result == valid_string.strip()

    @pytest.mark.parametrize("invalid_string,expected_error", [
        ("", "Строка не может быть пустой"),
        ("   ", "Строка не может быть пустой"),
        ("A", "Недопустимый символ"),  # латиница
        ("..", "Строка должна содержать хотя бы одну букву"),
        ("Test123", "Недопустимый символ"),
        ("Иван@Mail", "Недопустимый символ"),  # спецсимвол
        ("а" * 101, "Строка слишком длинная"),  # при max_length=100
    ])
    def test_validate_failure(self, invalid_string, expected_error):
        """Проверка отклонения некорректных строк"""
        validator = RussianStringValidator()
        with pytest.raises(ValidationError, match=expected_error):
            validator.validate(invalid_string)

    def test_validate_trims_whitespace(self):
        """Проверка удаления пробелов по краям"""
        validator = RussianStringValidator(allow_spaces=True)
        result = validator.validate("  Анна Петрова  ")
        assert result == "Анна Петрова"  # после strip

    def test_validate_min_length_custom(self):
        """Проверка минимальной длины с кастомным параметром"""
        validator = RussianStringValidator(min_length=5)
        with pytest.raises(ValidationError, match="слишком короткая"):
            validator.validate("Анна")  # 4 символа

        result = validator.validate("АннаП")  # 5 символов
        assert result == "АннаП"

    def test_validate_max_length_custom(self):
        """Проверка максимальной длины с кастомным параметром"""
        validator = RussianStringValidator(max_length=10)
        with pytest.raises(ValidationError, match="слишком длинная"):
            validator.validate("ОченьДлинноеИмя")  # 15 символов

        result = validator.validate("Коротко")  # 7 символов
        assert result == "Коротко"

    def test_validate_allows_dots(self):
        """Проверка разрешения точек в строке"""
        validator = RussianStringValidator()
        result = validator.validate("г.Санкт-Петербург")  # точка разрешена, дефис - нет
        assert result


# =============================================================================
# ТЕСТЫ ДЛЯ NumberValidator
# =============================================================================

class TestNumberValidator:
    """Тесты для валидатора чисел"""

    def test_init_default_params(self):
        """Проверка инициализации с параметрами по умолчанию"""
        validator = NumberValidator()
        assert validator.min_value is None
        assert validator.max_value is None
        assert validator.max_digits == 15
        assert validator.max_decimal_places == 5
        assert validator.allow_negative is True

    def test_init_custom_params(self):
        """Проверка инициализации с кастомными параметрами"""
        validator = NumberValidator(
            min_value=0, max_value=100, max_digits=5,
            max_decimal_places=2, allow_negative=False
        )
        assert validator.min_value == 0
        assert validator.max_value == 100
        assert validator.allow_negative is False

    def test_init_invalid_params(self):
        """Проверка ошибок при некорректных параметрах"""
        with pytest.raises(ValueError, match="max_digits"):
            NumberValidator(max_digits=0)

        with pytest.raises(ValueError, match="max_decimal_places"):
            NumberValidator(max_decimal_places=-1)

        with pytest.raises(ValueError, match="min_value не может быть больше"):
            NumberValidator(min_value=100, max_value=50)

    # validate_int tests
    @pytest.mark.parametrize("valid_input,expected", [
        ("42", 42),
        (42, 42),
        ("-10", -10),
        ("0", 0),
        ("999999999999999", 999999999999999),  # 15 цифр
    ])
    def test_validate_int_success(self, valid_input, expected):
        """Проверка успешной валидации целых чисел"""
        validator = NumberValidator()
        result = validator.validate_int(valid_input)
        assert result == expected
        assert isinstance(result, int)

    @pytest.mark.parametrize("invalid_input,expected_error", [
        (None, "Значение не может быть пустым"),
        (True, "Булевый тип не допускается"),
        ("", "Строка не может быть пустой"),
        ("   ", "Строка не может быть пустой"),
        ("12.34", "Недопустимые символы"),  # точка для int
        ("abc", "Недопустимые символы"),
        ("123.45.67", "Недопустимые символы"),
        ("1" * 16, "Слишком много цифр"),  # 16 цифр > max_digits=15
    ])
    def test_validate_int_failure(self, invalid_input, expected_error):
        """Проверка отклонения некорректных целых чисел"""
        validator = NumberValidator()
        with pytest.raises(NumberValidationError, match=expected_error):
            validator.validate_int(invalid_input)

    def test_validate_int_range(self):
        """Проверка диапазона для целых чисел"""
        validator = NumberValidator(min_value=1, max_value=100)

        assert validator.validate_int(50) == 50

        with pytest.raises(NumberValidationError, match="меньше минимума"):
            validator.validate_int(0)

        with pytest.raises(NumberValidationError, match="больше максимума"):
            validator.validate_int(101)

    def test_validate_int_no_negative(self):
        """Проверка запрета отрицательных чисел"""
        validator = NumberValidator(allow_negative=False)

        assert validator.validate_int(42) == 42

        with pytest.raises(NumberValidationError, match="Отрицательные"):
            validator.validate_int(-1)

    # validate_float tests
    @pytest.mark.parametrize("valid_input,expected", [
        ("3.14", 3.14),
        (3.14, 3.14),
        ("3,14", 3.14),  # запятая как десятичный разделитель
        ("-2.5", -2.5),
        ("0.001", 0.001),
        (100, 100.0),  # int -> float
    ])
    def test_validate_float_success(self, valid_input, expected):
        """Проверка успешной валидации чисел с плавающей точкой"""
        validator = NumberValidator()
        result = validator.validate_float(valid_input)
        assert abs(result - expected) < 1e-9
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_input,expected_error", [
        (None, "Значение не может быть пустым"),
        (True, "Булевый тип не допускается"),
        ("", "Строка не может быть пустой"),
        ("12.34.56", "Недопустимый формат"),
        ("abc", "Недопустимый формат"),
        ("1.2.3", "Недопустимый формат"),
        ("1" * 16, "Слишком много цифр"),
    ])
    def test_validate_float_failure(self, invalid_input, expected_error):
        """Проверка отклонения некорректных чисел с плавающей точкой"""
        validator = NumberValidator()
        with pytest.raises(NumberValidationError, match=expected_error):
            validator.validate_float(invalid_input)

    def test_validate_float_decimal_places(self):
        """Проверка ограничения знаков после запятой"""
        validator = NumberValidator(max_decimal_places=2)

        assert validator.validate_float("3.14") == 3.14

        with pytest.raises(NumberValidationError, match="Слишком много знаков"):
            validator.validate_float("3.14159")

    def test_validate_float_range(self):
        """Проверка диапазона для чисел с плавающей точкой"""
        validator = NumberValidator(min_value=0.0, max_value=10.0)

        assert validator.validate_float(5.5) == 5.5

        with pytest.raises(NumberValidationError, match="меньше минимума"):
            validator.validate_float(-0.1)

        with pytest.raises(NumberValidationError, match="больше максимума"):
            validator.validate_float(10.1)


# =============================================================================
# ТЕСТЫ ДЛЯ LatinStringValidator
# =============================================================================

class TestLatinStringValidator:
    """Тесты для валидатора латинских строк"""

    def test_init_default_params(self):
        """Проверка инициализации по умолчанию"""
        validator = LatinStringValidator()
        assert validator.min_length == 1
        assert validator.max_length == 100
        assert validator.allow_hyphen is False
        assert validator.allow_spaces is False

    def test_init_custom_params(self):
        """Проверка инициализации с кастомными параметрами"""
        validator = LatinStringValidator(
            min_length=2, max_length=20, allow_hyphen=True, allow_spaces=True
        )
        assert validator.allow_hyphen is True
        assert validator.allow_spaces is True

    @pytest.mark.parametrize("valid_string", [
        "Test",
        "user",
        "ABC",
        "testName",
    ])
    def test_validate_success(self, valid_string):
        """Проверка успешной валидации латинских строк"""
        validator = LatinStringValidator()
        result = validator.validate(valid_string)
        assert result == valid_string.strip()

    @pytest.mark.parametrize("invalid_string,expected_error", [
        ("", "Строка слишком короткая"),
        ("Тест", "Невалидная строка"),  # кириллица
        ("123", "Невалидная строка"),  # только цифры
        ("test@email", "Невалидная строка"),  # спецсимвол
        ("a" * 101, "Строка слишком длинная"),
    ])
    def test_validate_failure(self, invalid_string, expected_error):
        """Проверка отклонения некорректных латинских строк"""
        validator = LatinStringValidator()
        with pytest.raises(ValidationError, match=expected_error):
            validator.validate(invalid_string)

    def test_validate_with_hyphen(self):
        """Проверка разрешения дефиса"""
        validator = LatinStringValidator(allow_hyphen=True)
        result = validator.validate("test-name")
        assert result == "test-name"

        # Без разрешения дефиса должна быть ошибка
        validator_no_hyphen = LatinStringValidator(allow_hyphen=False)
        with pytest.raises(ValidationError):
            validator_no_hyphen.validate("test-name")

    def test_validate_with_spaces(self):
        """Проверка разрешения пробелов"""
        validator = LatinStringValidator(allow_spaces=True)
        result = validator.validate("test name")
        assert result == "test name"

        # Без разрешения пробелов должна быть ошибка
        validator_no_spaces = LatinStringValidator(allow_spaces=False)
        with pytest.raises(ValidationError):
            validator_no_spaces.validate("test name")

    def test_validate_requires_letter(self):
        """Проверка обязательного наличия буквы"""
        validator = LatinStringValidator()
        with pytest.raises(ValidationError, match="Невалидная строка"):
            validator.validate("12345")  # только цифры


# =============================================================================
# ТЕСТЫ ДЛЯ IdentifierValidator
# =============================================================================

class TestIdentifierValidator:
    """Тесты для валидатора идентификаторов"""

    def test_init_default_params(self):
        """Проверка инициализации по умолчанию"""
        validator = IdentifierValidator()
        assert validator.min_length == 1
        assert validator.max_length == 50

    def test_init_custom_params(self):
        """Проверка инициализации с кастомными параметрами"""
        validator = IdentifierValidator(min_length=3, max_length=20)
        assert validator.min_length == 3
        assert validator.max_length == 20

    @pytest.mark.parametrize("valid_id", [
        "user_123",
        "device001",
        "sensor_temp_01",
        "ABC",
        "test_id_99",
        "_private",
        "a",  # минимальная длина 1
    ])
    def test_validate_success(self, valid_id):
        """Проверка успешной валидации идентификаторов"""
        validator = IdentifierValidator()
        result = validator.validate(valid_id)
        assert result == valid_id.strip()

    @pytest.mark.parametrize("invalid_id,expected_error", [
        ("", "ID не может быть пустым"),
        ("   ", "ID не может быть пустым"),
        ("Тест", "Недопустимый символ"),  # кириллица
        ("test.id", "Недопустимый символ"),  # точка не разрешена
        ("test id", "Недопустимый символ"),  # пробел не разрешён
        ("a" * 51, "ID слишком длинный")
    ])
    def test_validate_failure(self, invalid_id, expected_error):
        """Проверка отклонения некорректных идентификаторов"""
        validator = IdentifierValidator()
        with pytest.raises(ValidationError, match=expected_error):
            validator.validate(invalid_id)

    def test_validate_allows_underscore(self):
        """Проверка разрешения нижнего подчёркивания"""
        validator = IdentifierValidator()
        result = validator.validate("my_identifier_123")
        assert result == "my_identifier_123"

    def test_validate_allows_digits(self):
        """Проверка разрешения цифр"""
        validator = IdentifierValidator()
        result = validator.validate("sensor123")
        assert result == "sensor123"

    def test_validate_trims_whitespace(self):
        """Проверка удаления пробелов по краям"""
        validator = IdentifierValidator()
        result = validator.validate("  test_id  ")
        assert result == "test_id"  # после strip


# =============================================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# =============================================================================

class TestCoreIntegration:
    """Интеграционные тесты взаимодействия компонентов core"""

    def test_smart_device_with_validators(self):
        """Проверка использования валидаторов с устройствами"""
        # Валидируем keyword для устройства
        keyword_validator = LatinStringValidator(min_length=3, max_length=20, allow_underscore=True)
        keyword = keyword_validator.validate("sensor_")

        device = SmartDevice(keyword, Domain.ECOLOGY)
        assert device.device_id.startswith("sensor_")

    def test_enum_with_validator(self):
        """Проверка использования Enum с валидаторами"""
        # Валидируем значение домена как строку
        domain_validator = LatinStringValidator()
        domain_str = domain_validator.validate("transportation")

        # Преобразуем в Enum
        domain = Domain(domain_str)
        assert domain is Domain.TRANSPORTATION

    def test_exception_hierarchy_usage(self):
        """Проверка иерархии исключений в обработке ошибок"""

        def process_sensor(value: Optional[float]) -> float:
            if value is None:
                raise SensorValueError("Пустое значение сенсора")
            if value < 0:
                raise NumberValidationError("Отрицательное значение")
            return value

        with pytest.raises(SensorValueError):
            process_sensor(None)

        with pytest.raises(NumberValidationError):
            process_sensor(-5.0)

        assert process_sensor(42.5) == 42.5

    def test_labeled_enum_workflow(self):
        """Проверка рабочего процесса с LabeledEnum"""
        # Получаем уровень по коду
        level = NoiseLevel.from_code(3)
        assert level.label == "Шумный"

        # Используем в логике
        if level.code >= 4:
            action = "Требуется шумоизоляция"
        else:
            action = "Допустимый уровень"

        assert action == "Допустимый уровень"