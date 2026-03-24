import random

from ..citizens import UserRepository
from ..core import VehicleType, StringValidator, Direction
from ..energy import SmartThermostat, SmartHome, SolarPanel, WindTurbine, BatteryStorage, SmartLight, CityEnergyGrid
from ..energy.lighting import SmartLightningSystem
from ..environment.monitoring import EnvironmentMonitoringSystem
from ..sensors import TemperatureSensor, AirQualitySensor, HumiditySensor, NoiseSensor, TrafficFlowSensor, \
    AITrafficCamera, PedestrianCrossingSensor, MotionSensor, LightLevelSensor, WaterMeter, ElectricityMeter
from ..services import Hospital, EducationService, UtilitiesService
from ..transport import TransportMonitoringSystem, BusStop, PublicTransportVehicle, TransportRoute, RouteStop, \
    Intersection, SmartTrafficLight, TrafficManager
from ..urban_planning import UrbanPlanningDataAnalyzer, District

class SmartCity:
    def __init__(self) -> None:
        self.validator = StringValidator(min_length=1, max_length=50)

        self.tms = TransportMonitoringSystem()
        self.analyzer = UrbanPlanningDataAnalyzer()
        self.districts: dict[str, District] = {}
        self.traffic_manager = TrafficManager(self.tms)
        self.monitoring_system = EnvironmentMonitoringSystem()
        self.energy_grid = self._init_energy()
        self._init_services()
        self._init_tms()

        self._initialize_default_data()
        self._init_traffic()

    def _initialize_default_data(self) -> None:
        dist1 = self._create_district("center_1")
        dist2 = self._create_district("suburb_1")
        dist3 = self._create_district("suburb_2")
        dists: list[District] = [dist1, dist2, dist3]
        self.districts = {dist.district_id: dist for dist in dists}
        for dist in self.districts.values():
            self.traffic_manager.register_district_intersections(dist.intersections)
            self.analyzer.register_district(dist)

    def _create_district(self, dist_id: str) -> District:
        light_sensor: list[LightLevelSensor] = [LightLevelSensor() for _ in range(13)]

        motion_sensor: list[MotionSensor] = [MotionSensor() for _ in range(12)]

        temp_sensors: list[TemperatureSensor] = [TemperatureSensor() for _ in range(2)]

        # === Генераторы (generators) ===
        solar_panel = SolarPanel(light_sensor[0])
        wind_turbine = WindTurbine()
        generators: list[SolarPanel | WindTurbine] = [solar_panel, wind_turbine]

        # === Хранилища (storages) ===
        battery_1 = BatteryStorage(capacity=1000)
        battery_2 = BatteryStorage(capacity=1500)
        storages: list[BatteryStorage] = [battery_1, battery_2]

        # === Потребители (consumers) ===
        # Умное освещение
        smart_lights_1: list[SmartLight] = [SmartLight(light_sensor[i + 1], motion_sensor[i]) for i in range(4)]
        lighting_system_1 = SmartLightningSystem(smart_lights_1)
        smart_lights_2: list[SmartLight] = [SmartLight(light_sensor[i + 5], motion_sensor[i + 4]) for i in range(4)]
        lighting_system_2 = SmartLightningSystem(smart_lights_2)
        street_lights: list[SmartLight] = [SmartLight(light_sensor[i + 9], motion_sensor[i + 8]) for i in range(4)]

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

        lights1: list[SmartTrafficLight] = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in range(4)]
        lights2: list[SmartTrafficLight] = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in range(2)]
        lights3: list[SmartTrafficLight] = [SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera(), PedestrianCrossingSensor()) for _ in range(4)]

        inter_1 = Intersection(f"{dist_id}_1", lights1)
        cross_2 = Intersection(f"{dist_id}_2", lights2)
        inter_3 = Intersection(f"{dist_id}_3", lights3)
        inters: list[Intersection] = [inter_1, cross_2, inter_3]

        traffic_sensors: list[TrafficFlowSensor] = [TrafficFlowSensor() for _ in range(2)]
        temp_sensors_list: list[TemperatureSensor] = [TemperatureSensor() for _ in range(2)]
        air_sensors: list[AirQualitySensor] = [AirQualitySensor() for _ in range(2)]
        humid_sensors: list[HumiditySensor] = [HumiditySensor(temp_sensors_list[i]) for i in range(2)]
        noise_sensors: list[NoiseSensor] = [NoiseSensor() for _ in range(2)]

        return District(dist_id, air_sensors, temp_sensors_list, humid_sensors, noise_sensors, traffic_sensors, inters,
                        [smart_home_1, smart_home_2], street_lights, storages, generators)

    def _init_services(self) -> None:
        self.hospital = Hospital("Поликлинника №1", ("Гришина", 3), "h_01")
        self.educational_service = EducationService("Гимназия №1",
                                                    ("Ленина", 45), "sch_01")
        self.user_repo = UserRepository()
        self.utility_services = UtilitiesService("Коммунальная служба №1",
                                                 ("Пушкина", 24), "ut_01")

    def _init_tms(self) -> None:
        physical_stops: list[BusStop] = [
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

        vehicles: list[PublicTransportVehicle] = [
            PublicTransportVehicle(VehicleType.BUS, "r1"),
            PublicTransportVehicle(VehicleType.BUS, "r2"),
            PublicTransportVehicle(VehicleType.TRAM, "r3")
        ]
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

        for veh, route in zip(vehicles, self.tms.routes.values()):
            route.add_vehicle(veh)

    def _init_traffic(self) -> None:
        all_intersection_ids: list[str] = []
        for dist in self.districts.values():
            for inter in dist.intersections:
                self.traffic_manager.intersections[inter.intersection_id]=inter
                all_intersection_ids.append(inter.intersection_id)

        for inter_id, stop_id in zip(all_intersection_ids, self.tms.physical_stops.keys()):
            self.traffic_manager.link_stop_to_intersection(
                stop_id,
                inter_id,
                random.choice(list(Direction))
            )

    def _init_energy(self) -> CityEnergyGrid:
        generators: list = []
        storages: list = []
        consumers: list = []
        for dist in self.districts.values():
            generators.extend(dist.generators)
            storages.append(dist.storages)
            consumers.extend(dist.smart_homes + dist.lights)

        return CityEnergyGrid(generators, storages, consumers)
