import statistics
from datetime import datetime, timedelta
from typing import Optional

from environment import EnvironmentMonitoringSystem
from sensors import TrafficFlowSensor


class District:
    def __init__(self, district_id: str, environment_system: EnvironmentMonitoringSystem,
                 traffic_sensors: list[TrafficFlowSensor]):
        self.environment_system = environment_system
        self.traffic_sensors = traffic_sensors
        self.district_id = district_id
        self.metrics_readings: list[dict] = []
        self.last_updated: Optional[datetime] = None

    def auto_collect_sensor_data(self):
        ecology = self.environment_system.environmental_monitoring_operation()["average"]
        traffic = sum(t.get_status() for t in self.traffic_sensors) / len(self.traffic_sensors)
        self.metrics_readings.append({
            "ecology_score": ecology * 20,
            "transport_load": traffic,
            "infrastructure_density": 70,
            "timestamp": datetime.now()
        })
        self.last_updated = datetime.now()

    def get_average(self, metric, hours: int = 24):
        cutoff = datetime.now() - timedelta(hours=hours)
        values = [
            r[metric] for r in self.metrics_readings
            if r["timestamp"] >= cutoff
        ]
        return statistics.mean(values) if values else None
