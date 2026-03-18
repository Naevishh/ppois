from city import SmartCity

class EnvironmentMonitoringUI:
    def __init__(self, city: SmartCity):
        self.city = city

    def get_environment_state(self, print_func):
        air, temp, humid, noise= [], [], [], []
        for dist in self.city.districts:
            air.extend(dist.air_quality_sensors)
            temp.extend(dist.temperature_sensors)
            humid.extend(dist.humidity_sensors)
            noise.extend(dist.noise_sensors)
        results = self.city.monitoring_system.environmental_monitoring_operation(air, temp, humid, noise)
        print_func("Состояние окружающей среды:"
                   f"\nКачество воздуха: {results["air"]}."
                   f"\nТемпература: {results["temperature"]}."
                   f"\nВлажность: {results["humidity"]}."
                   f"\nШум: {results["noise"]}.")

