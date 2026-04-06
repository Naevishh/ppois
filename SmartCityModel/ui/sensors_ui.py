from typing import Optional, Any

from ..city import SmartCity
from ..core import VehicleType
from ..core.utils import SENSOR_VALUE_VALIDATOR, NumberValidator
from ..sensors import AITrafficCamera


class SensorUI:
    """UI модуль для управления сенсорами"""

    def __init__(self, city: SmartCity) -> None:
        self.city = city
        self.value_validator = SENSOR_VALUE_VALIDATOR
        self.camera_incident_validator = NumberValidator(min_value=1, max_value=2, allow_negative=False)

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
        light = None
        for l in inter.lights.keys():
            if l.device_id == light_device_id:
                light = l

        if not light:
            raise ValueError(f"Светофор {light_device_id} не найден")

        if sensor_type == "camera":

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
            "smart_homes": dist.smart_homes,
            "traffic": dist.intersections
        }

        if sensor_category not in sensor_map:
            raise ValueError(f"Неизвестная категория: {sensor_category}")

        sensors = sensor_map[sensor_category]
        result = []

        if sensor_category == "smart_homes":
            for i, home in enumerate(sensors):
                adr = f"{home.address[0]} {home.address[1]}"

                water_meter_id = getattr(home.water_meter, 'device_id', f"Home_{i}_Water")
                result.append({
                    "index": i,
                    "device_id": f"{water_meter_id}",
                    "type": "water",
                    "description": f"Счетчик воды ({adr})"
                })

                thermo_sensor_id = getattr(home.thermostat.temp_sensor, 'sensor_id', f"Thermo_{i}_Temp")
                result.append({
                    "index": i,
                    "device_id": thermo_sensor_id,
                    "type": "thermostat_temp",
                    "description": f"Термостат ({adr})"
                })

                if hasattr(home, 'lightning_system') and hasattr(home.lightning_system, 'smart_lights'):
                    for l_idx, light in enumerate(home.lightning_system.smart_lights):
                        light_sensor = light.light_level_sensor
                        light_id = getattr(light_sensor, 'sensor_id', f"Light_{i}_{l_idx}")
                        result.append({
                            "index": i,
                            "light_index": l_idx,
                            "device_id": light_id,
                            "type": "light",
                            "description": f"Светильник {l_idx} ({adr})"
                        })
            return result


        elif sensor_category == "traffic":
            for i, intersection in enumerate(sensors):

                if hasattr(intersection, 'lights'):
                    for light in intersection.lights.keys():
                        result.append({
                            "intersection_index": i,
                            "light_device_id": light.device_id,
                            "device_id": light.camera.sensor_id,
                            "type": "camera",
                            "description": f"Камера перекрестка {i}"
                        })

                        result.append({
                            "intersection_index": i,
                            "light_device_id": light.device_id,
                            "device_id": light.flow_sensor.sensor_id,
                            "type": "flow",
                            "description": f"Датчик потока перекрестка {i}"
                        })

                        result.append({
                            "intersection_index": i,
                            "light_device_id": light.device_id,
                            "device_id": light.pedestrian_sensor.sensor_id,
                            "type": "pedestrian",
                            "description": f"Датчик пешеходов перекрестка {i}"
                        })
            return result


        else:
            for i, sensor in enumerate(sensors):
                dev_id = getattr(sensor, 'device_id', getattr(sensor, 'sensor_id', f'{sensor_category}_{i}'))
                sensor_data = {
                    "index": i,
                    "device_id": dev_id,
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
        """Отформатировать список сенсоров для вывода пользователю"""
        if not sensors:
            return "Сенсоры не найдены"

        lines = []
        for sensor in sensors:

            index = sensor.get('index')
            device_id = sensor.get('device_id', 'N/A')
            sensor_type = sensor.get('type', 'unknown')

            if index is not None:
                line = f"[{index}] {device_id} ({sensor_type})"
            else:

                line = f"{device_id} ({sensor_type})"

            if 'light_index' in sensor:
                line += f" [светильник  

            if 'intersection_index' in sensor:
                line += f" [перекресток  

            if 'light_device_id' in sensor:
                line += f" [светофор {sensor['light_device_id']}]"

            lines.append(line)

        return "\n".join(lines)

    def format_district_list(self, districts: list[str]) -> str:
        """Отформатировать список районов"""
        if not districts:
            return "Районы не найдены"

        return "\n".join(f"[{i}] {d}" for i, d in enumerate(districts))
