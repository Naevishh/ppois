from ..city import SmartCity
from ..core import SensorValueError, VehicleType, show_menu
from ..core.utils import SafeInput, SENSOR_VALUE_VALIDATOR, NumberValidator
from ..sensors import AITrafficCamera

from typing import Optional, Dict, Any

class SensorUI:
    """UI модуль для управления сенсорами"""

    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.value_validator = SENSOR_VALUE_VALIDATOR
        self.camera_incident_validator = NumberValidator(min_value=1, max_value=2, allow_negative=False)

        # SmartCityModel/ui/sensors_ui.py (фрагмент)

    def set_smart_home_sensor(self, district_id: str, home_index: int,
                              sensor_type: str, value: int,
                              light_index: Optional[int] = None) -> str:
        """
        Установить значение сенсора умного дома.
        :param district_id: ID района
        :param home_index: Индекс умного дома в районе
        :param sensor_type: Тип сенсора (water, thermostat, light)
        :param value: Значение сенсора
        :param light_index: Индекс светильника (требуется только для типа 'light')
        :return: Сообщение о результате
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        if home_index < 0 or home_index >= len(dist.smart_homes):
            raise ValueError(f"Некорректный индекс дома: {home_index}")

        home = dist.smart_homes[home_index]

        if sensor_type == "water":
            home.water_meter.set_value(value)
            return "Значение счетчика воды установлено"

        elif sensor_type == "thermostat":
            home.thermostat.temp_sensor.set_value(value)
            return "Значение термостата установлено"

        elif sensor_type == "light":
            if light_index is None:
                raise ValueError("Для типа 'light' требуется параметр --light-index")

            if light_index < 0 or light_index >= len(home.lightning_system.smart_lights):
                raise ValueError(f"Некорректный индекс светильника: {light_index}")

            sensor = home.lightning_system.smart_lights[light_index].light_level_sensor
            sensor.set_value(value)
            return f"Значение сенсора светильника [{light_index}] установлено"

        else:
            raise ValueError(f"Неизвестный тип сенсора: {sensor_type}")

    def set_street_light_sensor(self, district_id: str, light_index: int,
                                value: int) -> str:
        """
        Установить значение сенсора уличного фонаря.
        :param district_id: ID района
        :param light_index: Индекс фонаря
        :param value: Значение уровня света
        :return: Сообщение о результате
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        if light_index < 0 or light_index >= len(dist.lights):
            raise ValueError(f"Некорректный индекс фонаря: {light_index}")

        dist.lights[light_index].light_level_sensor.set_value(value)
        return "Значение сенсора фонаря установлено"

    def set_generator_sensor(self, district_id: str, sensor_type: str,
                             value: int) -> str:
        """
        Установить значение сенсора генератора.
        :param district_id: ID района
        :param sensor_type: Тип (solar или wind)
        :param value: Значение
        :return: Сообщение о результате
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        if sensor_type == "solar":
            dist.generators[0].light_level_sensor.set_value(value)
            return "Значение сенсора солнечной панели установлено"
        elif sensor_type == "wind":
            dist.generators[1].set_value(value)
            return "Значение скорости ветра установлено"
        else:
            raise ValueError(f"Неизвестный тип генератора: {sensor_type}")

    def set_district_sensor(self, district_id: str, sensor_category: str,
                            sensor_index: int, value: int) -> str:
        """
        Установить значение сенсора района (воздух, температура, влажность, шум).
        :param district_id: ID района
        :param sensor_category: Категория (air, temperature, humidity, noise)
        :param sensor_index: Индекс сенсора
        :param value: Значение
        :return: Сообщение о результате
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        sensor_map = {
            "air": dist.air_quality_sensors,
            "temperature": dist.temperature_sensors,
            "humidity": dist.humidity_sensors,
            "noise": dist.noise_sensors
        }

        if sensor_category not in sensor_map:
            raise ValueError(f"Неизвестная категория: {sensor_category}")

        sensors = sensor_map[sensor_category]

        if sensor_index < 0 or sensor_index >= len(sensors):
            raise ValueError(f"Некорректный индекс сенсора: {sensor_index}")

        sensors[sensor_index].set_value(value)
        return f"Значение сенсора {sensor_category} установлено"

    def set_traffic_sensor(self, district_id: str, intersection_index: int,
                           light_device_id: str, sensor_type: str,
                           value: Any) -> str:
        """
        Установить значение сенсора транспорта на перекрестке.
        :param district_id: ID района
        :param intersection_index: Индекс перекрестка
        :param light_device_id: ID светофора
        :param sensor_type: Тип (camera, flow, pedestrian)
        :param value: Значение (для camera - кортеж (vehicle_type, is_incident))
        :return: Сообщение о результате
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        if intersection_index < 0 or intersection_index >= len(dist.intersections):
            raise ValueError(f"Некорректный индекс перекрестка: {intersection_index}")

        inter = dist.intersections[intersection_index]
        inter_lights = inter.lights

        if light_device_id not in inter_lights:
            raise ValueError(f"Светофор {light_device_id} не найден")

        light = inter_lights[light_device_id]

        if sensor_type == "camera":
            # value должен быть кортежем (VehicleType, is_incident)
            light.camera.detect_event(value[0], value[1])
            return "Событие камеры зафиксировано"
        elif sensor_type == "flow":
            light.flow_sensor.set_value(value)
            return "Значение потока транспорта установлено"
        elif sensor_type == "pedestrian":
            light.pedestrian_sensor.set_value(value)
            return "Значение сенсора пешеходов установлено"
        else:
            raise ValueError(f"Неизвестный тип сенсора: {sensor_type}")

    def detect_camera_event(self, camera: AITrafficCamera,
                            vehicle_type: VehicleType, is_incident: bool) -> str:
        """
        Зафиксировать событие на камере.
        :param camera: Объект камеры
        :param vehicle_type: Тип транспорта
        :param is_incident: Было ли ДТП
        :return: Сообщение о результате
        """
        camera.detect_event(vehicle_type, is_incident)
        return "Средство зафиксировано"

    def get_sensor_list(self, district_id: str, sensor_category: str) -> list[dict]:
        """
        Получить список сенсоров категории.
        :param district_id: ID района
        :param sensor_category: Категория сенсоров
        :return: Список словарей с информацией о сенсорах
        """
        if district_id not in self.city.districts:
            raise ValueError(f"Район {district_id} не найден")

        dist = self.city.districts[district_id]

        sensor_map = {
            "air": dist.air_quality_sensors,
            "temperature": dist.temperature_sensors,
            "humidity": dist.humidity_sensors,
            "noise": dist.noise_sensors,
            "lights": dist.lights,
            "smart_homes": dist.smart_homes
        }

        if sensor_category not in sensor_map:
            raise ValueError(f"Неизвестная категория: {sensor_category}")

        sensors = sensor_map[sensor_category]

        result = []
        for i, sensor in enumerate(sensors):
            sensor_data = {
                "index": i,
                "device_id": getattr(sensor, 'device_id', getattr(sensor, 'sensor_id', f'{sensor_category}_{i}')),
                "type": sensor_category
            }
            result.append(sensor_data)

        return result

    def get_district_list(self) -> list[str]:
        """
        Получить список ID районов.
        :return: Список ID районов
        """
        return list(self.city.districts.keys())

    def format_sensor_list(self, sensors: list[dict]) -> str:
        """Отформатировать список сенсоров"""
        if not sensors:
            return "Сенсоры не найдены"

        lines = []
        for sensor in sensors:
            lines.append(f"[{sensor['index']}] {sensor['device_id']} ({sensor['type']})")

        return "\n".join(lines)

    def format_district_list(self, districts: list[str]) -> str:
        """Отформатировать список районов"""
        if not districts:
            return "Районы не найдены"

        return "\n".join(f"[{i}] {d}" for i, d in enumerate(districts))