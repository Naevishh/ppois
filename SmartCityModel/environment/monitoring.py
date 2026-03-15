from core import AirQualityLevel, TemperatureLevel, HumidityLevel, NoiseLevel
from sensors import AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor


class EnvironmentMonitoringSystem:
    def __init__(self, air_quality_sensors: list[AirQualitySensor], temperature_sensors: list[TemperatureSensor],
                 humidity_sensors: list[HumiditySensor], noise_sensors: list[NoiseSensor]):
        self.air_quality_sensors = air_quality_sensors
        self.temperature_sensors = temperature_sensors
        self.humidity_sensors = humidity_sensors
        self.noise_sensors = noise_sensors

    def environmental_monitoring_operation(self):
        def get_average(sensors):
            if not sensors:
                return 0
            return sum(s.get_status()[0] for s in sensors) / len(sensors)

        def get_level(enum_class, average):
            code = max(1, min(5, round(average)))
            return enum_class.from_code(code)

        results = {
            "air": get_level(AirQualityLevel, get_average(self.air_quality_sensors)),
            "temperature": get_level(TemperatureLevel, get_average(self.temperature_sensors)),
            "humidity": get_level(HumidityLevel, get_average(self.humidity_sensors)),
            "noise": get_level(NoiseLevel, get_average(self.noise_sensors)),
        }

        average_result = sum(val.code for val in results.values()) / len(results)
        results["average"] = average_result

        return results
