import time

from ..city import SmartCity
from .environment_ui import EnvironmentMonitoringUI
from .sensors_ui import SensorUI
from .transport_ui import TransportSystemUI, TrafficManagementUI
from ..core import show_menu
from .urban_planning_ui import UrbanPlanningDataAnalysisUI

class CityUI:
    def __init__(self) -> None:
        self.city = SmartCity()
        self.tms_ui = TransportSystemUI(self.city)
        self.traffic_ui = TrafficManagementUI(self.city)
        self.env_ui = EnvironmentMonitoringUI(self.city)
        self.urban_planning_ui = UrbanPlanningDataAnalysisUI(self.city)
        self.sensors_ui = SensorUI(self.city)

    def show_welcome(self, print_func) -> None:
        lines = [
            "========================================",
            "        SMART CITY MODEL v1.0",
            "     Система моделирования городской",
            "          инфраструктуры",
            "========================================",
            "",
            "      > Загрузка ядра...",
            "      > Подключение модулей...",
            "      > Система готова.",
            "",
            "      Нажмите Enter для входа"
        ]
        for line in lines:
            print_func(line)
            time.sleep(0.08)  # плавное появление по строкам

    def general_menu(self, get_user_input, print_func) -> None:
        # Показываем приветствие перед меню
        # self.show_welcome(print_func)
        # get_user_input()  # ждём Enter

        # Очищаем экран (опционально)
        # print_func('\n' * 2)

        ops = [(1, "Система общественного транспорта"), (2, "Управление движением"), (3, "Мониторинг окружающей среды"),
               (4, "Сбор и анализ данных"), (5, "Сенсоры")]
        while True:
            key = show_menu(ops, get_user_input, print_func, "Выберите область:")
            match key:
                case 1:
                    self.tms_ui.menu(get_user_input, print_func)
                case 2:
                    self.traffic_ui.menu(get_user_input, print_func)
                case 3:
                    self.env_ui.get_environment_state(print_func)
                case 4:
                    self.urban_planning_ui.print_report(print_func)
                case 5:
                    self.sensors_ui.update_sensor_data(get_user_input, print_func)
                case '':
                    return