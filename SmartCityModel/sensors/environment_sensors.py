import math

from .base_sensor import Sensor
from ..core import Domain, MeasurementType, AirQualityLevel, TemperatureLevel, HumidityLevel, NoiseLevel, SensorValueError


class AirQualitySensor(Sensor):
    def __init__(self) -> None:
        super().__init__("air_", Domain.ECOLOGY, MeasurementType.CONCENTRATION)
        self._concentration = 60

    def set_value(self, concentration: int) -> None:
        if concentration < 0:
            raise SensorValueError("Концентрация не может быть отрицательной.")
        elif concentration > 500:
            raise SensorValueError("Концентрация слишком высокая.")
        self._concentration = concentration

    def _calculate_quality_level(self) -> AirQualityLevel:
        if self._concentration <= 50:
            return AirQualityLevel.EXCELLENT  # Отличное
        elif self._concentration <= 100:
            return AirQualityLevel.GOOD  # Хорошее
        elif self._concentration <= 150:
            return AirQualityLevel.MODERATE  # Умеренное
        elif self._concentration <= 200:
            return AirQualityLevel.POOR  # Плохое
        else:
            return AirQualityLevel.HAZARDOUS  # Опасное

    def get_status(self) -> AirQualityLevel:
        return self._calculate_quality_level()


class TemperatureSensor(Sensor):
    def __init__(self) -> None:
        super().__init__("temp_", Domain.ECOLOGY, MeasurementType.TEMPERATURE)
        self._temperature = 20

    def set_value(self, temperature: int) -> None:
        if temperature < -50:
            raise SensorValueError("Температура слишком низкая.")
        elif temperature > 60:
            raise SensorValueError("Температура слишком высокая.")
        self._temperature = temperature

    def _calculate_temperature_level(self) -> TemperatureLevel:
        if self._temperature <= 10:
            return TemperatureLevel.VERY_COLD
        elif self._temperature <= 18:
            return TemperatureLevel.COLD
        elif self._temperature <= 24:
            return TemperatureLevel.COMFORTABLE
        elif self._temperature <= 30:
            return TemperatureLevel.WARM
        else:
            return TemperatureLevel.HOT

    def get_temperature(self) -> int:
        return self._temperature

    def get_status(self) -> TemperatureLevel:
        return self._calculate_temperature_level()


class HumiditySensor(Sensor):
    def __init__(self, temperature_sensor: TemperatureSensor) -> None:
        super().__init__("humid_", Domain.ECOLOGY, MeasurementType.HUMIDITY)
        self._vapor_concentration = 9.0  # Концентрация пара (г/м³)
        self._temperature_sensor = temperature_sensor  # Температура по умолчанию (°C)

    def set_value(self, concentration: float) -> None:
        """Устанавливает концентрацию водяного пара в г/м³"""
        if concentration < 0:
            raise SensorValueError("Концентрация пара не может быть отрицательной.")
        elif concentration > 100:
            raise SensorValueError("Концентрация пара слишком высокая.")

        self._vapor_concentration = concentration
        self._update_humidity()

    def _get_saturation_vapor_density(self) -> float:
        """
        Возвращает плотность насыщенного водяного пара при данной температуре.
        Формула на основе уравнения Арден-Бака (г/м³).
        """
        # Коэффициенты для расчёта давления насыщенного пара (в Па)
        t = self._temperature_sensor.get_temperature()
        if t >= 0:
            # Для положительных температур
            p_sat = 611.21 * math.exp((18.678 - t / 234.5) * (t / (257.14 + t)))
        else:
            # Для отрицательных температур
            p_sat = 611.15 * math.exp((23.036 - t / 333.7) * (t / (279.82 + t)))

        # Перевод давления в плотность (г/м³) через уравнение состояния идеального газа
        # ρ = (P * M) / (R * T)
        M = 18.01528  # Молярная масса воды (г/моль)
        R = 8.31446  # Универсальная газовая постоянная (Дж/(моль·К))
        T = t + 273.15  # Температура в Кельвинах

        density = (p_sat * M) / (R * T)
        return density

    def _update_humidity(self) -> None:
        """Пересчитывает относительную влажность на основе текущих данных"""
        saturation = self._get_saturation_vapor_density()

        if saturation > 0:
            self._humidity_percent = (self._vapor_concentration / saturation) * 100
            # Ограничиваем 100% (перенасыщение возможно, но для RH обычно обрезают)
            self._humidity_percent = min(100.0, max(0.0, self._humidity_percent))
        else:
            self._humidity_percent = 0.0

    def get_status(self) -> HumidityLevel:
        """Возвращает уровень влажности (1-5)"""
        return self._get_humidity_level()

    def get_humidity_percent(self) -> float:
        """Возвращает влажность в процентах (точное значение)"""
        return round(self._humidity_percent, 2)

    def _get_humidity_level(self) -> HumidityLevel:
        """Определяет уровень влажности по процентам"""
        if self._humidity_percent < 30:
            return HumidityLevel.VERY_DRY
        elif self._humidity_percent < 45:
            return HumidityLevel.DRY
        elif self._humidity_percent < 60:
            return HumidityLevel.COMFORTABLE
        elif self._humidity_percent < 75:
            return HumidityLevel.HUMID
        else:
            return HumidityLevel.VERY_HUMID


class NoiseSensor(Sensor):
    def __init__(self) -> None:
        super().__init__("noise_", Domain.ECOLOGY, MeasurementType.NOISE)
        self._decibels = 50.0  # Уровень шума в дБ

    def set_value(self, decibels: float) -> None:
        """Устанавливает уровень шума в децибелах"""
        if decibels < 0:
            raise SensorValueError("Уровень шума не может быть отрицательным.")
        elif decibels > 150:
            raise SensorValueError("Уровень шума слишком высокий.")
        self._decibels = decibels

    def _calculate_noise_level(self) -> NoiseLevel:
        """Определяет уровень шума на основе значений в дБ"""
        if self._decibels < 40:
            return NoiseLevel.QUIET
        elif self._decibels < 60:
            return NoiseLevel.MODERATE
        elif self._decibels < 80:
            return NoiseLevel.LOUD
        elif self._decibels < 100:
            return NoiseLevel.VERY_LOUD
        else:
            return NoiseLevel.DANGEROUS

    def get_status(self) -> NoiseLevel:
        """Возвращает числовой уровень шума (1-5)"""
        return self._calculate_noise_level()