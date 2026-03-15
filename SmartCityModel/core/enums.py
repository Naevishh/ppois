from enum import Enum


class Domain(Enum):
    TRANSPORTATION = "transportation"
    ECOLOGY = "ecology"  # ENVIRONMENT = "environment"
    INFRASTRUCTURE = "infrastructure"
    SAFETY = "safety"  # SECURITY = "security"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    HOUSING = "housing"


class VehicleType(Enum):
    CAR = "car"
    BUS = "bus"
    TRAM = "tram"
    TROLLEYBUS = "trolleybus"
    TRUCK = "truck"
    AMBULANCE = "ambulance"
    FIRE_TRUCK = "fire_truck"
    POLICE = "police"
    BICYCLE = "bicycle"
    MOTORCYCLE = "motorcycle"


class LabeledEnum(Enum):
    """Базовый класс для Enum с кодом и меткой"""

    def __init__(self, code, label):
        self.code = code
        self.label = label

    @classmethod
    def from_code(cls, code):
        for level in cls:
            if level.code == code:
                return level
        raise ValueError(f"Нет элемента {cls.__name__} с кодом {code}")

    @classmethod
    def from_label(cls, label):
        for level in cls:
            if level.label == label:
                return level
        raise ValueError(f"Нет элемента {cls.__name__} с меткой '{label}'")


class AirQualityLevel(LabeledEnum):
    EXCELLENT = (1, "отличное")
    GOOD = (2, "хорошее")
    MODERATE = (3, "умеренное")
    POOR = (4, "плохое")
    HAZARDOUS = (5, "ужасное")


class TemperatureLevel(LabeledEnum):
    VERY_COLD = (1, "Очень холодно")
    COLD = (2, "Холодно")
    COMFORTABLE = (3, "Комфортно")
    WARM = (4, "Тепло")
    HOT = (5, "Жарко")


class HumidityLevel(LabeledEnum):
    """Уровни влажности для удобства оценки"""
    VERY_DRY = (1, "Очень сухо")  # < 30%
    DRY = (2, "Сухо")  # 30-45%
    COMFORTABLE = (3, "Комфортно")  # 45-60%
    HUMID = (4, "Влажно")  # 60-75%
    VERY_HUMID = (5, "Очень влажно")


class NoiseLevel(LabeledEnum):
    """Уровни шума по степени воздействия на человека"""
    QUIET = (1, "Тишина")  # < 40 дБ
    MODERATE = (2, "Нормальный")  # 40-60 дБ
    LOUD = (3, "Шумный")  # 60-80 дБ
    VERY_LOUD = (4, "Очень шумный")  # 80-100 дБ
    DANGEROUS = (5, "Опасный")


class PlanningMetricType(Enum):
    """Типы метрик для городского планирования"""
    ECOLOGY_SCORE = "ecology_score"  # Комплексный экологический рейтинг
    TRANSPORT_LOAD = "transport_load"  # Загруженность транспортной сети
    INFRASTRUCTURE_DENSITY = "infrastructure_density"  # Плотность сервисов
    LIVEABILITY_INDEX = "liveability_index"  # Индекс комфорта проживания


class MeasurementType(Enum):
    OCCUPANCY = "occupancy"
    DISTANCE = "distance"
    AIR_QUALITY = "air_quality"
    TRAFFIC_INTENSITY = "traffic_intensity"
    LOCATION = "location"
    VIDEO_ANALYTICS = "video_analytics"
    VEHICLE_PRESENCE = "vehicle_presence"
    LIGHT = "light"
    MOTION = "motion"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    GAS = "gas"
    NOISE = "noise"
    CONCENTRATION = "concentration"


class TrafficLightColor(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
