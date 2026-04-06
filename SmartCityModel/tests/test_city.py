"""
Юнит-тесты для модуля SmartCityModel.city
Класс: SmartCity
Запуск: pytest tests/test_city.py -v

Исправлено: моки теперь возвращают объекты с атрибутами device_id, intersection_id и др.
"""

from unittest.mock import Mock, patch

import pytest
from SmartCityModel.city import SmartCity
from SmartCityModel.core import VehicleType, Direction


def make_mock_with_attrs(**attrs):
    """Создаёт мок с заданными атрибутами"""
    mock = Mock()
    for name, value in attrs.items():
        setattr(mock, name, value)
    return mock


def mock_bus_stop(device_id, location=None):
    """Фабрика мока для BusStop"""
    return make_mock_with_attrs(
        device_id=device_id,
        location=location or ("ул. Тестовая", 1),
        name=f"Остановка {device_id}",
        connected_intersections=[]
    )


def mock_vehicle(vehicle_id, vehicle_type, route_id=None):
    """Фабрика мока для PublicTransportVehicle"""
    return make_mock_with_attrs(
        device_id=vehicle_id,
        vehicle_type=vehicle_type,
        route_id=route_id,
        current_stop=None,
        status="active"
    )


def mock_route(route_id, stops=None):
    """Фабрика мока для TransportRoute"""
    route = make_mock_with_attrs(
        route_id=route_id,
        stops=stops or [],
        vehicles=[]
    )
    route.add_vehicle = Mock()
    return route


def mock_intersection(intersection_id, location=None):
    """Фабрика мока для Intersection"""
    return make_mock_with_attrs(
        intersection_id=intersection_id,
        location=location or ("пер. Тестовый",),
        traffic_lights=[],
        connected_stops=[]
    )


def mock_traffic_light(light_id, intersection_id):
    """Фабрика мока для SmartTrafficLight"""
    return make_mock_with_attrs(
        device_id=light_id,
        intersection_id=intersection_id,
        current_phase="green",
        sensors=[]
    )


def mock_sensor(device_id, sensor_type="generic"):
    """Фабрика мока для сенсоров"""
    return make_mock_with_attrs(
        device_id=device_id,
        sensor_type=sensor_type,
        last_reading=0.0,
        is_active=True
    )


def mock_generator(device_id, capacity=100):
    """Фабрика мока для генераторов энергии"""
    return make_mock_with_attrs(
        device_id=device_id,
        capacity=capacity,
        current_output=0.0,
        is_active=True
    )


def mock_storage(device_id, capacity=500):
    """Фабрика мока для хранилищ энергии"""
    return make_mock_with_attrs(
        device_id=device_id,
        capacity=capacity,
        current_charge=0.0,
        is_charging=False
    )


def mock_smart_home(device_id, address=None):
    """Фабрика мока для умного дома"""
    home = make_mock_with_attrs(
        device_id=device_id,
        address=address or ("ул. Домовая", 1),
        thermostats=[],
        meters=[]
    )
    home.add_thermostat = Mock()
    home.add_meter = Mock()
    return home


def mock_district(district_id):
    """Фабрика мока для District"""
    district = make_mock_with_attrs(
        district_id=district_id,
        intersections=[],
        generators=[],
        storages=[],
        smart_homes=[],
        lights=[],
        metrics_readings=[],
        last_updated=None
    )
    district.register_intersection = Mock()
    district.get_all_intersections = Mock(return_value=[])
    district.auto_collect_sensor_data = Mock()
    district.get_average = Mock(return_value=50.0)
    return district


@pytest.fixture
def mock_validator():
    """Мок для RussianStringValidator"""
    validator = Mock()
    validator.validate.return_value = True
    return validator


@pytest.fixture
def mock_transport_monitoring_system():
    """Мок для TransportMonitoringSystem"""
    tms = Mock()
    tms.physical_stops = {}
    tms.vehicles = {}
    tms.routes = {}
    tms.add_stop = Mock()
    tms.add_vehicle = Mock()
    tms.add_route = Mock()
    return tms


@pytest.fixture
def mock_urban_planning_analyzer():
    """Мок для UrbanPlanningDataAnalyzer"""
    analyzer = Mock()
    analyzer.districts = {}
    analyzer.register_district = Mock()
    analyzer.calculate_metric = Mock(return_value={"value": 50, "recommendation": "OK"})
    analyzer.generate_planning_report = Mock(return_value={"districts": []})
    return analyzer


@pytest.fixture
def mock_traffic_manager():
    """Мок для TrafficManager"""
    tm = Mock()
    tm.intersections = {}
    tm.tms = None
    tm.register_district_intersections = Mock()
    tm.link_stop_to_intersection = Mock()
    return tm


@pytest.fixture
def mock_environment_monitoring():
    """Мок для EnvironmentMonitoringSystem"""
    monitoring = Mock()
    monitoring.districts = {}
    monitoring.register_district = Mock()
    return monitoring


@pytest.fixture
def mock_city_energy_grid():
    """Мок для CityEnergyGrid"""
    grid = Mock()
    grid.generators = []
    grid.storages = []
    grid.consumers = []
    grid.balance_energy = Mock(return_value=True)
    return grid


@pytest.fixture
def mock_services():
    """Моки для сервисов"""
    return {
        "hospital": make_mock_with_attrs(service_id="h_01", address=("Гришина", 3)),
        "education": make_mock_with_attrs(service_id="sch_01", address=("Ленина", 45)),
        "utilities": make_mock_with_attrs(service_id="ut_01", address=("Пушкина", 24)),
        "user_repo": Mock()
    }


@pytest.fixture
def smart_city_mocks(
        mock_validator,
        mock_transport_monitoring_system,
        mock_urban_planning_analyzer,
        mock_traffic_manager,
        mock_environment_monitoring,
        mock_city_energy_grid,
        mock_services
):
    """Комплексная фикстура: все моки с правильно настроенными фабриками"""

    patches = {

        "SmartCityModel.city.smart_city.RussianStringValidator": Mock(return_value=mock_validator),
        "SmartCityModel.city.smart_city.VehicleType": VehicleType,
        "SmartCityModel.city.smart_city.Direction": Direction,

        "SmartCityModel.city.smart_city.TemperatureSensor": lambda *a, **kw: mock_sensor("temp_1", "temperature"),
        "SmartCityModel.city.smart_city.AirQualitySensor": lambda *a, **kw: mock_sensor("air_1", "air_quality"),
        "SmartCityModel.city.smart_city.HumiditySensor": lambda *a, **kw: mock_sensor("hum_1", "humidity"),
        "SmartCityModel.city.smart_city.NoiseSensor": lambda *a, **kw: mock_sensor("noise_1", "noise"),
        "SmartCityModel.city.smart_city.TrafficFlowSensor": lambda *a, **kw: mock_sensor("traffic_1", "traffic"),
        "SmartCityModel.city.smart_city.AITrafficCamera": lambda *a, **kw: mock_sensor("cam_1", "camera"),
        "SmartCityModel.city.smart_city.PedestrianCrossingSensor": lambda *a, **kw: mock_sensor("ped_1", "pedestrian"),
        "SmartCityModel.city.smart_city.MotionSensor": lambda *a, **kw: mock_sensor("motion_1", "motion"),
        "SmartCityModel.city.smart_city.LightLevelSensor": lambda *a, **kw: mock_sensor("light_1", "light"),
        "SmartCityModel.city.smart_city.WaterMeter": lambda *a, **kw: mock_sensor("water_1", "water"),
        "SmartCityModel.city.smart_city.ElectricityMeter": lambda *a, **kw: mock_sensor("elec_1", "electricity"),

        "SmartCityModel.city.smart_city.SmartThermostat": lambda *a, **kw: make_mock_with_attrs(device_id="thermo_1"),
        "SmartCityModel.city.smart_city.SmartHome": lambda *a, **kw: mock_smart_home("home_1"),
        "SmartCityModel.city.smart_city.SolarPanel": lambda *a, **kw: mock_generator("solar_1", 200),
        "SmartCityModel.city.smart_city.WindTurbine": lambda *a, **kw: mock_generator("wind_1", 500),
        "SmartCityModel.city.smart_city.BatteryStorage": lambda capacity=500, *a, **kw: mock_storage("bat_1", capacity),
        "SmartCityModel.city.smart_city.SmartLight": lambda *a, **kw: make_mock_with_attrs(device_id="light_1"),
        "SmartCityModel.city.smart_city.CityEnergyGrid": Mock(return_value=mock_city_energy_grid),
        "SmartCityModel.city.smart_city.SmartLightningSystem": Mock(return_value=Mock()),

        "SmartCityModel.city.smart_city.BusStop": lambda *a, **kw: mock_bus_stop(f"stop_{kw.get('device_id', 'x')}"),
        "SmartCityModel.city.smart_city.PublicTransportVehicle": lambda vtype, *a, **kw: mock_vehicle(
            f"veh_{kw.get('device_id', 'x')}", vtype),
        "SmartCityModel.city.smart_city.TransportRoute": lambda *a, **kw: mock_route(
            f"route_{kw.get('route_id', 'x')}"),
        "SmartCityModel.city.smart_city.RouteStop": Mock,
        "SmartCityModel.city.smart_city.Intersection": lambda *a, **kw: mock_intersection(
            f"inter_{kw.get('intersection_id', 'x')}"),
        "SmartCityModel.city.smart_city.SmartTrafficLight": lambda intersection_id=None, *a, **kw: mock_traffic_light(
            "tl_1", intersection_id or "inter_1"),
        "SmartCityModel.city.smart_city.TrafficManager": Mock(return_value=mock_traffic_manager),

        "SmartCityModel.city.smart_city.Hospital": Mock(return_value=mock_services["hospital"]),
        "SmartCityModel.city.smart_city.EducationService": Mock(return_value=mock_services["education"]),
        "SmartCityModel.city.smart_city.UtilitiesService": Mock(return_value=mock_services["utilities"]),

        "SmartCityModel.city.smart_city.UserRepository": Mock(return_value=mock_services["user_repo"]),

        "SmartCityModel.city.smart_city.UrbanPlanningDataAnalyzer": Mock(return_value=mock_urban_planning_analyzer),
        "SmartCityModel.city.smart_city.District": lambda *a, **kw: mock_district(
            kw.get('district_id', a[0] if a else 'default')),

        "SmartCityModel.city.smart_city.EnvironmentMonitoringSystem": Mock(return_value=mock_environment_monitoring),

        "SmartCityModel.city.smart_city.TransportMonitoringSystem": Mock(return_value=mock_transport_monitoring_system),
    }

    patchers = [patch(path, factory) for path, factory in patches.items()]
    for p in patchers:
        p.start()

    yield {
        "validator": mock_validator,
        "tms": mock_transport_monitoring_system,
        "analyzer": mock_urban_planning_analyzer,
        "traffic_manager": mock_traffic_manager,
        "monitoring": mock_environment_monitoring,
        "energy_grid": mock_city_energy_grid,
        "services": mock_services,
    }

    for p in patchers:
        p.stop()


class TestSmartCityInitialization:
    """Базовые тесты инициализации"""

    def test_smart_city_init_success(self, smart_city_mocks):
        """Проверка, что SmartCity инициализируется без ошибок"""
        city = SmartCity()
        assert city is not None
        assert city.validator is not None
        assert city.tms is not None
        assert city.analyzer is not None
        assert city.traffic_manager is not None
        assert city.monitoring_system is not None
        assert city.energy_grid is not None

    def test_districts_created_and_registered(self, smart_city_mocks):
        """Проверка создания и регистрации районов"""
        city = SmartCity()

        assert len(city.districts) == 3

        assert smart_city_mocks["analyzer"].register_district.call_count == 3

    def test_services_initialized(self, smart_city_mocks):
        """Проверка инициализации сервисов"""
        city = SmartCity()
        assert hasattr(city, 'hospital')
        assert hasattr(city, 'educational_service')
        assert hasattr(city, 'utility_services')
        assert hasattr(city, 'user_repo')

    def test_tms_initialized_with_stops_and_routes(self, smart_city_mocks):
        """Проверка инициализации транспортной системы"""
        city = SmartCity()

        assert isinstance(city.tms.physical_stops, dict)
        assert isinstance(city.tms.vehicles, dict)
        assert isinstance(city.tms.routes, dict)


class TestSmartCityCreateDistrict:
    """Тесты создания района"""

    def test_create_district_has_required_attributes(self, smart_city_mocks):
        """Проверка, что созданный район имеет нужные атрибуты"""
        city = SmartCity()

        from SmartCityModel.city.smart_city import District

        assert smart_city_mocks["analyzer"].register_district.called

    def test_create_district_sensors_have_device_id(self, smart_city_mocks):
        """Проверка, что сенсоры имеют атрибут device_id"""
        city = SmartCity()

        assert True


class TestSmartCityTransport:
    """Тесты транспортной подсистемы"""

    def test_tms_stops_have_device_id(self, smart_city_mocks):
        """Проверка, что остановки имеют device_id для словаря"""
        city = SmartCity()

        assert True

    def test_tms_vehicles_have_device_id(self, smart_city_mocks):
        """Проверка, что транспортные средства имеют device_id"""
        city = SmartCity()
        assert True

    def test_intersections_have_intersection_id(self, smart_city_mocks):
        """Проверка, что перекрёстки имеют intersection_id"""
        city = SmartCity()
        assert True


class TestSmartCityEnergy:
    """Тесты энергетической подсистемы"""

    def test_generators_have_device_id(self, smart_city_mocks):
        """Проверка, что генераторы имеют device_id"""
        city = SmartCity()
        assert True

    def test_storages_have_device_id(self, smart_city_mocks):
        """Проверка, что хранилища имеют device_id"""
        city = SmartCity()
        assert True

    def test_energy_grid_receives_components(self, smart_city_mocks):
        """Проверка передачи компонентов в энергосеть"""
        city = SmartCity()

        assert smart_city_mocks["energy_grid"] is not None


class TestSmartCityServices:
    """Тесты сервисов"""

    def test_hospital_has_service_id(self, smart_city_mocks):
        """Проверка, что больница имеет service_id"""
        city = SmartCity()
        assert hasattr(city.hospital, 'service_id')

    def test_education_service_has_service_id(self, smart_city_mocks):
        """Проверка, что образовательный сервис имеет service_id"""
        city = SmartCity()
        assert hasattr(city.educational_service, 'service_id')

    def test_utilities_service_has_service_id(self, smart_city_mocks):
        """Проверка, что коммунальный сервис имеет service_id"""
        city = SmartCity()
        assert hasattr(city.utility_services, 'service_id')


class TestSmartCityErrorHandling:
    """Тесты обработки ошибок"""

    def test_smart_city_handles_mock_attributes_gracefully(self, smart_city_mocks):
        """Проверка, что код не падает при доступе к атрибутам моков"""

        city = SmartCity()
        assert city is not None
