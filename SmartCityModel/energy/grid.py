from .lighting import SmartLightningSystem


class CityEnergyGrid:
    def __init__(self, generators: list, storages: list, consumers: list):
        self.generators = generators  # SolarPanel, WindTurbine
        self.storages = storages  # BatteryStorage
        self.consumers = consumers  # SmartStreetLight, SmartHome

    def balance_energy(self):
        """Главный цикл оптимизации"""
        # 1. Считаем производство
        total_production = sum(g.produce_electricity() for g in self.generators)

        # 2. Считаем базовое потребление
        total_consumption = sum(c.get_energy_consumption() for c in self.consumers)

        surplus = total_production - total_consumption

        # 3. Распределяем излишки
        if surplus > 0:
            for battery in self.storages:
                surplus -= battery.store_energy(surplus)
                if surplus <= 0:
                    break
        elif surplus < 0:
            # Если не хватает, берем из батарей
            needed = abs(surplus)
            for battery in self.storages:
                needed -= battery.release_energy(needed)
                if needed <= 0:
                    break

            if needed > 0:
                print(f"Warning: Дефицит энергии {needed} Вт, подключение к внешней сети")

    def optimize_all(self):
        """Вызывает оптимизацию на всех устройствах"""
        for system in self.consumers:
            if isinstance(system, SmartLightningSystem):
                system.optimize_lightning()
        self.balance_energy()
