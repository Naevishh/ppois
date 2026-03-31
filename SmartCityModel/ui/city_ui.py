import time

from .energy_ui import EnergyUI
from .services_ui import PublicServiceUI
from ..city import SmartCity
from .environment_ui import EnvironmentMonitoringUI
from .sensors_ui import SensorUI
from .transport_ui import TransportSystemUI, TrafficManagementUI
from .urban_planning_ui import UrbanPlanningDataAnalysisUI

class CityUI:
    def __init__(self) -> None:
        self.city = SmartCity()
        self.tms_ui = TransportSystemUI(self.city)
        self.traffic_ui = TrafficManagementUI(self.city)
        self.env_ui = EnvironmentMonitoringUI(self.city)
        self.urban_planning_ui = UrbanPlanningDataAnalysisUI(self.city)
        self.sensors_ui = SensorUI(self.city)
        self.services_ui=PublicServiceUI(self.city)
        self.energy_ui=EnergyUI(self.city)

    def show_welcome(self, print_func) -> None:
        lines = [
            "========================================",
            "        SMART CITY MODEL v1.0",
            "     Система моделирования городской",
            "          инфраструктуры",
            "========================================",
            "",
            "      > Загрузка ядра...",
            "      > Подключение модулей...",
            "      > Система готова.",
            "",
            "      Нажмите Enter для входа"
        ]
        for line in lines:
            print_func(line)
            time.sleep(0.08)  # плавное появление по строкам