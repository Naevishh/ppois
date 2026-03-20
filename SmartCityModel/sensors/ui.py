from city import SmartCity
from core import SensorValueError
from ui import show_menu


class SensorUI:
    def __init__(self, city: SmartCity):
        self.city = city
        pass

    def set_sensor_value(self, print_func, get_user_input, sensor, val_name):
        print_func(f"Введите показания ({val_name}):")
        value = get_user_input()
        try:
            sensor.set_value(value)
        except SensorValueError as e:
            print_func(f"Ошибка: {e}")

    def update_sensor_data(self, print_func, get_user_input):
        ops = [(dist_id, dist_id) for dist_id in self.city.districts.keys()]
        while True:
            dist_key = show_menu(ops, print_func, get_user_input, "Выберите район:")
            ops_dist = [(1, "Сенсоры уровня освещения"), (2, "Сенсоры движения"), (3, "Счетчик воды"),
                   (4, "Сенсоры качества воздуха"), (5, "Сенсоры температуры"), (6, "Сенсоры влажности"),
                   (7, "Сенсоры уровня шума"), (8, "AI-камера"), (9, "Сенсоры транспортного потока"),
                   (10, "Сенсоры присутствия пешеходов"), (11, "Выход")]
            dist=self.city.districts[dist_key]

            ops_dist= [(1, "Сенсоры умного дома"), (2, "Сенсоры фонарей"), (3, "Сенсоры генераторов"),(4, "Сенсоры качества воздуха"), (5, "Сенсоры температуры"), (6, "Сенсоры влажности"),
                   (7, "Сенсоры уровня шума"), (8, "Сенсоры транспорта"), (9, "Выход")]
            key = show_menu(ops_dist, print_func, get_user_input, "Выберите объекты:")

            match key:
                case 1:
                    homes=[(i, home.device_id) for i,home in enumerate(dist.smart_homes,1)]
                    home_index = show_menu(homes, print_func, get_user_input, "Выберите умный дом:")
                    if home_index == '':
                        break
                    home=dist.smart_homes[home_index-1]
                    home_ops=[(1, "Счетчик воды"), (2, "Сенсор термостата"), (3, "Сенсоры уровня освещения в системе освещения")]
                    home_key=show_menu(home_ops, print_func, get_user_input)
                    match home_key:
                        case 1:
                            print_func("Введите показания воды:")
                            water=get_user_input()
                            try:
                                home.water_meter.set_water_volume(water)
                            except SensorValueError as e:
                                print_func(f"Ошибка: {e}")
                        case 2:
                            print_func("Введите показания температуры:")
                            temp = get_user_input()
                            try:
                                home.thermostat.temp_sensor.set_temperature(temp)
                            except SensorValueError as e:
                                print_func(f"Ошибка: {e}")
                        case 3:
                            lights = [(i, light.device_id) for i, light in enumerate(home.lightning_system.lights,1)]
                            l_key=show_menu(lights, print_func, get_user_input, "Выберите источник света")
                            if l_key != '':
                                print_func("Введите показания уровня света:")
                                light_level = get_user_input()
                                try:
                                    home.lights[l_key-1].light_level_sensor.set_light_level(light_level)
                                except SensorValueError as e:
                                    print_func(f"Ошибка: {e}")

                case 2:
                    lights = [(i, light.device_id) for i, light in enumerate(dist.lights, 1)]
                    l_key = show_menu(lights, print_func, get_user_input, "Выберите фонарь")
                    if l_key != '':
                        print_func("Введите показания уровня света:")
                        light_level = get_user_input()
                        try:
                            dist.lights[l_key-1].light_level_sensor.set_light_level(light_level)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 3:
                    generators = [(1, "Сенсор солнечной панели"), (2, "Скорость ветра")]
                    gen_key = show_menu(generators, print_func, get_user_input, "Выберите генератор")
                    if gen_key == 1:
                        print_func("Введите показания уровня света:")
                        light_level = get_user_input()
                        try:
                            dist.generatiors[0].light_level_sensor.set_light_level(light_level)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                    elif gen_key == 2:
                        print_func("Введите показания скорости ветра:")
                        wind_speed = get_user_input()
                        try:
                            dist.generatiors[1].set_wind_speed(wind_speed)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 4:
                    air_sensors = [(i, sensor.sensor_id) for i, sensor in enumerate(dist.air_quality_sensors, 1)]
                    air_key = show_menu(air_sensors, print_func, get_user_input, "Выберите сенсор")
                    if air_key != '':
                        print_func("Введите показания концентрации газа:")
                        concentration = get_user_input()
                        try:
                            dist.air_quality_sensors[air_key-1].set_concentration(concentration)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 5:
                    temp_sensors = [(i, sensor.sensor_id) for i, sensor in enumerate(dist.temperature_sensors, 1)]
                    temp_key = show_menu(temp_sensors, print_func, get_user_input, "Выберите сенсор")
                    if temp_key != '':
                        print_func("Введите показания температуры:")
                        temp = get_user_input()
                        try:
                            dist.temperature_sensors[temp_key-1].set_temperature(temp)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 6:
                    humid_sensors = [(i, sensor.sensor_id) for i, sensor in enumerate(dist.humidity_sensors, 1)]
                    humid_key = show_menu(humid_sensors, print_func, get_user_input, "Выберите сенсор")
                    if humid_key != '':
                        print_func("Введите показания концентрации пара")
                        concentration = get_user_input()
                        try:
                            dist.humidity_sensors[humid_key-1].set_vapor_concentration(concentration)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 7:
                    noise_sensors = [(i, sensor.sensor_id) for i, sensor in enumerate(dist.air_quality_sensors, 1)]
                    air_key = show_menu(noise_sensors, print_func, get_user_input, "Выберите сенсор")
                    if air_key != '':
                        print_func("Введите показания концентрации газа:")
                        concentration = get_user_input()
                        try:
                            dist.air_quality_sensors.set_concentration(concentration)
                        except SensorValueError as e:
                            print_func(f"Ошибка: {e}")
                case 7:
                case 8:




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

                case 3:

