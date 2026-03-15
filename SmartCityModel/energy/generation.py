from core import SmartDevice, Domain


class SolarPanel:
    def __init__(self, light_level_sensor):
        self.light_level_sensor = light_level_sensor

    def produce_electricity(self):
        light_level = self.light_level_sensor.get_status()
        # Выработка энергии пропорциональна уровню освещения (0-100%)
        return light_level * 0.5  # например, 50 Вт при 100% света


class WindTurbine:
    def __init__(self):
        self._wind_speed = 0

    def set_wind_speed(self, wind_speed: int):
        self._wind_speed = wind_speed

    def produce_electricity(self):
        # Выработка энергии начинается с определённой скорости ветра
        if self._wind_speed < 3:
            return 0  # слишком слабый ветер
        elif self._wind_speed > 25:
            return 0  # слишком сильный ветер (опасно)
        else:
            return (self._wind_speed - 3) * 10  # например, 10 Вт на каждый м/с


class BatteryStorage(SmartDevice):
    def __init__(self, device_id: str, capacity: int):
        super().__init__(device_id, Domain.INFRASTRUCTURE)
        self.capacity = capacity  # Максимальная емкость в Вт*ч
        self.current_charge = 0  # Текущий заряд
        self._is_charging = False

    def store_energy(self, amount: int):
        """Принять излишки энергии от солнечных панелей"""
        if self.current_charge + amount <= self.capacity:
            self.current_charge += amount
            return amount
        else:
            # Батарея полная, возвращаем сколько не влезло (потери)
            added = self.capacity - self.current_charge
            self.current_charge = self.capacity
            return added

    def release_energy(self, amount: int):
        """Отдать энергию в сеть при пиковом потреблении"""
        if self.current_charge >= amount:
            self.current_charge -= amount
            return amount
        return 0  # Батарея разряжена

    def get_charge_percentage(self):
        return (self.current_charge / self.capacity) * 100
