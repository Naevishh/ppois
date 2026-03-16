from city import SmartCity
from .monitoring import EnvironmentMonitoringSystem


class EnvironmentMonitoringUI:
    def __init__(self, city: SmartCity):
        self.city = city

    def get_environment_state(self, print_func):
        results = self.city.monitoring_system.monitor_all()
        print_func("Состояние окружающей среды:"
                   f"\nКачество воздуха: {results["air"]}."
                   f"\nТемпература: {results["temperature"]}."
                   f"\nВлажность: {results["humidity"]}."
                   f"\nШум: {results["noise"]}.")
