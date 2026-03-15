from environment import EnvironmentMonitoringSystem
from sensors import AirQualitySensor, TemperatureSensor, TrafficFlowSensor, HumiditySensor, NoiseSensor
from . import UrbanPlanningDataAnalyzer, District


class UrbanPlanningDataAnalysisUI:
    def __init__(self, ):
        self.analyzer = self._build_analyzer()

    def _build_analyzer(self) -> UrbanPlanningDataAnalyzer:
        """Factory method: создаёт анализатор и регистрирует 3 района."""
        analyzer = UrbanPlanningDataAnalyzer()

        # Конфигурация районов: [id, sensor_count]
        districts_config = [
            ("center_1", 3),
            ("center_2", 2),
            ("suburb_1", 2),
        ]

        for district_id, sensor_count in districts_config:
            district = self._create_district(district_id, sensor_count)
            analyzer.register_district(district)

        return analyzer

    def _create_district(self, district_id: str, sensor_count: int) -> District:
        """
        Создаёт и настраивает один район с сенсорами и системой эко-мониторинга.

        Args:
            district_id: Уникальный идентификатор района
            sensor_count: Количество транспортных сенсоров в районе
        """

        traffic_sensors = [
            TrafficFlowSensor()
            for _ in range(sensor_count)
        ]

        temp_sensors = [TemperatureSensor() for _ in range(2)]
        air_sensors = [AirQualitySensor() for _ in range(2)]

        # Влажность привязываем к температурным сенсорам
        humidity_sensors = [
            HumiditySensor(temp_sensor) for temp_sensor in temp_sensors
        ]

        noise_sensors = [NoiseSensor() for _ in range(2)]

        env_system = EnvironmentMonitoringSystem(
            air_sensors,
            temp_sensors,
            humidity_sensors,
            noise_sensors,
        )

        return District(district_id, env_system, traffic_sensors)

    def print_report(self, print_func):
        """Красивый вывод отчёта в консоль"""
        report = self.analyzer.generate_planning_report()

        print_func(f"Отчет по улучшению планировки районов")
        print_func(f"Сгенерирован: {report['generated_at']}")

        for district in report['districts']:
            print_func(f"\nРайон: {district['district_id'].upper()}")

            print_func("Метрики:")
            for metric_name, metric_data in district['metrics'].items():
                value = metric_data.get('value', 'N/A')
                # Добавляем цветовой индикатор (условно)
                print_func(f" {metric_name}: {value}")

            if 'development_priority' in district:
                priority = district['development_priority']
                print_func("\nПриоритет развития:")
                print_func(f"\nПроблема: {priority['focus_area']}")
                print_func(f"\nЗначение: {priority['current_value']}")
                print_func(f"\nРекомендации:")
                # Делаем отступ для текста рекомендации
                for line in priority['action'].split('. '):
                    if line:
                        print_func(f"      {line.strip()}.")
            else:
                print_func("\nНет данных для определения приоритетов")
