from city import SmartCity
from core import SensorValueError
from ui import show_menu


class SensorUI:
    def __init__(self, city: SmartCity):
        self.city = city
        pass

    def update_sensor_data(self, print_func, get_user_input):
        ops = [(1, "Сенсоры уровня освещения"), (2, "Сенсоры движения"), (3, "Счетчик воды"),
               (4, "Сенсоры качества воздуха"), (5, "Сенсоры температуры"), (6, "Сенсоры влажности"),
               (7, "Сенсоры уровня шума"), (8, "AI-камера"), (9, "Сенсоры транспортного потока"),
               (10, "Сенсоры присутствия пешеходов"), (11, "Выход")]
        while True:
            key = show_menu(ops, print_func, get_user_input, "Выберите область сенсоров:")
            match key:
                case 1:
                    light_ops=[(sens_id, sens_id) for sens_id in self.city.light_sensors.keys()]
                    light_key = show_menu(light_ops, print_func, get_user_input, "Выберите сенсор:")
                    print_func("")
                    val=get_user_input()
                    if val:
                        try:
                            self.city.light_sensors[light_key].set_light_level(val)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 2:
                    motion_ops = [(sens_id, sens_id) for sens_id in self.city.motion_sensors.keys()]
                    light_key = show_menu(motion_ops, print_func, get_user_input, "Выберите сенсор:")
                    print_func("")
                    val = get_user_input()
                    if val:
                        try:
                            self.city.motion_sensors[light_key].detect_motion(val)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")

