"""
Юнит-тесты для всех классов модуля ui.
Запуск: python -m unittest tests.test_ui -v
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from SmartCityModel.ui.city_ui import CityUI
from SmartCityModel.ui.services_ui import PublicServiceUI
from SmartCityModel.ui.transport_ui import TransportSystemUI, TrafficManagementUI
from SmartCityModel.ui.sensors_ui import SensorUI
from SmartCityModel.ui.energy_ui import EnergyUI
from SmartCityModel.ui.environment_ui import EnvironmentMonitoringUI
from SmartCityModel.ui.urban_planning_ui import UrbanPlanningDataAnalysisUI
from SmartCityModel.core import Domain, VehicleType, TrafficLightColor, SensorValueError
from SmartCityModel.citizens import Human
from SmartCityModel.sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor


class TestPublicServiceUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_user_repo = Mock()
        self.mock_hospital = Mock()
        self.mock_edu = Mock()
        self.mock_utility = Mock()

        self.mock_city.user_repo = self.mock_user_repo
        self.mock_city.hospital = self.mock_hospital
        self.mock_city.educational_service = self.mock_edu
        self.mock_city.utility_services = self.mock_utility

        self.ui = PublicServiceUI(self.mock_city)

        self.ui.name_validator.validate = Mock(return_value=True)
        self.ui.age_validator.validate = Mock(return_value=True)
        self.ui.address_validator.validate = Mock(return_value=True)
        self.ui.house_validator.validate = Mock(return_value=True)

    def test_init_attributes(self):
        """Проверка инициализации атрибутов."""
        self.assertIs(self.ui.city, self.mock_city)
        self.assertIsNone(self.ui.current_user_id)
        self.assertIn("hospital", str(self.ui.available_actions))

    def test_register_user_success(self):
        """Успешная регистрация пользователя."""
        user_id = self.ui.register_user(
            name="Анна", surname="Петрова", age=25,
            street="Ленина", house=10, apartment=5
        )

        self.assertIsNotNone(user_id)
        self.assertEqual(len(user_id), 6)
        self.mock_user_repo.add_user.assert_called_once()

        call_args = self.mock_user_repo.add_user.call_args[0][0]
        self.assertIsInstance(call_args, Human)
        self.assertEqual(call_args.name, "Анна")

    def test_register_user_invalid_name(self):
        """Регистрация с некорректным именем."""
        self.ui.name_validator.validate = Mock(return_value=False)

        with self.assertRaises(ValueError) as context:
            self.ui.register_user(name="123", surname="Петров", age=30,
                                  street="Ленина", house=5)
        self.assertIn("Некорректное имя", str(context.exception))

    def test_register_user_invalid_age(self):
        """Регистрация с некорректным возрастом."""
        self.ui.age_validator.validate = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.ui.register_user("Иван", "Иванов", -5, "Пушкина", 1)

    def test_login_user_success(self):
        """Успешный вход пользователя."""
        self.mock_user_repo.authenticate.return_value = True

        result = self.ui.login_user("user123")

        self.assertTrue(result)
        self.assertEqual(self.ui.current_user_id, "user123")

    def test_login_user_failure(self):
        """Неудачный вход пользователя."""
        self.mock_user_repo.authenticate.return_value = False

        result = self.ui.login_user("unknown")

        self.assertFalse(result)
        self.assertIsNone(self.ui.current_user_id)

    def test_get_current_user_authenticated(self):
        """Получение текущего пользователя при авторизации."""
        mock_user = Mock(spec=Human)
        self.mock_user_repo.get_user.return_value = mock_user
        self.ui.current_user_id = "user123"

        result = self.ui.get_current_user()

        self.assertEqual(result, mock_user)
        self.mock_user_repo.get_user.assert_called_with("user123")

    def test_get_current_user_not_authenticated(self):
        """Получение пользователя без авторизации."""
        self.ui.current_user_id = None
        result = self.ui.get_current_user()
        self.assertIsNone(result)

    def test_access_hospital_not_authenticated(self):
        """Доступ к больнице без авторизации."""
        with self.assertRaises(ValueError) as context:
            self.ui.access_hospital(action="get_ticket")
        self.assertIn("не авторизован", str(context.exception))

    def test_access_hospital_success(self):
        """Успешный доступ к больнице."""
        mock_user = Mock(spec=Human)
        self.mock_user_repo.get_user.return_value = mock_user
        self.ui.current_user_id = "user123"
        self.mock_hospital.provide_service.return_value = "Талон выдан"

        result = self.ui.access_hospital(action="get_ticket", doctor_name="therapist")

        self.assertEqual(result, "Талон выдан")
        self.mock_hospital.provide_service.assert_called_with(
            mock_user, "get_ticket", "therapist", None
        )

    def test_access_school_success(self):
        """Успешный доступ к образовательным услугам."""
        mock_user = Mock(spec=Human)
        self.mock_user_repo.get_user.return_value = mock_user
        self.ui.current_user_id = "user123"
        self.mock_edu.provide_service.return_value = "Записан на курс"

        result = self.ui.access_school(action="enroll_course", course_name="Python")

        self.assertEqual(result, "Записан на курс")
        self.mock_edu.provide_service.assert_called()

    def test_access_utility_success(self):
        """Успешный доступ к коммунальным услугам."""
        mock_user = Mock(spec=Human)
        self.mock_user_repo.get_user.return_value = mock_user
        self.ui.current_user_id = "user123"
        self.mock_utility.provide_service.return_value = "Заявка принята"

        result = self.ui.access_utility(action="report_issue", description="Нет света")

        self.assertEqual(result, "Заявка принята")

    def test_get_user_info_not_authenticated(self):
        """Информация о пользователе без авторизации."""
        self.ui.current_user_id = None
        result = self.ui.get_user_info()
        self.assertIsNone(result)

    def test_get_user_info_authenticated(self):
        """Информация о пользователе при авторизации."""
        mock_user = Mock(spec=Human)
        mock_user.name = "Иван"
        mock_user.surname = "Иванов"
        mock_user.age = 30
        mock_user.address = ("Ленина", 10, 5)

        self.mock_user_repo.get_user.return_value = mock_user
        self.ui.current_user_id = "user123"

        result = self.ui.get_user_info()

        self.assertEqual(result["name"], "Иван")
        self.assertEqual(result["address"], ("Ленина", 10, 5))

    def test_format_user_info_full_address(self):
        """Форматирование информации с полным адресом."""
        user_data = {
            "user_id": "abc123",
            "name": "Мария",
            "surname": "Сидорова",
            "age": 28,
            "address": ("Пушкина", 15, 42)
        }
        result = self.ui.format_user_info(user_data)

        self.assertIn("Мария Сидорова", result)
        self.assertIn("Пушкина, д. 15, кв. 42", result)
        self.assertIn("abc123", result)

    def test_format_user_info_short_address(self):
        """Форматирование информации с коротким адресом."""
        user_data = {
            "user_id": "xyz789",
            "name": "Пётр",
            "surname": "Козлов",
            "age": 45,
            "address": ("Гагарина", 8)
        }
        result = self.ui.format_user_info(user_data)

        self.assertIn("Гагарина, д. 8", result)
        self.assertNotIn("квартира", result)


class TestTransportSystemUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_tms = Mock()
        self.mock_city.tms = self.mock_tms
        self.mock_tms.physical_stops = {}
        self.mock_tms.routes = {}
        self.mock_tms.vehicles = {}

        self.ui = TransportSystemUI(self.mock_city)
        self.ui.stop_name_validator = Mock(return_value=True)
        self.ui.passenger_validator = Mock(return_value=True)

    def test_add_stop_success(self):
        """Успешное добавление остановки."""
        stop_id = self.ui.add_stop("Центральная")

        self.assertIn("stop_", stop_id)
        assert self.mock_tms.physical_stops[stop_id].name == "Центральная"

    def test_add_stop_invalid_name(self):
        """Добавление остановки с некорректным именем."""
        self.ui.stop_name_validator = Mock(return_value=False)

        with self.assertRaises(ValueError) as context:
            self.ui.add_stop("123!")
        self.assertIn("Некорректное название", str(context.exception))

    def test_add_route_success(self):
        """Успешное добавление маршрута."""

        stop1_id, stop2_id = "stop_1", "stop_2"
        self.mock_tms.physical_stops = {stop1_id: Mock(), stop2_id: Mock()}

        route_id = self.ui.add_route([stop1_id, stop2_id])

        self.assertEqual(route_id, "r1")
        self.mock_tms.register_route.assert_called_once()

    def test_add_route_empty(self):
        """Добавление пустого маршрута."""
        with self.assertRaises(ValueError) as context:
            self.ui.add_route([])
        self.assertIn("не может быть пустым", str(context.exception))

    def test_add_route_duplicate_stops(self):
        """Добавление маршрута с дубликатами остановок."""
        with self.assertRaises(ValueError) as context:
            self.ui.add_route(["stop_1", "stop_1", "stop_2"])
        self.assertIn("дубликаты", str(context.exception))

    def test_add_route_stop_not_found(self):
        """Добавление маршрута с несуществующей остановкой."""
        self.mock_tms.physical_stops = {"stop_1": Mock()}

        with self.assertRaises(ValueError) as context:
            self.ui.add_route(["stop_1", "stop_999"])
        self.assertIn("не найдена", str(context.exception))

    def test_add_vehicle_success(self):
        """Успешное добавление транспорта."""
        self.mock_tms.routes = {"r1": Mock()}

        vehicle_id = self.ui.add_vehicle("bus", "r1")

        self.assertIn("bus_", vehicle_id)
        self.mock_tms.register_vehicle.assert_called_once()

    def test_add_vehicle_invalid_type(self):
        """Добавление транспорта с неизвестным типом."""
        with self.assertRaises(ValueError) as context:
            self.ui.add_vehicle("helicopter", "r1")
        self.assertIn("Неизвестный тип", str(context.exception))

    def test_add_vehicle_route_not_found(self):
        """Добавление транспорта на несуществующий маршрут."""
        self.mock_tms.routes = {}

        with self.assertRaises(ValueError) as context:
            self.ui.add_vehicle("bus", "r999")
        self.assertIn("не найден", str(context.exception))

    def test_update_vehicle_location_success(self):
        """Успешное обновление локации транспорта."""
        mock_vehicle = Mock()
        mock_vehicle.report_stop_passed.return_value = "Остановка пройдена"
        self.mock_tms.vehicles = {"bus_1": mock_vehicle}

        mock_route = Mock()
        mock_route.stops = [Mock(), Mock(), Mock()]
        self.mock_tms.routes = {"r1": mock_route}
        mock_vehicle.route_id = "r1"

        result = self.ui.update_vehicle_location("bus_1", 1)

        self.assertEqual(result, "Остановка пройдена")
        mock_vehicle.report_stop_passed.assert_called_with(1)

    def test_update_vehicle_location_invalid_index(self):
        """Обновление локации с некорректным индексом."""
        mock_vehicle = Mock()
        self.mock_tms.vehicles = {"bus_1": mock_vehicle}

        mock_route = Mock()
        mock_route.stops = [Mock()]
        self.mock_tms.routes = {"r1": mock_route}
        mock_vehicle.route_id = "r1"

        with self.assertRaises(ValueError) as context:
            self.ui.update_vehicle_location("bus_1", 5)
        self.assertIn("Некорректный индекс", str(context.exception))

    def test_arrive_at_stop_success(self):
        """Симуляция прихода пассажира на остановку."""
        mock_stop = Mock()
        mock_stop.get_status.return_value = {"passengers": 2}
        self.mock_tms.physical_stops = {"stop_1": mock_stop}

        self.mock_tms.get_arrival_info.return_value = {
            "stop_id": "stop_1", "stop_name": "Центральная", "arrivals": []
        }

        result = self.ui.arrive_at_stop("stop_1")

        self.assertEqual(result["stop_name"], "Центральная")

        calls = mock_stop.update_passengers.call_args_list
        self.assertEqual(len(calls), 2)

    def test_list_routes_empty(self):
        """Список маршрутов, когда их нет."""
        self.mock_tms.routes = {}
        result = self.ui.list_routes()
        self.assertEqual(result, [])

    def test_list_routes_with_data(self):
        """Список маршрутов с данными."""
        mock_route = Mock()
        mock_stop1 = Mock()
        mock_stop1.bus_stop.name = "Старт"
        mock_stop2 = Mock()
        mock_stop2.bus_stop.name = "Финиш"
        mock_route.stops = [mock_stop1, mock_stop2]
        mock_route.vehicles = [Mock(device_id="bus_1")]

        self.mock_tms.routes = {"r1": mock_route}

        result = self.ui.list_routes()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["route_id"], "r1")
        self.assertEqual(result[0]["stops"], ["Старт", "Финиш"])

    def test_format_arrival_info_with_arrivals(self):
        """Форматирование информации о прибытии с транспортом."""
        info = {
            "stop_name": "Центральная",
            "arrivals": [
                {"type": "bus", "route": "r1", "eta_minutes": 0},
                {"type": "tram", "route": "r2", "eta_minutes": 5}
            ]
        }
        mock_print = Mock()
        self.ui.format_arrival_info(info, mock_print)

        self.assertTrue(mock_print.called)
        calls_str = str(mock_print.call_args_list)
        self.assertIn("Сейчас на остановке", calls_str)
        self.assertIn("через 5 мин", calls_str)

    def test_format_arrival_info_no_arrivals(self):
        """Форматирование информации без прибытий."""
        info = {"stop_name": "Пустая", "arrivals": []}
        mock_print = Mock()
        self.ui.format_arrival_info(info, mock_print)

        calls_str = str(mock_print.call_args_list)
        self.assertIn("Нет ближайшего транспорта", calls_str)


class TestTrafficManagementUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_city.districts = {}
        self.mock_city.traffic_manager = Mock()
        self.mock_city.traffic_manager.intersections = {}

        self.ui = TrafficManagementUI(self.mock_city)

    def test_add_intersection_district_not_found(self):
        """Создание перекрёстка в несуществующем районе."""
        with self.assertRaises(ValueError) as context:
            self.ui.add_intersection("unknown", "simple")
        self.assertIn("не найден", str(context.exception))

    def test_add_intersection_simple_success(self):
        """Успешное создание простого перекрёстка."""
        mock_district = Mock()
        mock_district.district_id = "D1"
        mock_district.intersections = []
        self.mock_city.districts = {"D1": mock_district}

        int_id = self.ui.add_intersection("D1", "simple")

        self.assertEqual(int_id, "D1_1")
        mock_district.register_intersection.assert_called_once()

    def test_add_intersection_full_success(self):
        """Успешное создание полного перекрёстка (4 светофора)."""
        mock_district = Mock()
        mock_district.district_id = "D2"
        mock_district.intersections = []
        self.mock_city.districts = {"D2": mock_district}

        int_id = self.ui.add_intersection("D2", "full")

        self.assertEqual(int_id, "D2_1")

        call_args = mock_district.register_intersection.call_args[0][0]
        self.assertEqual(len(call_args.lights), 4)

    def test_trigger_accident_success(self):
        """Симуляция аварии на перекрёстке."""
        mock_light = Mock()
        mock_light.camera = Mock()
        mock_intersection = Mock()
        mock_intersection.lights = [mock_light]

        self.mock_city.traffic_manager.intersections = {"INT_1": mock_intersection}

        self.ui.trigger_accident("INT_1")

        mock_light.camera.detect_event.assert_called_with(VehicleType.CAR, True)

    def test_trigger_accident_not_found(self):
        """Симуляция аварии на несуществующем перекрёстке."""
        self.mock_city.traffic_manager.intersections = {}

        with self.assertRaises(ValueError) as context:
            self.ui.trigger_accident("UNKNOWN")
        self.assertIn("не найден", str(context.exception))

    def test_manage_flow_success(self):
        """Управление потоком транспорта."""
        self.mock_city.traffic_manager.prioritize_public_transport.return_value = "Приоритет установлен"

        mock_intersection = Mock()
        mock_intersection.regulate_intersection.return_value = False
        mock_intersection.intersection_id = "INT_1"
        self.mock_city.traffic_manager.intersections = {"INT_1": mock_intersection}

        result = self.ui.manage_flow()

        self.assertIn("Приоритет установлен", result)
        self.assertIn("INT_1", result)

    def test_manage_flow_with_accident(self):
        """Управление потоком с аварией."""
        self.mock_city.traffic_manager.prioritize_public_transport.return_value = ""

        mock_intersection = Mock()
        mock_intersection.regulate_intersection.return_value = True
        mock_intersection.intersection_id = "INT_ACC"
        self.mock_city.traffic_manager.intersections = {"INT_ACC": mock_intersection}

        result = self.ui.manage_flow()

        self.assertIn("Внимание! Авария", result)
        self.assertIn("INT_ACC", result)


class TestSensorUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_district = Mock()
        self.mock_city.districts = {"D1": self.mock_district}

        self.ui = SensorUI(self.mock_city)
        self.ui.value_validator = Mock(return_value=True)

    def test_set_smart_home_sensor_water_success(self):
        """Установка значения сенсора воды в умном доме."""
        mock_home = Mock()
        self.mock_district.smart_homes = [mock_home]

        result = self.ui.set_smart_home_sensor("D1", 0, "water", 150)

        self.assertIn("установлено", result)
        mock_home.water_meter.set_value.assert_called_with(150)

    def test_set_smart_home_sensor_light(self):
        """Установка сенсора света без light_index."""
        mock_home = Mock()
        self.mock_district.smart_homes = [mock_home]

        with self.assertRaises(ValueError) as context:
            self.ui.set_smart_home_sensor("D1", 0, "light", 50)
        self.assertIn("требуется параметр", str(context.exception))

    def test_set_smart_home_sensor_light_index_out_of_range(self):
        """Некорректный индекс светильника (строки 46-47)."""
        mock_home = Mock()
        mock_home.lightning_system.smart_lights = [Mock()]
        self.mock_district.smart_homes = [mock_home]

        with self.assertRaises(ValueError) as context:
            self.ui.set_smart_home_sensor("D1", 0, "light", 100, light_index=5)
        self.assertIn("Некорректный индекс светильника", str(context.exception))

    def test_set_smart_home_sensor_invalid_type(self):
        """Установка сенсора с неизвестным типом."""
        mock_home = Mock()
        self.mock_district.smart_homes = [mock_home]
        with self.assertRaises(ValueError) as context:
            self.ui.set_smart_home_sensor("D1", 0, "unknown", 100)
        self.assertIn("Неизвестный тип", str(context.exception))

    def test_set_street_light_sensor_success(self):
        """Установка значения сенсора уличного фонаря."""
        mock_light = Mock()
        self.mock_district.lights = [mock_light]

        result = self.ui.set_street_light_sensor("D1", 0, 75)

        self.assertIn("установлено", result)
        mock_light.light_level_sensor.set_value.assert_called_with(75)

    def test_set_street_light_sensor_district_not_found(self):
        """Район не найден для уличного фонаря (строка 73)."""
        with self.assertRaises(ValueError) as context:
            self.ui.set_street_light_sensor("UNKNOWN", 0, 50)
        self.assertIn("Район UNKNOWN не найден", str(context.exception))

    def test_set_district_sensor_success(self):
        """Установка значения сенсора района."""
        mock_sensor = Mock()
        self.mock_district.air_quality_sensors = [mock_sensor]

        result = self.ui.set_district_sensor("D1", "air", 0, 42)

        self.assertIn("установлено", result)
        mock_sensor.set_value.assert_called_with(42)

    def test_set_generator_sensor_solar_success(self):
        """Установка сенсора солнечной панели (строки 92-94)."""
        mock_generator = Mock()
        self.mock_district.generators = [mock_generator, Mock()]

        result = self.ui.set_generator_sensor("D1", "solar", 900)

        self.assertEqual(result, "Значение сенсора солнечной панели установлено")
        mock_generator.light_level_sensor.set_value.assert_called_with(900)

    def test_set_generator_sensor_wind_success(self):
        """Установка сенсора скорости ветра (строки 95-97)."""
        mock_wind_gen = Mock()
        self.mock_district.generators = [Mock(), mock_wind_gen]

        result = self.ui.set_generator_sensor("D1", "wind", 15)

        self.assertEqual(result, "Значение скорости ветра установлено")
        mock_wind_gen.set_value.assert_called_with(15)

    def test_set_traffic_sensor_camera_success(self):
        """Фиксация события камеры на перекрёстке."""
        mock_light = Mock()
        mock_light.device_id = "TL_1"
        mock_light.camera = Mock()

        mock_intersection = Mock()
        mock_intersection.lights = {mock_light: mock_light}
        self.mock_district.intersections = [mock_intersection]

        result = self.ui.set_traffic_sensor(
            "D1", 0, "TL_1", "camera", (VehicleType.BUS, False)
        )

        self.assertIn("зафиксировано", result)
        mock_light.camera.detect_event.assert_called_with(VehicleType.BUS, False)

    def test_set_traffic_sensor_flow_success(self):
        """Установка значения датчика потока (строка 152)."""
        mock_light = Mock()
        mock_light.device_id = "TL_1"
        mock_light.flow_sensor = Mock()

        mock_intersection = Mock()
        mock_intersection.lights = {mock_light: mock_light}
        self.mock_district.intersections = [mock_intersection]

        result = self.ui.set_traffic_sensor("D1", 0, "TL_1", "flow", 25)

        self.assertEqual(result, "Значение потока транспорта установлено")
        mock_light.flow_sensor.set_value.assert_called_with(25)

    def test_set_traffic_sensor_pedestrian_success(self):
        """Установка значения датчика пешеходов (строка 157)."""
        mock_light = Mock()
        mock_light.device_id = "TL_2"
        mock_light.pedestrian_sensor = Mock()

        mock_intersection = Mock()
        mock_intersection.lights = {mock_light: mock_light}
        self.mock_district.intersections = [mock_intersection]

        result = self.ui.set_traffic_sensor("D1", 0, "TL_2", "pedestrian", 8)

        self.assertEqual(result, "Значение сенсора пешеходов установлено")
        mock_light.pedestrian_sensor.set_value.assert_called_with(8)

    def test_get_sensor_list_smart_homes(self):
        """Получение списка сенсоров умных домов."""
        mock_home = Mock()
        mock_home.address = ("Ленина", 10)
        mock_home.water_meter.device_id = "WM_1"
        mock_home.thermostat.temp_sensor.sensor_id = "TS_1"
        mock_light = Mock()
        mock_light.light_level_sensor.sensor_id = "LS_1"
        mock_home.lightning_system.smart_lights = [mock_light]

        self.mock_district.smart_homes = [mock_home]

        result = self.ui.get_sensor_list("D1", "smart_homes")

        self.assertTrue(any(s["type"] == "water" for s in result))
        self.assertTrue(any(s["type"] == "thermostat_temp" for s in result))
        self.assertTrue(any(s["type"] == "light" for s in result))

    def test_get_sensor_list_traffic(self):
        """Получение списка сенсоров транспорта."""
        mock_light = Mock()
        mock_light.device_id = "TL_1"
        mock_light.camera.sensor_id = "CAM_1"
        mock_light.flow_sensor.sensor_id = "FLOW_1"
        mock_light.pedestrian_sensor.sensor_id = "PED_1"

        mock_intersection = Mock()
        mock_intersection.lights = {mock_light: mock_light}
        self.mock_district.intersections = [mock_intersection]

        result = self.ui.get_sensor_list("D1", "traffic")

        self.assertTrue(any(s["type"] == "camera" for s in result))
        self.assertTrue(any(s["type"] == "flow" for s in result))
        self.assertTrue(any(s["type"] == "pedestrian" for s in result))

    def test_get_sensor_list_unknown_category(self):
        """Неизвестная категория в get_sensor_list (строки 190-191)."""
        with self.assertRaises(ValueError) as context:
            self.ui.get_sensor_list("D1", "magnetic")
        self.assertIn("Неизвестная категория", str(context.exception))

    def test_format_sensor_list_with_light_index(self):
        """Форматирование списка сенсоров со светильниками."""
        sensors = [
            {"index": 0, "device_id": "LS_1", "type": "light", "light_index": 2}
        ]
        result = self.ui.format_sensor_list(sensors)

        self.assertIn("[светильник

    def test_format_sensor_list_with_intersection(self):
        """Форматирование списка сенсоров с перекрёстками."""
        sensors = [
            {
                "device_id": "CAM_1", "type": "camera",
                "intersection_index": 0, "light_device_id": "TL_1"
            }
        ]
        result = self.ui.format_sensor_list(sensors)

        self.assertIn("[перекресток
        self.assertIn("[светофор TL_1]", result)


class TestEnergyUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_grid = Mock()
        self.mock_city.energy_grid = self.mock_grid

        self.ui = EnergyUI(self.mock_city)

    def test_generate_report_success(self):
        """Генерация отчета по энергии."""
        self.mock_grid.optimize_all.return_value = {
            "production": 1500,
            "consumption": 1200,
            "surplus": 300,
            "result": "Избыток энергии"
        }

        result = self.ui.generate_report()

        self.assertIn("РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ", result)
        self.assertIn("1500 кВт·ч", result)
        self.assertIn("Избыток энергии", result)
        self.assertIn("=" * 50, result)


class TestEnvironmentMonitoringUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_monitoring = Mock()
        self.mock_city.monitoring_system = self.mock_monitoring
        self.mock_city.districts = {}

        self.ui = EnvironmentMonitoringUI(self.mock_city)

    def test_get_environment_state_success(self):
        """Получение состояния окружающей среды."""
        mock_sensor = Mock()
        mock_district = Mock()
        mock_district.air_quality_sensors = [mock_sensor]
        mock_district.temperature_sensors = [mock_sensor]
        mock_district.humidity_sensors = [mock_sensor]
        mock_district.noise_sensors = [mock_sensor]

        self.mock_city.districts = {"D1": mock_district}

        self.mock_monitoring.environmental_monitoring_operation.return_value = {
            "average": {"air": Mock(label="Хорошее"), "temperature": Mock(label="Комфортная")}
        }

        result = self.ui.get_environment_state()

        self.assertIn("average", result)
        self.mock_monitoring.environmental_monitoring_operation.assert_called_once()

    def test_format_environment_state(self):
        """Форматирование состояния среды."""
        results = {
            "air": Mock(label="Отличное"),
            "temperature": Mock(label="Тёплая"),
            "humidity": Mock(label="Нормальная"),
            "noise": Mock(label="Тихо")
        }
        output = self.ui.format_environment_state(results)

        self.assertIn("Качество воздуха: Отличное", output)
        self.assertIn("Температура: Тёплая", output)
        self.assertIn("Влажность: Нормальная", output)
        self.assertIn("Шум: Тихо", output)

    def test_print_environment_state(self):
        """Вывод состояния среды через print_func."""
        mock_print = Mock()
        self.ui.get_environment_state = Mock(return_value={
            "air": Mock(label="Хорошее"),
            "temperature": Mock(label="Нормальная"),
            "humidity": Mock(label="Сухая"),
            "noise": Mock(label="Шумно")
        })

        self.ui.print_environment_state(mock_print)

        mock_print.assert_called_once()
        self.assertIn("Хорошее", str(mock_print.call_args))


class TestUrbanPlanningDataAnalysisUI(unittest.TestCase):

    def setUp(self):
        self.mock_city = Mock()
        self.mock_analyzer = Mock()
        self.mock_monitoring = Mock()

        self.mock_city.analyzer = self.mock_analyzer
        self.mock_city.monitoring_system = self.mock_monitoring
        self.mock_city.districts = {}

        self.ui = UrbanPlanningDataAnalysisUI(self.mock_city)

    def test_generate_report_success(self):
        """Генерация отчета по планированию."""
        mock_sensor = Mock()
        mock_district = Mock()
        mock_district.air_quality_sensors = [mock_sensor]
        mock_district.temperature_sensors = [mock_sensor]
        mock_district.humidity_sensors = [mock_sensor]
        mock_district.noise_sensors = [mock_sensor]
        mock_district.auto_collect_sensor_data = Mock()

        self.mock_city.districts = {"D1": mock_district}

        self.mock_monitoring.environmental_monitoring_operation.return_value = {
            "average": {"air": Mock(), "temperature": Mock()}
        }
        self.mock_analyzer.generate_planning_report.return_value = {
            "generated_at": "2026-01-01",
            "districts": []
        }

        result = self.ui.generate_report()

        self.assertEqual(result["generated_at"], "2026-01-01")
        self.mock_analyzer.generate_planning_report.assert_called_once()

    def test_format_report_with_priority(self):
        """Форматирование отчета с приоритетами развития."""
        report = {
            "generated_at": "2026-01-01",
            "districts": [{
                "district_id": "D1",
                "metrics": {"air_quality": {"value": 85}, "noise": {"value": 40}},
                "development_priority": {
                    "focus_area": "Экология",
                    "current_value": 85,
                    "action": "Увеличить зелёные зоны. Установить фильтры."
                }
            }]
        }
        output = self.ui.format_report(report)

        self.assertIn("Район: D1", output)
        self.assertIn("air_quality: 85", output)
        self.assertIn("Экология", output)
        self.assertIn("Увеличить зелёные зоны", output)

    def test_format_report_without_priority(self):
        """Форматирование отчета без приоритетов."""
        report = {
            "generated_at": "2026-01-01",
            "districts": [{
                "district_id": "D2",
                "metrics": {"temperature": {"value": 22}}
            }]
        }
        output = self.ui.format_report(report)

        self.assertIn("Нет данных для определения приоритетов", output)

    def test_print_report(self):
        """Вывод отчета через print_func."""
        mock_print = Mock()
        self.ui.generate_report = Mock(return_value={
            "generated_at": "2026-01-01", "districts": []
        })
        self.ui.format_report = Mock(return_value="Отчет готов")

        self.ui.print_report(mock_print)

        mock_print.assert_called_with("Отчет готов")


class TestCityUI(unittest.TestCase):

    @patch('SmartCityModel.ui.city_ui.SmartCity')
    @patch('SmartCityModel.ui.city_ui.TransportSystemUI')
    @patch('SmartCityModel.ui.city_ui.TrafficManagementUI')
    @patch('SmartCityModel.ui.city_ui.PublicServiceUI')
    def setUp(self, mock_pub_ui, mock_traffic_ui, mock_tms_ui, mock_city_cls):
        self.mock_city = Mock()
        mock_city_cls.return_value = self.mock_city

        self.mock_tms_ui = Mock()
        self.mock_traffic_ui = Mock()
        self.mock_pub_ui = Mock()

        mock_tms_ui.return_value = self.mock_tms_ui
        mock_traffic_ui.return_value = self.mock_traffic_ui
        mock_pub_ui.return_value = self.mock_pub_ui

        from SmartCityModel.ui.city_ui import CityUI
        self.ui = CityUI()

    def test_init_creates_sub_uis(self):
        """Проверка, что при инициализации создаются под-модули UI."""

        self.assertIsNotNone(self.ui.tms_ui)
        self.assertIsNotNone(self.ui.traffic_ui)
        self.assertIsNotNone(self.ui.services_ui)
        self.assertIsNotNone(self.ui.sensors_ui)
        self.assertIsNotNone(self.ui.energy_ui)
        self.assertIsNotNone(self.ui.env_ui)
        self.assertIsNotNone(self.ui.urban_planning_ui)


if __name__ == "__main__":
    unittest.main(verbosity=2)
