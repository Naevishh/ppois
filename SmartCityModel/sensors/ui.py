from city import SmartCity
from core import SensorValueError, VehicleType
from sensors import AITrafficCamera
from ui import show_menu


class SensorUI:
    def __init__(self, city: SmartCity):
        self.city = city
        pass

    def detect_camera_event(self, get_user_input, print_func, camera: AITrafficCamera):
        ops = [(vehicle.name, vehicle.value) for vehicle in VehicleType]
        v_type = show_menu(ops, get_user_input, get_user_input, "Выберите тип транспорта:")
        if v_type:
            print_func("Случилась ли авария? Введите 'да', если случилась, если нет - нажмите пробел")
            incident = get_user_input()
            if incident:
                incident = incident == 1
                camera.detect_event(v_type, incident)

    def set_sensor_value(self, get_user_input, print_func, sensor, val_name):
        print_func(f"Введите показания ({val_name}):")
        value = get_user_input()
        try:
            sensor.set_value(value)
        except SensorValueError as e:
            print_func(f"Ошибка: {e}")

    def list_sensors(self, get_user_input, print_func, sensors, val_name):
        sensors_ops = [(i, sensor.sensor_id) for i, sensor in enumerate(sensors)]
        sensor_key = show_menu(sensors_ops, get_user_input, print_func, "Выберите сенсор")
        if sensor_key != '':
            self.set_sensor_value(get_user_input, print_func, sensors[sensor_key], val_name)

    def update_sensor_data(self, get_user_input, print_func):
        ops = [(dist_id, dist_id) for dist_id in self.city.districts.keys()]
        while True:
            dist_key = show_menu(ops, get_user_input, print_func, "Выберите район:")
            dist = self.city.districts[dist_key]

            ops_dist = [(1, "Сенсоры умного дома"), (2, "Сенсоры фонарей"), (3, "Сенсоры генераторов"),
                        (4, "Сенсоры качества воздуха"), (5, "Сенсоры температуры"), (6, "Сенсоры влажности"),
                        (7, "Сенсоры уровня шума"), (8, "Сенсоры транспорта"), (9, "Выход")]
            key = show_menu(ops_dist, get_user_input, print_func, "Выберите объекты:")

            match key:
                case 1:
                    homes = [(i, home.device_id) for i, home in enumerate(dist.smart_homes)]
                    home_index = show_menu(homes, get_user_input, print_func, "Выберите умный дом:")
                    if home_index == '':
                        break
                    home = dist.smart_homes[home_index]
                    home_ops = [(1, "Счетчик воды"), (2, "Сенсор термостата"),
                                (3, "Сенсоры уровня освещения в системе освещения")]
                    home_key = show_menu(home_ops, get_user_input, print_func)
                    match home_key:
                        case 1:
                            self.set_sensor_value(get_user_input, print_func, home.water_meter, "вода")
                        case 2:
                            self.set_sensor_value(get_user_input, print_func, home.thermostat.temp_sensor,
                                                  "температура")
                        case 3:
                            lights = [(i, light.device_id) for i, light in enumerate(home.lightning_system.lights)]
                            l_key = show_menu(lights, get_user_input, print_func, "Выберите источник света")
                            if l_key != '':
                                self.set_sensor_value(get_user_input, print_func, home.lights[l_key].light_level_sensor,
                                                      "уровень света")
                case 2:
                    lights = [(i, light.device_id) for i, light in enumerate(dist.lights)]
                    l_key = show_menu(lights, get_user_input, print_func, "Выберите фонарь")
                    if l_key != '':
                        self.set_sensor_value(get_user_input, print_func, dist.lights[l_key].light_level_sensor,
                                              "уровень света")
                case 3:
                    generators = [(1, "Сенсор солнечной панели"), (2, "Скорость ветра")]
                    gen_key = show_menu(generators, get_user_input, print_func, "Выберите генератор")
                    if gen_key == 1:
                        self.set_sensor_value(get_user_input, print_func, dist.generatiors[0].light_level_sensor,
                                              "уровень света")
                    elif gen_key == 2:
                        self.set_sensor_value(get_user_input, print_func, dist.generatiors[1],
                                              "скорость ветра")

                case 4:
                    self.list_sensors(get_user_input, print_func, dist.air_quality_sensors, "концентрация газа")
                case 5:
                    self.list_sensors(get_user_input, print_func, dist.temperature_sensors, "температура")
                case 6:
                    self.list_sensors(get_user_input, print_func, dist.humidity_sensors, "концентрация пара")
                case 7:
                    self.list_sensors(get_user_input, print_func, dist.noise_sensors, "уровень шума")
                case 8:
                    inters = [(i, inter.intersection_id) for i, inter in enumerate(dist.intersections)]
                    inters_key = show_menu(inters, get_user_input, print_func, "Выберите переход")
                    if inters_key != '':
                        inter_lights = dist.intersections[inters_key].lights
                        lights = [(light.device_id, light.device_id) for light in inter_lights.keys()]
                        light = show_menu(lights, get_user_input, print_func, "Выберите светофор")
                        if light != '':
                            light_ops = [(1, "AI-камера"), (2, "Сенсор транспортного потока"),
                                         (3, "Сенсор присутствия пешеходов")]
                            light_key = show_menu(light_ops, get_user_input, print_func)
                            match light_key:
                                case 1:
                                    self.detect_camera_event(get_user_input, print_func, inter_lights[light_key].camera)
                                case 2:
                                    self.set_sensor_value(get_user_input, print_func,
                                                          inter_lights[light_key].flow_sensor,
                                                          "поток (транспорта в минуту)")
                                case 3:
                                    self.set_sensor_value(get_user_input, print_func,
                                                          inter_lights[light_key].pedestrian_sensor,
                                                          "число пешеходов")
                case 9:
                    return
