import time

from .energy_ui import EnergyUI
from .environment_ui import EnvironmentMonitoringUI
from .sensors_ui import SensorUI
from .services_ui import PublicServiceUI
from .transport_ui import TransportSystemUI, TrafficManagementUI
from .urban_planning_ui import UrbanPlanningDataAnalysisUI
from ..city import SmartCity


class CityUI:
    def __init__(self) -> None:
        self.city = SmartCity()
        self.tms_ui = TransportSystemUI(self.city)
        self.traffic_ui = TrafficManagementUI(self.city)
        self.env_ui = EnvironmentMonitoringUI(self.city)
        self.urban_planning_ui = UrbanPlanningDataAnalysisUI(self.city)
        self.sensors_ui = SensorUI(self.city)
        self.services_ui = PublicServiceUI(self.city)
        self.energy_ui = EnergyUI(self.city)