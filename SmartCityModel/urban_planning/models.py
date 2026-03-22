import statistics
from datetime import datetime, timedelta
from typing import Optional

from energy import SmartHome, BatteryStorage, SmartLight
from sensors import TrafficFlowSensor, AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor
from transport import Intersection


class District:
    def __init__(self, district_id: str, air_quality_sensors: list[AirQualitySensor],
                 temperature_sensors: list[TemperatureSensor],
                 humidity_sensors: list[HumiditySensor],
                 noise_sensors: list[NoiseSensor],
                 traffic_sensors: list[TrafficFlowSensor],
                 intersections: list[Intersection],
                 smart_homes: list[SmartHome],
                 lights: list[SmartLight],
                 storages: list[BatteryStorage],
                 generators: list) -> None:
        self.air_quality_sensors = air_quality_sensors
        self.temperature_sensors = temperature_sensors
        self.humidity_sensors = humidity_sensors
        self.noise_sensors = noise_sensors
        self.traffic_sensors = traffic_sensors
        self.intersections = intersections
        self.smart_homes = smart_homes
        self.lights = lights
        self.storages = storages
        self.generators = generators
        self.district_id = district_id
        self.metrics_readings: list[dict] = []
        self.last_updated: Optional[datetime] = None

    def register_intersection(self, intersection: Intersection) -> None:
        self.intersections.append(intersection)

    def auto_collect_sensor_data(self, ecology: float) -> None:
        # ecology = self.environment_system.environmental_monitoring_operation()["average"]
        traffic = sum(t.get_status() for t in self.traffic_sensors) / len(self.traffic_sensors)
        self.metrics_readings.append({
            "ecology_score": ecology * 20,
            "transport_load": traffic,
            "infrastructure_density": 70,
            "timestamp": datetime.now()
        })
        self.last_updated = datetime.now()

    def get_average(self, metric: str, hours: int = 24) -> float | None:
        cutoff = datetime.now() - timedelta(hours=hours)
        values = [
            r[metric] for r in self.metrics_readings
            if r["timestamp"] >= cutoff
        ]
        return statistics.mean(values) if values else None

    def get_all_intersections(self) -> list[Intersection]:
        return list(self.intersections)