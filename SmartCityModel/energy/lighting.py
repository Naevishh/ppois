from ui import show_menu


class SmartLightningSystem:
    def __init__(self, smart_lights: list):
        self.smart_lights = smart_lights

    def optimize_lightning(self):
        for light in self.smart_lights:
            light.set_level()

    def get_energy_consumption(self):
        return sum(l.get_energy_consumption_estimate() for l in self.smart_lights)

lis=["t", "k", "l"]
homes=[(i, home) for i,home in enumerate(lis, 1)]


if __name__=='__main__':
    j=0
    if j is None:
        print("oh no")
    o=input("enter space: ")
    if o is None:
        print("oh yes")
    print(f"'{o}'")