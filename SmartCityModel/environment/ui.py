from .monitoring import EnvironmentMonitoringSystem


class EnvironmentMonitoringUI:
    def __init__(self, monitoring_system: EnvironmentMonitoringSystem):
        self.monitoring_system = monitoring_system

    def get_environment_state(self, print_func):
        results = self.monitoring_system.environmental_monitoring_operation()
        print_func("Состояние окружающей среды:"
                   f"\nКачество воздуха: {results["air"]}."
                   f"\nТемпература: {results["temperature"]}."
                   f"\nВлажность: {results["humidity"]}."
                   f"\nШум: {results["noise"]}.")
