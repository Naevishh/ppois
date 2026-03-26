from typing import Any

from ..city import SmartCity


class EnvironmentMonitoringUI:
    """UI модуль для мониторинга окружающей среды"""

    def __init__(self, city: SmartCity) -> None:
        self.city = city

    def get_environment_state(self) -> dict[str, Any]:
        """
        Получить состояние окружающей среды по всем датчикам города.
        :return: Словарь с результатами мониторинга
        """
        air, temp, humid, noise = [], [], [], []

        for dist in self.city.districts.values():
            air.extend(dist.air_quality_sensors)
            temp.extend(dist.temperature_sensors)
            humid.extend(dist.humidity_sensors)
            noise.extend(dist.noise_sensors)

        results = self.city.monitoring_system.environmental_monitoring_operation(
            air, temp, humid, noise
        )

        return results

    def format_environment_state(self, results: dict[str, Any]) -> str:
        """
        Отформатировать результаты для вывода.
        :param results: Словарь с результатами мониторинга
        :return: Отформатированная строка
        """
        output = (
            "Состояние окружающей среды:\n"
            f"Качество воздуха: {results['air']}.\n"
            f"Температура: {results['temperature']}.\n"
            f"Влажность: {results['humidity']}.\n"
            f"Шум: {results['noise']}."
        )
        return output

    def print_environment_state(self, print_func) -> None:
        """
        Получить и сразу вывести состояние среды (удобно для меню).
        :param print_func: Функция для вывода
        """
        results = self.get_environment_state()
        output = self.format_environment_state(results)
        print_func(output)