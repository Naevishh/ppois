"""
Юнит-тесты для модуля SmartCityModel.urban_planning
Запуск: pytest tests/test_urban_planning.py -v
"""

from datetime import datetime
from unittest.mock import Mock

import pytest
from SmartCityModel.core import PlanningMetricType
from SmartCityModel.urban_planning import District, UrbanPlanningDataAnalyzer


@pytest.fixture
def mock_sensor():
    """Создаёт мок-сенсор с методом get_status()"""
    sensor = Mock()
    sensor.get_status.return_value = 50.0
    return sensor


@pytest.fixture
def mock_intersection():
    """Создаёт мок перекрёстка"""
    return Mock()


@pytest.fixture
def mock_smart_home():
    """Создаёт мок умного дома"""
    return Mock()


@pytest.fixture
def mock_light():
    """Создаёт мок умного света"""
    return Mock()


@pytest.fixture
def mock_storage():
    """Создаёт мок батареи"""
    return Mock()


@pytest.fixture
def district(mock_sensor, mock_intersection, mock_smart_home, mock_light, mock_storage):
    """Фикстура: экземпляр District с мокированными зависимостями"""
    return District(
        district_id="test_district_001",
        air_quality_sensors=[mock_sensor],
        temperature_sensors=[mock_sensor],
        humidity_sensors=[mock_sensor],
        noise_sensors=[mock_sensor],
        traffic_sensors=[mock_sensor],
        intersections=[mock_intersection],
        smart_homes=[mock_smart_home],
        lights=[mock_light],
        storages=[mock_storage],
        generators=[]
    )


@pytest.fixture
def analyzer():
    """Фикстура: экземпляр UrbanPlanningDataAnalyzer"""
    return UrbanPlanningDataAnalyzer()


class TestDistrict:
    """Тесты для класса District"""

    def test_district_initialization(self, district):
        """Проверка корректной инициализации района"""
        assert district.district_id == "test_district_001"
        assert district.metrics_readings == []
        assert district.last_updated is None
        assert len(district.get_all_intersections()) == 1

    def test_register_intersection(self, district, mock_intersection):
        """Проверка добавления перекрёстка"""
        initial_count = len(district.get_all_intersections())
        district.register_intersection(mock_intersection)
        assert len(district.get_all_intersections()) == initial_count + 1

    def test_auto_collect_sensor_data(self, district):
        """Проверка сбора данных с сенсоров"""
        ecology_value = 4.5
        district.auto_collect_sensor_data(ecology_value)

        assert len(district.metrics_readings) == 1
        reading = district.metrics_readings[0]

        assert reading["ecology_score"] == ecology_value * 20
        assert reading["transport_load"] == 50.0
        assert reading["infrastructure_density"] == 70
        assert district.last_updated is not None
        assert isinstance(district.last_updated, datetime)

    def test_get_average_with_data(self, district):
        """Проверка расчёта среднего значения при наличии данных"""
        district.metrics_readings = [
            {"ecology_score": 80, "transport_load": 40},
            {"ecology_score": 90, "transport_load": 60},
        ]

        assert district.get_average("ecology_score") == 85.0
        assert district.get_average("transport_load") == 50.0

    def test_get_average_empty(self, district):
        """Проверка возврата None при отсутствии данных"""
        assert district.get_average("ecology_score") is None

    def test_get_average_invalid_metric(self, district):
        """Проверка обработки несуществующей метрики"""
        district.metrics_readings = [{"ecology_score": 80}]
        with pytest.raises(KeyError):
            district.get_average("nonexistent_metric")


class TestUrbanPlanningDataAnalyzer:
    """Тесты для класса UrbanPlanningDataAnalyzer"""

    def test_init_empty(self, analyzer):
        """Проверка инициализации пустого анализатора"""
        assert analyzer.districts == {}

    def test_register_district(self, analyzer, district):
        """Проверка регистрации района"""
        analyzer.register_district(district)
        assert district.district_id in analyzer.districts
        assert analyzer.districts[district.district_id] is district

    def test_calculate_metric_district_not_found(self, analyzer):
        """Проверка обработки несуществующего района"""
        result = analyzer.calculate_metric("unknown_district", PlanningMetricType.ECOLOGY_SCORE)
        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.parametrize("score,expected_keywords", [
        (85, ["отличная", "сохранить"]),
        (65, ["удовлетворительная", "деревьев"]),
        (45, ["меры", "мониторинг", "парковых"]),
        (30, ["критическая", "срочная", "озеленения"]),
    ])
    def test_ecology_recommendations(self, analyzer, district, score, expected_keywords):
        """Проверка рекомендаций по экологии для разных диапазонов"""
        analyzer.register_district(district)
        district.metrics_readings = [{"ecology_score": score}]

        result = analyzer.calculate_metric(
            district.district_id,
            PlanningMetricType.ECOLOGY_SCORE
        )

        assert result["metric"] == PlanningMetricType.ECOLOGY_SCORE.value
        assert result["value"] == score
        assert all(keyword in result["recommendation"].lower() for keyword in expected_keywords)

    @pytest.mark.parametrize("load,expected_keywords", [
        (30, ["норме", "велодорожек"]),
        (55, ["средняя", "светофоров", "общественного транспорта"]),
        (80, ["высокая", "разгрузка", "метро"]),
    ])
    def test_transport_recommendations(self, analyzer, district, load, expected_keywords):
        """Проверка рекомендаций по транспортной нагрузке"""
        analyzer.register_district(district)
        district.metrics_readings = [{"transport_load": load}]

        result = analyzer.calculate_metric(
            district.district_id,
            PlanningMetricType.TRANSPORT_LOAD
        )

        assert result["value"] == load
        assert all(keyword in result["recommendation"].lower() for keyword in expected_keywords)

    @pytest.mark.parametrize("density,expected_keywords", [
        (30, ["низкая", "освоение", "базовой инфраструктуры"]),
        (55, ["умеренная", "баланс", "социальной инфраструктуры"]),
        (85, ["высокая", "модернизация", "парковочных"]),
    ])
    def test_infrastructure_recommendations(self, analyzer, district, density, expected_keywords):
        """Проверка рекомендаций по плотности застройки"""
        analyzer.register_district(district)
        district.metrics_readings = [{"infrastructure_density": density}]

        result = analyzer.calculate_metric(
            district.district_id,
            PlanningMetricType.INFRASTRUCTURE_DENSITY
        )

        assert result["value"] == density
        assert all(keyword in result["recommendation"].lower() for keyword in expected_keywords)

    def test_calculate_composite_metric(self, analyzer, district):
        """Проверка расчёта композитного индекса комфорта"""
        analyzer.register_district(district)
        district.metrics_readings = [{
            "ecology_score": 80,
            "transport_load": 40,
            "infrastructure_density": 70
        }]

        result = analyzer.calculate_metric(
            district.district_id,
            Mock(value="composite")
        )

        expected = 80 * 0.4 + (100 - 40) * 0.3 + 70 * 0.3
        assert abs(result["value"] - expected) < 0.01

    def test_generate_planning_report_single_district(self, analyzer, district):
        """Проверка генерации отчёта для одного района"""
        analyzer.register_district(district)
        district.metrics_readings = [
            {"ecology_score": 70, "transport_load": 50, "infrastructure_density": 60}
        ]

        report = analyzer.generate_planning_report()

        assert "generated_at" in report
        assert len(report["districts"]) == 1
        district_report = report["districts"][0]
        assert district_report["district_id"] == district.district_id
        assert "metrics" in district_report
        assert "development_priority" in district_report

    def test_generate_planning_report_specific_districts(self, analyzer, district):
        """Проверка генерации отчёта для указанных районов"""
        district2 = Mock(district_id="district_002", metrics_readings=[], get_average=Mock(return_value=50))
        district.get_average = Mock(return_value=50)
        analyzer.register_district(district)
        analyzer.register_district(district2)

        report = analyzer.generate_planning_report(district_ids=["test_district_001"])

        assert len(report["districts"]) == 1
        assert report["districts"][0]["district_id"] == "test_district_001"

    def test_result_structure(self, analyzer, district):
        """Проверка структуры возвращаемого результата calculate_metric"""
        analyzer.register_district(district)
        district.metrics_readings = [{"ecology_score": 75}]

        result = analyzer.calculate_metric(
            district.district_id,
            PlanningMetricType.ECOLOGY_SCORE
        )

        required_keys = {"district_id", "metric", "value", "timestamp", "recommendation"}
        assert required_keys.issubset(result.keys())
        assert isinstance(result["value"], (int, float))
        assert isinstance(result["timestamp"], str)
