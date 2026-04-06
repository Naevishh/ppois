"""
Юнит-тесты для всех классов модуля transport.
Запуск: python -m unittest tests.test_transport -v
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from SmartCityModel.transport.models import BusStop, RouteStop, PublicTransportVehicle, TransportRoute
from SmartCityModel.transport.monitoring import TransportMonitoringSystem
from SmartCityModel.transport.traffic_control import SmartTrafficLight, Intersection, TrafficManager
from SmartCityModel.core import Domain, VehicleType, TrafficLightColor, Direction, TransportException


class TestBusStop(unittest.TestCase):

    def setUp(self):
        self.stop = BusStop(name="Центральная площадь")

    def test_init_attributes(self):
        """Проверка инициализации атрибутов."""
        self.assertEqual(self.stop.name, "Центральная площадь")
        self.assertEqual(self.stop._waiting_passengers, 0)
        self.assertEqual(self.stop._display_message, "")
        self.assertEqual(self.stop.domain, Domain.TRANSPORTATION)
        self.assertTrue(self.stop.device_id.startswith("stop_"))

    def test_update_passengers_valid(self):
        """Обновление количества пассажиров с корректным значением."""
        self.stop.update_passengers(15)
        self.assertEqual(self.stop._waiting_passengers, 15)

        self.stop.update_passengers(0)
        self.assertEqual(self.stop._waiting_passengers, 0)

    def test_update_passengers_invalid(self):
        """Обновление с отрицательным значением должно вызывать исключение."""
        with self.assertRaises(TransportException) as context:
            self.stop.update_passengers(-5)
        self.assertIn("отрицательным", str(context.exception))

    def test_set_display(self):
        """Установка сообщения на табло."""
        self.stop.set_display("Автобус №5: 3 мин")
        self.assertEqual(self.stop._display_message, "Автобус №5: 3 мин")

    def test_get_status(self):
        """Получение статуса остановки."""
        self.stop.update_passengers(7)
        self.stop.set_display("Следующий: 2 мин")

        status = self.stop.get_status()

        self.assertEqual(status["name"], "Центральная площадь")
        self.assertEqual(status["passengers"], 7)
        self.assertEqual(status["display"], "Следующий: 2 мин")
        self.assertIn("stop_", status["stop_id"])


class TestRouteStop(unittest.TestCase):

    def setUp(self):
        self.bus_stop = BusStop(name="Парк Горького")
        self.route_stop = RouteStop(bus_stop=self.bus_stop, index=3)

    def test_init(self):
        """Проверка инициализации RouteStop."""
        self.assertEqual(self.route_stop.bus_stop, self.bus_stop)
        self.assertEqual(self.route_stop.index, 3)

    def test_different_index(self):
        """Проверка с другим индексом."""
        rs = RouteStop(self.bus_stop, 0)
        self.assertEqual(rs.index, 0)


class TestPublicTransportVehicle(unittest.TestCase):

    def setUp(self):
        self.vehicle = PublicTransportVehicle(
            vehicle_type=VehicleType.BUS,
            route_id="BUS_42"
        )

    def test_init_attributes(self):
        """Проверка инициализации атрибутов."""
        self.assertEqual(self.vehicle.vehicle_type, VehicleType.BUS)
        self.assertEqual(self.vehicle.route_id, "BUS_42")
        self.assertEqual(self.vehicle._last_passed_stop_index, -1)
        self.assertEqual(self.vehicle._passenger_count, 0)
        self.assertTrue(self.vehicle.device_id.startswith("bus_"))
        self.assertEqual(self.vehicle.domain, Domain.TRANSPORTATION)

    def test_report_stop_passed_forward(self):
        """Сообщение о прохождении остановки вперёд по маршруту."""
        result = self.vehicle.report_stop_passed(2)

        self.assertEqual(self.vehicle._last_passed_stop_index, 2)
        self.assertIn("Пройдена остановка", result)
        self.assertIn("#2", result)
        self.assertIsNotNone(self.vehicle._last_update)

    def test_report_stop_passed_backward(self):
        """Попытка сообщить о прохождении остановки назад по маршруту."""
        self.vehicle.report_stop_passed(5)
        result = self.vehicle.report_stop_passed(3)

        self.assertIsNone(result)
        self.assertEqual(self.vehicle._last_passed_stop_index, 5)

    def test_report_stop_passed_same(self):
        """Повторное сообщение о той же остановке."""
        self.vehicle.report_stop_passed(3)
        result = self.vehicle.report_stop_passed(3)

        self.assertIsNone(result)

    def test_update_passengers_valid(self):
        """Обновление количества пассажиров в допустимом диапазоне."""
        self.vehicle.update_passengers(25)
        self.assertEqual(self.vehicle._passenger_count, 25)

        self.vehicle.update_passengers(60)
        self.assertEqual(self.vehicle._passenger_count, 60)

    def test_update_passengers_negative(self):
        """Отрицательное количество пассажиров."""
        with self.assertRaises(TransportException) as context:
            self.vehicle.update_passengers(-10)
        self.assertIn("отрицательным", str(context.exception))

    def test_update_passengers_overflow(self):
        """Превышение лимита пассажиров."""
        with self.assertRaises(TransportException) as context:
            self.vehicle.update_passengers(61)
        self.assertIn("слишком большое", str(context.exception))

    def test_get_last_stop_index_property(self):
        """Проверка свойства get_last_stop_index."""
        self.assertEqual(self.vehicle.get_last_stop_index, -1)
        self.vehicle.report_stop_passed(4)
        self.assertEqual(self.vehicle.get_last_stop_index, 4)

    def test_get_status(self):
        """Получение статуса транспортного средства."""
        self.vehicle.report_stop_passed(2)
        self.vehicle.update_passengers(18)

        status = self.vehicle.get_status()

        self.assertEqual(status["type"], VehicleType.BUS.value)
        self.assertEqual(status["route_id"], "BUS_42")
        self.assertEqual(status["last_passed_stop_index"], 2)
        self.assertEqual(status["passengers"], 18)
        self.assertIn("bus_", status["vehicle_id"])


class TestTransportRoute(unittest.TestCase):

    def setUp(self):
        self.stops = [
            RouteStop(BusStop("Старт"), 0),
            RouteStop(BusStop("Середина"), 1),
            RouteStop(BusStop("Финиш"), 2)
        ]
        self.route = TransportRoute(
            route_id="ROUTE_10",
            stops=self.stops,
            avg_time_between_stops=5
        )

    def test_init(self):
        """Проверка инициализации маршрута."""
        self.assertEqual(self.route.route_id, "ROUTE_10")
        self.assertEqual(len(self.route.stops), 3)
        self.assertEqual(self.route.vehicles, [])
        self.assertEqual(self.route.avg_time_between_stops, 5)

    def test_add_vehicle_same_route(self):
        """Добавление транспорта с правильным route_id."""
        vehicle = PublicTransportVehicle(VehicleType.BUS, "ROUTE_10")
        self.route.add_vehicle(vehicle)

        self.assertEqual(len(self.route.vehicles), 1)
        self.assertIn(vehicle, self.route.vehicles)

    def test_add_vehicle_different_route(self):
        """Попытка добавить транспорт с другим route_id."""
        vehicle = PublicTransportVehicle(VehicleType.TRAM, "ROUTE_99")
        self.route.add_vehicle(vehicle)

        self.assertEqual(len(self.route.vehicles), 0)

    def test_get_status(self):
        """Получение статуса маршрута."""

        for i in range(2):
            v = PublicTransportVehicle(VehicleType.BUS, "ROUTE_10")
            self.route.add_vehicle(v)

        status = self.route.get_status()

        self.assertEqual(status["route_id"], "ROUTE_10")
        self.assertEqual(status["total_stops"], 3)
        self.assertEqual(status["active_vehicles"], 2)


class TestTransportMonitoringSystem(unittest.TestCase):

    def setUp(self):
        self.tms = TransportMonitoringSystem()
        self.stop1 = BusStop("Площадь")
        self.stop2 = BusStop("Вокзал")
        self.route_stops = [
            RouteStop(self.stop1, 0),
            RouteStop(self.stop2, 1)
        ]
        self.route = TransportRoute("R1", self.route_stops)
        self.vehicle = PublicTransportVehicle(VehicleType.BUS, "R1")

    def test_register_route(self):
        """Регистрация маршрута."""
        self.tms.register_route(self.route)

        self.assertIn("R1", self.tms.routes)
        self.assertIn(self.stop1.device_id, self.tms.physical_stops)
        self.assertIn(self.stop2.device_id, self.tms.physical_stops)

    def test_register_route_no_duplicate_stops(self):
        """Регистрация маршрута с уже существующей остановкой."""

        self.tms.register_route(self.route)

        route2 = TransportRoute("R2", [RouteStop(self.stop1, 0)])
        self.tms.register_route(route2)

        self.assertEqual(len(self.tms.physical_stops), 2)
        self.assertIs(self.tms.physical_stops[self.stop1.device_id], self.stop1)

    def test_register_vehicle(self):
        """Регистрация транспортного средства."""
        self.tms.register_route(self.route)
        self.tms.register_vehicle(self.vehicle)

        self.assertIn(self.vehicle.device_id, self.tms.vehicles)
        self.assertIn(self.vehicle, self.route.vehicles)

    def test_register_vehicle_without_route(self):
        """Регистрация транспорта, маршрут которого ещё не зарегистрирован."""

        self.tms.register_vehicle(self.vehicle)

        self.assertIn(self.vehicle.device_id, self.tms.vehicles)

    def test_calculate_eta_same_stop(self):
        """ETA = 0, если транспорт уже на остановке."""
        self.vehicle.report_stop_passed(1)
        target_stop = self.route_stops[1]

        eta = self.tms.calculate_eta(self.vehicle, target_stop, self.route)
        self.assertEqual(eta, 0)

    def test_calculate_eta_future_stop(self):
        """Расчёт ETA для будущей остановки."""
        self.vehicle.report_stop_passed(0)
        target_stop = self.route_stops[1]

        with patch('random.randint', return_value=1):
            eta = self.tms.calculate_eta(self.vehicle, target_stop, self.route)

        self.assertEqual(eta, 4.0)

    def test_calculate_eta_past_stop(self):
        """ETA = None, если остановка уже пройдена."""
        self.vehicle.report_stop_passed(1)
        target_stop = self.route_stops[0]

        eta = self.tms.calculate_eta(self.vehicle, target_stop, self.route)
        self.assertIsNone(eta)

    def test_calculate_eta_unknown_position(self):
        """ETA = None, если позиция транспорта неизвестна."""

        target_stop = self.route_stops[0]

        eta = self.tms.calculate_eta(self.vehicle, target_stop, self.route)
        self.assertIsNone(eta)

    def test_get_arrival_info_stop_not_found(self):
        """Запрос информации для несуществующей остановки."""
        result = self.tms.get_arrival_info("nonexistent_stop")

        self.assertEqual(result, {"error": "Остановка не найдена"})

    def test_get_arrival_info_no_vehicles(self):
        """Запрос информации, когда на маршруте нет транспорта."""
        self.tms.register_route(self.route)

        result = self.tms.get_arrival_info(self.stop1.device_id)

        self.assertEqual(result["stop_id"], self.stop1.device_id)
        self.assertEqual(result["stop_name"], "Площадь")
        self.assertEqual(result["arrivals"], [])
        self.assertEqual(self.stop1._display_message, "Нет данных")

    def test_get_arrival_info_with_vehicle(self):
        """Запрос информации с приближающимся транспортом."""
        self.tms.register_route(self.route)
        self.tms.register_vehicle(self.vehicle)
        self.vehicle.report_stop_passed(1)

        with patch('random.randint', return_value=0):
            result = self.tms.get_arrival_info(self.stop2.device_id)

        self.assertEqual(len(result["arrivals"]), 1)
        arrival = result["arrivals"][0]
        self.assertEqual(arrival["route"], "R1")
        self.assertEqual(arrival["type"], "bus")
        self.assertIn("eta_minutes", arrival)

        self.assertIn("мин", self.stop2._display_message)


class TestSmartTrafficLight(unittest.TestCase):

    def setUp(self):
        self.flow_sensor = Mock()
        self.camera = Mock()
        self.pedestrian_sensor = Mock()

        self.traffic_light = SmartTrafficLight(
            flow_sensor=self.flow_sensor,
            camera=self.camera,
            pedestrian_sensor=self.pedestrian_sensor
        )

    def test_init(self):
        """Проверка инициализации светофора."""
        self.assertEqual(self.traffic_light._current_color, TrafficLightColor.RED)
        self.assertEqual(self.traffic_light.flow_sensor, self.flow_sensor)
        self.assertEqual(self.traffic_light.camera, self.camera)
        self.assertEqual(self.traffic_light.pedestrian_sensor, self.pedestrian_sensor)

    def test_init_without_pedestrian_sensor(self):
        """Инициализация без датчика пешеходов."""
        tl = SmartTrafficLight(self.flow_sensor, self.camera)
        self.assertIsNone(tl.pedestrian_sensor)

    def test_get_traffic_request_incident(self):
        """Запрос приоритета при инциденте."""
        self.camera.get_status.return_value = {"incident": True, "vehicle_type": VehicleType.CAR}
        self.flow_sensor.get_status.return_value = 5
        self.pedestrian_sensor.get_status.return_value = 4

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 100)
        self.assertEqual(request["reason"], "INCIDENT")
        self.assertFalse(request["pedestrian_waiting"])

    def test_get_traffic_request_emergency_vehicle(self):
        """Запрос приоритета для спецтранспорта."""
        self.camera.get_status.return_value = {
            "incident": False,
            "vehicle_type": VehicleType.AMBULANCE
        }
        self.flow_sensor.get_status.return_value = 3
        self.pedestrian_sensor.get_status.return_value = 4

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 90)
        self.assertEqual(request["reason"], "EMERGENCY")

    def test_get_traffic_request_public_transport(self):
        """Запрос приоритета для общественного транспорта."""
        self.camera.get_status.return_value = {
            "incident": False,
            "vehicle_type": VehicleType.BUS
        }
        self.flow_sensor.get_status.return_value = 8
        self.pedestrian_sensor.get_status.return_value = 4

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 60)
        self.assertEqual(request["reason"], "PUBLIC_TRANSPORT")

    def test_get_traffic_request_high_flow(self):
        """Запрос приоритета при высоком потоке."""
        self.camera.get_status.return_value = {
            "incident": False,
            "vehicle_type": VehicleType.CAR
        }
        self.flow_sensor.get_status.return_value = 20
        self.pedestrian_sensor.get_status.return_value = 4

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 50)
        self.assertEqual(request["reason"], "HIGH_FLOW")

    def test_get_traffic_request_pedestrians_waiting(self):
        """Приоритет для пешеходов."""
        self.camera.get_status.return_value = {
            "incident": False,
            "vehicle_type": VehicleType.CAR
        }
        self.flow_sensor.get_status.return_value = 5
        self.pedestrian_sensor.get_status.return_value = 10

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 5)
        self.assertEqual(request["reason"], "PEDESTRIANS_WAITING")
        self.assertTrue(request["pedestrian_waiting"])

    def test_get_traffic_request_default(self):
        """Базовый запрос без особых условий."""
        self.camera.get_status.return_value = {
            "incident": False,
            "vehicle_type": VehicleType.CAR
        }
        self.flow_sensor.get_status.return_value = 3
        self.pedestrian_sensor.get_status.return_value = 1

        request = self.traffic_light.get_traffic_request()

        self.assertEqual(request["priority"], 10)
        self.assertEqual(request["reason"], "FLOW")
        self.assertFalse(request["pedestrian_waiting"])

    def test_set_color(self):
        """Смена цвета светофора."""
        self.traffic_light.set_color(TrafficLightColor.GREEN)
        self.assertEqual(self.traffic_light._current_color, TrafficLightColor.GREEN)

        self.traffic_light.set_color(TrafficLightColor.YELLOW)
        self.assertEqual(self.traffic_light._current_color, TrafficLightColor.YELLOW)


class TestIntersection(unittest.TestCase):

    def setUp(self):

        self.light_n = Mock(spec=SmartTrafficLight)
        self.light_s = Mock(spec=SmartTrafficLight)
        self.light_e = Mock(spec=SmartTrafficLight)
        self.light_w = Mock(spec=SmartTrafficLight)

        self.light_n.device_id = "TL_N"
        self.light_s.device_id = "TL_S"
        self.light_e.device_id = "TL_E"
        self.light_w.device_id = "TL_W"

    def test_init_two_lights(self):
        """Инициализация с двумя противоположными светофорами."""
        intersection = Intersection("INT_2WAY", [self.light_n, self.light_s])

        self.assertFalse(intersection.is_intersection)
        self.assertEqual(len(intersection.lights), 2)
        self.assertEqual(intersection.conflict_map, {})

    def test_init_four_lights(self):
        """Инициализация с четырьмя светофорами (полный перекрёсток)."""
        intersection = Intersection("INT_4WAY", [
            self.light_n, self.light_s, self.light_e, self.light_w
        ])

        self.assertTrue(intersection.is_intersection)
        self.assertEqual(len(intersection.lights), 4)
        self.assertIn(Direction.NORTH, intersection.conflict_map)

    def test_init_invalid_lights_count(self):
        """Попытка создать перекрёсток с неправильным количеством светофоров."""
        with self.assertRaises(ValueError) as context:
            Intersection("INT_BAD", [self.light_n])
        self.assertIn("2 (противоположных), либо 4", str(context.exception))

    def test_regulate_intersection_emergency_priority(self):
        """Регулировка с приоритетом спецтранспорта."""
        intersection = Intersection("INT_TEST", [self.light_n, self.light_s])

        self.light_n.get_traffic_request.return_value = {
            "device_id": "TL_N", "priority": 100, "reason": "INCIDENT",
            "pedestrian_waiting": False
        }
        self.light_s.get_traffic_request.return_value = {
            "device_id": "TL_S", "priority": 10, "reason": "FLOW",
            "pedestrian_waiting": False
        }

        warning = intersection.regulate_intersection()

        self.assertTrue(warning)

        self.light_n.set_color.assert_called()
        self.light_s.set_color.assert_called()

    def test_regulate_intersection_four_way_conflict(self):
        """Регулировка полного перекрёстка с конфликтами направлений."""
        intersection = Intersection("INT_4WAY", [
            self.light_n, self.light_s, self.light_e, self.light_w
        ])

        for light in [self.light_n, self.light_s, self.light_e, self.light_w]:
            light.get_traffic_request.return_value = {
                "device_id": light.device_id, "priority": 10,
                "reason": "FLOW", "pedestrian_waiting": False
            }

        warning = intersection.regulate_intersection()

        self.assertFalse(warning)

        for light in [self.light_n, self.light_s, self.light_e, self.light_w]:
            light.set_color.assert_called()


class TestTrafficManager(unittest.TestCase):

    def setUp(self):
        self.tms = Mock(spec=TransportMonitoringSystem)
        self.tms.routes = {}
        self.tms.physical_stops = {}

        self.tm = TrafficManager(self.tms)

        self.light = Mock(spec=SmartTrafficLight)
        self.light.device_id = "TL_1"
        self.intersection = Intersection("INT_1", [self.light, Mock(spec=SmartTrafficLight)])

    def test_register_district_intersections(self):
        """Регистрация нескольких перекрёстков района."""
        self.tm.register_district_intersections([self.intersection])

        self.assertIn("INT_1", self.tm.intersections)

    def test_get_all_sensors(self):
        """Получение всех сенсоров района."""
        flow_sensor = Mock()
        for l in self.intersection.lights:
            l.flow_sensor = flow_sensor

        self.tm.register_district_intersections([self.intersection])
        sensors = self.tm.get_all_sensors()

        self.assertIn(flow_sensor, sensors)

    def test_link_stop_to_intersection_success(self):
        """Успешная связь остановки с перекрёстком."""
        stop_id = "STOP_1"
        self.tms.physical_stops[stop_id] = Mock()
        self.tm.intersections[self.intersection.intersection_id] = self.intersection

        result = self.tm.link_stop_to_intersection(
            stop_id, "INT_1", Direction.NORTH
        )

        self.assertIn("Связана остановка", result)
        self.assertIn(stop_id, self.tm.stop_intersection_map)
        self.assertEqual(self.tm.stop_intersection_map[stop_id], ("INT_1", Direction.NORTH))

    def test_link_stop_to_intersection_stop_not_found(self):
        """Связь с несуществующей остановкой."""
        with self.assertRaises(TransportException) as context:
            self.tm.link_stop_to_intersection("UNKNOWN", "INT_1", Direction.NORTH)
        self.assertIn("Остановка не найдена", str(context.exception))

    def test_link_stop_to_intersection_not_found(self):
        """Связь с несуществующим перекрёстком."""
        stop_id = "STOP_1"
        self.tms.physical_stops[stop_id] = Mock()

        with self.assertRaises(TransportException) as context:
            self.tm.link_stop_to_intersection(stop_id, "UNKNOWN", Direction.NORTH)
        self.assertIn("Перекресток не найден", str(context.exception))

    def test_link_stop_duplicate_direction(self):
        """Попытка связать вторую остановку с той же стороной перекрёстка."""
        stop1 = "STOP_1"
        stop2 = "STOP_2"
        self.tms.physical_stops[stop1] = Mock()
        self.tms.physical_stops[stop2] = Mock()
        self.tm.intersections[self.intersection.intersection_id] = self.intersection

        self.tm.link_stop_to_intersection(stop1, "INT_1", Direction.NORTH)

        with self.assertRaises(TransportException) as context:
            self.tm.link_stop_to_intersection(stop2, "INT_1", Direction.NORTH)
        self.assertIn("уже имеет остановку", str(context.exception))

    def test_prioritize_public_transport_no_vehicles(self):
        """Приоритет общественного транспорта, когда транспортных средств нет."""
        self.tms.routes = {}

        result = self.tm.prioritize_public_transport()
        self.assertIsNone(result)

    def test_prioritize_public_transport_non_public_vehicle(self):
        """Игнорирование личного транспорта."""

        vehicle = Mock(spec=PublicTransportVehicle)
        vehicle.vehicle_type = VehicleType.CAR
        vehicle.route_id = "R1"

        route = Mock(spec=TransportRoute)
        route.vehicles = [vehicle]
        route.stops = [Mock()]

        self.tms.routes = {"R1": route}

        result = self.tm.prioritize_public_transport()
        self.assertIsNone(result)

    def test_prioritize_public_transport_linked_stop(self):
        """Приоритет для общественного транспорта на связанной остановке."""

        vehicle = Mock(spec=PublicTransportVehicle)
        vehicle.vehicle_type = VehicleType.BUS
        vehicle.route_id = "R1"
        vehicle.get_last_stop_index = 0

        next_stop = Mock()
        next_stop.bus_stop.device_id = "STOP_LINKED"
        route = Mock(spec=TransportRoute)
        route.vehicles = [vehicle]
        route.stops = [Mock(), next_stop]

        self.tms.routes = {"R1": route}
        self.tms.physical_stops["STOP_LINKED"] = Mock()

        self.tm.intersections["INT_1"] = self.intersection
        self.tm.stop_intersection_map["STOP_LINKED"] = ("INT_1", Direction.NORTH)

        self.light.camera = Mock()

        result = self.tm.prioritize_public_transport()

        self.assertIn("Общественный транспорт", result)
        self.assertIn("BUS", result)

        self.light.camera.detect_event.assert_called_with(VehicleType.BUS, False)

    def test_grant_green_wave_intersection_not_found(self):
        """Обработка случая, когда перекрёсток не найден в системе."""
        result = self.tm._grant_green_wave(("NONEXISTENT_INT", Direction.NORTH), Mock())

        self.assertIn("ОШИБКА", result)
        self.assertIn("не найден", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
