from ..city import SmartCity


class UrbanPlanningDataAnalysisUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city

    def print_report(self, print_func) -> None:
        """Красивый вывод отчёта в консоль"""
        report = self.city.analyzer.generate_planning_report()

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