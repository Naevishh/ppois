import random

from citizens import UserRepository
from core import VehicleType, StringValidator, Direction
from energy import SmartThermostat, SmartHome, SolarPanel, WindTurbine, BatteryStorage, SmartLight, CityEnergyGrid
from energy.lighting import SmartLightningSystem
from environment import EnvironmentMonitoringSystem, EnvironmentMonitoringUI
from sensors import TemperatureSensor, AirQualitySensor, HumiditySensor, NoiseSensor, TrafficFlowSensor, \
    AITrafficCamera, PedestrianCrossingSensor, MotionSensor, LightLevelSensor, WaterMeter, ElectricityMeter
from sensors.ui import SensorUI
from services import Hospital, EducationService, UtilitiesService
from transport import TransportMonitoringSystem, BusStop, PublicTransportVehicle, TransportRoute, RouteStop, \
    Intersection, SmartTrafficLight, TrafficManager
from transport.ui import TransportSystemUI, TrafficManagementUI
from urban_planning import UrbanPlanningDataAnalyzer, District, UrbanPlanningDataAnalysisUI


class SmartCity:
    def __init__(self):
        self.validator = StringValidator(min_length=1, max_length=50)

        self.tms = TransportMonitoringSystem()
        self.analyzer = UrbanPlanningDataAnalyzer()
        self.districts = dict[str, District]
        self.traffic_manager = TrafficManager(self.tms)
        self.monitoring_system = EnvironmentMonitoringSystem()
        self.energy_grid = self._init_energy()
        self._init_services()
        self._init_tms()

        self._initialize_default_data()
        self._init_traffic()

    def _initialize_default_data(self):
        dist1 = self._create_district("center_1")
        dist2 = self._create_district("suburb_1")
        dist3 = self._create_district("suburb_2")
        dists = [dist1, dist2, dist3]
        self.districts = {dist.district_id: dist for dist in dists}
        for dist in self.districts.values():
            self.traffic_manager.register_district(dist)
            self.analyzer.register_district(dist)

    def _create_district(self, dist_id: str):

        light_sensor = [LightLevelSensor() for _ in range(13)]
        self.light_sensors = {sens.sensor_id: sens for sens in light_sensor}

        motion_sensor = [MotionSensor() for _ in range(12)]
        self.motion_sensors = {sens.sensor_id: sens for sens in motion_sensor}

        temp_sensors=[TemperatureSensor() for _ in range(2)]

        # === Генераторы (generators) ===
        solar_panel = SolarPanel(light_sensor[0])
        wind_turbine = WindTurbine()
        generators = [solar_panel, wind_turbine]

        # === Хранилища (storages) ===
        battery_1 = BatteryStorage(capacity=1000)
        battery_2 = BatteryStorage(capacity=1500)
        storages = [battery_1, battery_2]

        # === Потребители (consumers) ===
        # Умное освещение
        smart_lights_1 = [SmartLight(light_sensor[i + 1], motion_sensor[i]) for i in range(4)]
        lighting_system_1 = SmartLightningSystem(smart_lights_1)
        smart_lights_2 = [SmartLight(light_sensor[i + 5], motion_sensor[i + 4]) for i in range(4)]
        lighting_system_2 = SmartLightningSystem(smart_lights_2)
        street_lights = [SmartLight(light_sensor[i + 9], motion_sensor[i + 8]) for i in range(4)]

        # Умные дома
        water_meter_1 = WaterMeter()
        electricity_meter_1 = ElectricityMeter()
        thermostat_1 = SmartThermostat(temp_sensors[0])
        smart_home_1 = SmartHome(
            ("Ленина", 10),
            water_meter_1,
            electricity_meter_1,
            thermostat_1,
            lighting_system_1
        )

        water_meter_2 = WaterMeter()
        electricity_meter_2 = ElectricityMeter()
        thermostat_2 = SmartThermostat(temp_sensors[1])
        smart_home_2 = SmartHome(
            ("Гагарина", 25),
            water_meter_2,
            electricity_meter_2,
            thermostat_2,
            lighting_system_2
        )

        lights1 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(4)]
        lights2 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(2)]
        lights3 = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in
                   range(4)]

        inter_1 = Intersection(f"{dist_id}_1", lights1)
        cross_2 = Intersection(f"{dist_id}_2", lights2)
        inter_3 = Intersection(f"{dist_id}_3", lights3)
        inters = [inter_1, cross_2, inter_3]

        traffic_sensors = [TrafficFlowSensor() for _ in range(2)]
        temp_sensors = [TemperatureSensor() for _ in range(2)]
        air_sensors = [AirQualitySensor() for _ in range(2)]
        humid_sensors = [HumiditySensor(temp_sensors[i]) for i in range(2)]
        noise_sensors = [NoiseSensor() for _ in range(2)]

        return District(dist_id, air_sensors, temp_sensors, humid_sensors, noise_sensors, traffic_sensors, inters,
                        [smart_home_1, smart_home_2], street_lights, storages, generators)

    def _init_services(self):
        self.hospital = Hospital("Поликлинника №1", ("Гришина", 3), "h_01")
        self.educational_service = EducationService("Гимназия №1",
                                                    ("Ленина", 45), "sch_01")
        self.user_repo = UserRepository()
        self.utility_services = UtilitiesService("Коммунальная служба №1",
                                                 ("Пушкина", 24), "ut_01")

    def _init_tms(self):
        physical_stops = [
            BusStop("Пл. Ленина"),
            BusStop("Универмаг"),
            BusStop("Парк Горького"),
            BusStop("Вокзал"),
            BusStop("Пл. Победы"),
            BusStop("Пл. Якуба Коласа"),
            BusStop("Комаровский Рынок"),
            BusStop("Ст. метро Петровщина")
        ]
        self.tms.physical_stops = {stop.device_id: stop for stop in physical_stops}

        vehicles = [PublicTransportVehicle(VehicleType.BUS, "r1"),
                    PublicTransportVehicle(VehicleType.BUS, "r2"),
                    PublicTransportVehicle(VehicleType.TRAM, "r3")]
        self.tms.vehicles = {vehicle.device_id: vehicle for vehicle in vehicles}
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

    def _init_traffic(self):
        all_intersection_ids = []
        for dist in self.districts.values():
            for inter in dist.intersections:
                all_intersection_ids.append(inter.intersection_id)

        for inter_id, stop_id in zip(all_intersection_ids, self.tms.physical_stops.keys()):
            self.traffic_manager.link_stop_to_intersection(
                stop_id,
                inter_id,
                random.choice(list(Direction))
            )

    def _init_energy(self):
        generators=[]
        storages=[]
        consumers=[]
        for dist in self.districts.values():
            generators.extend(dist.generators)
            storages.append(dist.storages)
            consumers.extend(dist.smart_homes+dist.lights)

        return CityEnergyGrid(generators, storages, consumers)


class CityUI:
    def __init__(self):
        self.city = SmartCity()
        self.tms_ui = TransportSystemUI(self.city)
        self.traffic_ui = TrafficManagementUI(self.city)
        self.env_ui = EnvironmentMonitoringUI(self.city)
        self.urban_planning_ui = UrbanPlanningDataAnalysisUI(self.city)
        self.sensors_ui=SensorUI(self.city)

    def general_menu(self):
