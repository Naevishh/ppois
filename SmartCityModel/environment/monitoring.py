from ..core import AirQualityLevel, TemperatureLevel, HumidityLevel, NoiseLevel


class EnvironmentMonitoringSystem:
    def __init__(self) -> None:
        pass

    def environmental_monitoring_operation(self, air: list, temp: list, humid: list, noise: list) -> dict:
        def get_average(sensors: list) -> float:
            if not sensors:
                return 0
            return sum(s.get_status()[0] for s in sensors) / len(sensors)

        def get_level(enum_class, average: float):
            code = max(1, min(5, round(average)))
            return enum_class.from_code(code)

        results = {
            "air": get_level(AirQualityLevel, get_average(air)),
            "temperature": get_level(TemperatureLevel, get_average(temp)),
            "humidity": get_level(HumidityLevel, get_average(humid)),
            "noise": get_level(NoiseLevel, get_average(noise)),
        }

        average_result = sum(val.code for val in results.values()) / len(results)
        results["average"] = average_result

        return results