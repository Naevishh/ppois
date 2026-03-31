# SmartCityModel/ui/urban_planning_ui.py

from typing import Any
from ..city import SmartCity


class UrbanPlanningDataAnalysisUI:
    """UI модуль для анализа данных городского планирования"""

    def __init__(self, city: SmartCity) -> None:
        self.city = city

    def generate_report(self) -> dict[str, Any]:
        """
        Сгенерировать отчет по улучшению планировки районов.
        :return: Словарь с данными отчета
        """
        air, temp, humid, noise = [], [], [], []

        for dist in self.city.districts.values():
            air.extend(dist.air_quality_sensors)
            temp.extend(dist.temperature_sensors)
            humid.extend(dist.humidity_sensors)
            noise.extend(dist.noise_sensors)

        ecology=self.city.monitoring_system.environmental_monitoring_operation(air, temp, humid, noise)["average"]
        for dist in self.city.districts.values():
            dist.auto_collect_sensor_data(ecology)
        return self.city.analyzer.generate_planning_report()

    def format_report(self, report: dict[str, Any]) -> str:
        """
        Отформатировать отчет для вывода.
        :param report: Словарь с данными отчета
        :return: Отформатированная строка
        """
        lines = ["Отчет по улучшению планировки районов", f"Сгенерирован: {report['generated_at']}"]

        for district in report['districts']:
            lines.append(f"\nРайон: {district['district_id'].upper()}")

            lines.append("Метрики:")
            for metric_name, metric_data in district['metrics'].items():
                value = metric_data.get('value', 'N/A')
                lines.append(f" {metric_name}: {value}")

            if 'development_priority' in district:
                priority = district['development_priority']
                lines.append("\nПриоритет развития:")
                lines.append(f"\nПроблема: {priority['focus_area']}")
                lines.append(f"\nЗначение: {priority['current_value']}")
                lines.append("\nРекомендации:")
                for line in priority['action'].split('. '):
                    if line:
                        lines.append(f"      {line.strip()}")
            else:
                lines.append("\nНет данных для определения приоритетов")

        return "\n".join(lines)

    def print_report(self, print_func) -> None:
        """
        Сгенерировать и вывести отчет (удобно для меню).
        :param print_func: Функция для вывода
        """
        report = self.generate_report()
        output = self.format_report(report)
        print_func(output)