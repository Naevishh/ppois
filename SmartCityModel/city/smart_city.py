from citizens import UserRepository
from core import VehicleType
from environment import EnvironmentMonitoringSystem
from sensors import TemperatureSensor, AirQualitySensor, HumiditySensor, NoiseSensor, TrafficFlowSensor, \
    AITrafficCamera, PedestrianCrossingSensor
from services import Hospital, EducationService, UtilitiesService
from transport import TransportMonitoringSystem, BusStop, PublicTransportVehicle, TransportRoute, RouteStop, \
    Intersection, SmartTrafficLight, TrafficManager
from transport.ui import TransportSystemUI, TrafficManagementUI
from urban_planning import UrbanPlanningDataAnalyzer, District


class SmartCity:
    def __init__(self):
        self.tms = TransportMonitoringSystem()
        self.analyzer = UrbanPlanningDataAnalyzer()
        self.districts=[]
        self.traffic_manager = TrafficManager(self.tms)
        self.monitoring_system = EnvironmentMonitoringSystem()

        self._initialize_default_data()

    def _initialize_default_data(self):
        dist1=self._create_district("center_1")
        dist2 = self._create_district("suburb_1")
        dist3 = self._create_district("suburb_2")
        self.districts=[dist1, dist2, dist3]
        for dist in self.districts:
            self.traffic_manager.register_district(dist)
            self.analyzer.register_district(dist)

    def _create_district(self, dist_id: str):
        lights1 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(4)]
        lights2 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(2)]
        lights3 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(4)]

        inter_1 = Intersection(f"{dist_id}_1", lights1)
        cross_2 = Intersection(f"{dist_id}_2", lights2)
        inter_3 = Intersection(f"{dist_id}_3", lights3)
        inters=[inter_1, cross_2, inter_3]

        traffic_sensors=[TrafficFlowSensor() for _ in range(2)]
        temp_sensors = [TemperatureSensor() for _ in range(2)]
        air_sensors = [AirQualitySensor() for _ in range(2)]
        humid_sensors = [HumiditySensor(temp_sensors[i]) for i in range(2)]
        noise_sensors = [NoiseSensor() for _ in range(2)]

        return District(dist_id, air_sensors, temp_sensors, humid_sensors, noise_sensors, traffic_sensors, inters)

    def _init_services(self):
        self.hospital = Hospital("Поликлинника №1", ("Гришина", 3), "h_01")
        self.educational_service = EducationService("Гимназия №1",
                                                    ("Ленина", 45), "sch_01")
        self.utility_services = UtilitiesService("Коммунальная служба №1",
                                                 ("Пушкина", 24), "ut_01")

    def _init_tms(self):
        self.tms.physical_stops = {
            "s1": BusStop("s1", "Пл. Ленина"),
            "s2": BusStop("s2", "Универмаг"),
            "s3": BusStop("s3", "Парк Горького"),
            "s4": BusStop("s4", "Вокзал"),
            "s5": BusStop("s5", "Пл. Победы"),
            "s6": BusStop("s6", "Пл. Якуба Коласа"),
            "s7": BusStop("s7", "Комаровский Рынок"),
            "s8": BusStop("s8", "Ст. метро Петровщина")
        }
        self.tms.vehicles = {
            "bus_1": PublicTransportVehicle("bus_1", VehicleType.BUS, "r1"),
            "bus_2": PublicTransportVehicle("bus_2", VehicleType.BUS, "r2"),
            "tram_3": PublicTransportVehicle("tram_3", VehicleType.TRAM, "r3")
        }
        self.tms.routes = {
            "r1": TransportRoute("r1", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i < len(self.tms.physical_stops) - 2], avg_time_between_stops=4),
            "r2": TransportRoute("r2", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i % 2 == 0], avg_time_between_stops=8),
            "r3": TransportRoute("r3", [RouteStop(self.tms.physical_stops[stop_id], i)
                                        for i, stop_id in enumerate(self.tms.physical_stops, 1)
                                        if i > 2], avg_time_between_stops=4)
        }

    def _init_energy(self):


class CityUI:
    def __init__(self):
        self.city=SmartCity()
        self.tms_ui=TransportSystemUI(self.city)
        self.traffic_ui=TrafficManagementUI(self.city)