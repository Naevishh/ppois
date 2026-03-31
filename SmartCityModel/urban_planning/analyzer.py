from datetime import datetime

from ..core import PlanningMetricType
from .models import District


class UrbanPlanningDataAnalyzer:
    """
    Операция: Сбор и анализ данных для улучшения городской планировки.

    Агрегирует данные из:
    - EnvironmentMonitoringSystem (экология)
    - Сенсоров трафика

    Возвращает рекомендации по развитию районов.
    """

    def __init__(self) -> None:
        self.districts: dict[str, District] = {}

    def register_district(self, district: District) -> None:
        """Регистрация района для анализа"""
        self.districts[district.district_id] = district

    def calculate_metric(self, district_id: str, metric_type: PlanningMetricType, ecology=None) -> dict:
        """Расчёт конкретной метрики для района"""
        district = self.districts.get(district_id)
        if not district:
            return {"error": f"District {district_id} not found"}

        if metric_type == PlanningMetricType.ECOLOGY_SCORE:
            value = district.get_average("ecology_score")
            recommendation = self._get_ecology_recommendation(value)

        elif metric_type == PlanningMetricType.TRANSPORT_LOAD:
            value = district.get_average("transport_load")
            recommendation = self._get_transport_recommendation(value)

        elif metric_type == PlanningMetricType.INFRASTRUCTURE_DENSITY:
            value = district.get_average("infrastructure_density")
            recommendation = self._get_infrastructure_recommendation(value)

        else:
            # Композитный индекс: экология + транспорт + доступность сервисов
            eco = district.get_average("ecology_score") * 0.4
            transport = (100 - district.get_average("transport_load")) * 0.3
            services = district.get_average("infrastructure_density")
            value = eco + transport + services * 0.3
            recommendation = self._get_liveability_recommendation(value)

        return {
            "district_id": district_id,
            "metric": metric_type.value,
            "value": round(value, 2),
            "timestamp": datetime.now().isoformat(),
            "recommendation": recommendation
        }

    def _get_ecology_recommendation(self, score: float) -> str:
        if score >= 80:
            return "Экологическая обстановка отличная. Рекомендуется сохранить текущие зелёные зоны."
        elif score >= 60:
            return "Удовлетворительная экология. Рассмотреть высадку деревьев вдоль магистралей."
        elif score >= 40:
            return "Требуются меры: мониторинг выбросов, расширение парковых зон."
        else:
            return "Критическая экологическая обстановка. Необходима срочная программа озеленения и контроля загрязнений."

    def _get_transport_recommendation(self, load: float) -> str:
        if load <= 40:
            return "Транспортная нагрузка в норме. Можно рассмотреть развитие велодорожек."
        elif load <= 70:
            return "Средняя загруженность. Рекомендуется оптимизация светофоров и развитие общественного транспорта."
        else:
            return "Высокая транспортная нагрузка. Приоритет: разгрузка магистралей, строительство дублёров, развитие метро/трамвая."

    def _get_infrastructure_recommendation(self, density: float) -> str:
        if density <= 40:
            return "Низкая плотность застройки. Рекомендуется освоение территории или развитие базовой инфраструктуры."
        elif density <= 70:
            return "Умеренная плотность. Оптимальный баланс. Рекомендуется развитие социальной инфраструктуры (школы, поликлиники)."
        else:
            return "Высокая плотность застройки. Приоритет: модернизация коммунальных сетей, увеличение парковочных мест, озеленение."

    def _get_liveability_recommendation(self, index: float) -> str:
        if index >= 75:
            return "Район комфортен для проживания. Фокус на поддержании качества инфраструктуры."
        elif index >= 55:
            return "Средний уровень комфорта. Рекомендуется точечное улучшение экологии и транспорта."
        else:
            return "Низкий индекс комфорта. Требуется комплексная программа реновации района."

    def generate_planning_report(self, district_ids: list[str] = None) -> dict:
        """
        Генерация отчёта для градостроительного планирования.
        Возвращает структурированные данные + текстовые рекомендации.
        """
        if district_ids is None:
            district_ids = list(self.districts.keys())

        report = {
            "generated_at": datetime.now().isoformat(),
            "districts": []
        }

        for dist_id in district_ids:
            district_report = {
                "district_id": dist_id,
                "metrics": {}
            }
            for metric in PlanningMetricType:
                result = self.calculate_metric(dist_id, metric)
                if "error" not in result:
                    district_report["metrics"][metric.value] = result

            # Приоритет развития на основе худшей метрики
            priorities = [
                (m, data["value"])
                for m, data in district_report["metrics"].items()
                if m in [PlanningMetricType.ECOLOGY_SCORE.value,
                         PlanningMetricType.TRANSPORT_LOAD.value]
            ]
            if priorities:
                worst = min(priorities, key=lambda x: x[1] if "ecology" in x[0] else -x[1])
                district_report["development_priority"] = {
                    "focus_area": worst[0],
                    "current_value": worst[1],
                    "action": district_report["metrics"].get(worst[0], {}).get("recommendation")
                }

            report["districts"].append(district_report)

        return report