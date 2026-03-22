class SmartLightningSystem:
    def __init__(self, smart_lights: list) -> None:
        self.smart_lights = smart_lights

    def optimize_lightning(self) -> None:
        for light in self.smart_lights:
            light.set_level()

    def get_energy_consumption(self) -> float:
        return sum(l.get_energy_consumption_estimate() for l in self.smart_lights)