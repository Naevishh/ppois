# SmartCityModel/cli.py

import typer
from .ui.city_ui import CityUI
from .core.helpers import smooth_print, print_help

app = typer.Typer(
    name="smartcity",
    help="Модель умного города",
    add_completion=False
)

VERSION = "1.0.0"

# Сопоставление команд с методами CityUI
MODULE_MAP = {
    "tms": ("tms_ui", "menu"),
    "traffic": ("traffic_ui", "menu"),
    "env": ("env_ui", "get_environment_state"),
    "data": ("urban_planning_ui", "print_report"),
    "sensors": ("sensors_ui", "update_sensor_data"),
}


def print_welcome():
    """Вывод приветственного экрана"""
    text = (
        "========================================\n"
        f"        SMART CITY MODEL v{VERSION}\n"
        "     Система моделирования городской\n"
        "          инфраструктуры\n"
        "========================================\n"
        "\n"
        "      > Загрузка ядра...\n"
        "      > Подключение модулей...\n"
        "      > Система готова.\n"
    )
    smooth_print(text, print, char_delay=0.015, line_delay=0.03)

modules = [
    ("tms", "Система управления общественным транспортом"),
    ("traffic", "Дорожное движение"),
    ("env", "Окружающая среда"),
    ("data", "Анализ данных города"),
    ("sensors", "Задание значений сенсоров"),
    ("services", "Общественные сервисы")
]

tms_options = [
    (1, "--add-route", "Добавить маршрут"),
    (2, "--add-vehicle", "Добавить транспортное средство"),
    (3, "--add-stop", "Добавить остановку"),
    (4, "--update-location", "Обновить локацию средства"),
    (5, "--arrive-stop", "Прийти на остановку"),
    (6, "--view-routes", "Посмотреть маршруты")
]

traffic_options = [
    (1, "--add-intersection", "Добавить перекресток"),
    (2, "--accident", "Попасть в аварию"),
    (3, "--manage-flow", "Управление транспортным потоком")
]

sensors_options = [
    ("--smart-home", "Сенсоры умного дома"),
    ("--street-lights", "Сенсоры фонарей"),
    ("--generators", "Сенсоры генераторов"),
    ("--air-quality", "Сенсоры качества воздуха"),
    ("--temperature", "Сенсоры температуры"),
    ("--humidity", "Сенсоры влажности"),
    ("--noise-level", "Сенсоры уровня шума")
]

service_actions = [
    ("--hospital", "Больница"),
    ("--school", "Школа"),
    ("--utility", "Коммунальные услуги")
]

commands = {
    "tms": {
        "--add-route": "Добавить маршрут",
        "--add-vehicle": "Добавить транспортное средство",
        "--add-stop": "Добавить остановку",
        "--update-location": "Обновить локацию средства",
        "--arrive-stop": "Прийти на остановку",
        "--view-routes": "Посмотреть маршруты"
    },

    "traffic": {
        "--add-intersection": "Добавить перекресток",
        "--accident": "Попасть в аварию",
        "--manage-flow": "Управление транспортным потоком"
    },

    "env": {"--get-env-state": "Получить состояние среды"},
    "data": {"--print-report": "Распечатать отчет"},

    "sensors": {
        "--smart-home": "Сенсоры умного дома",
        "--street-lights": "Сенсоры фонарей",
        "--generators": "Сенсоры генераторов",
        "--air-quality": "Сенсоры качества воздуха",
        "--temperature": "Сенсоры температуры",
        "--humidity": "Сенсоры влажности",
        "--noise-level": "Сенсоры уровня шума"
    },

    "services": {
        "--hospital": "Больница",
        "--school": "Школа",
        "--utility": "Коммунальные услуги",
        "--exit": "Выйти"
    }
}

def run_module(city_ui: CityUI, module_name: str):
    """Запускает конкретный модуль"""
    if module_name not in MODULE_MAP:
        typer.echo(f"❌ Неизвестный модуль: {module_name}")
        typer.echo(f"   Доступные: {', '.join(MODULE_MAP.keys())}")
        raise typer.Exit(code=1)

    attr_name, method_name = MODULE_MAP[module_name]
    module_ui = getattr(city_ui, attr_name)
    method = getattr(module_ui, method_name)

    typer.echo(f"🔧 Запуск модуля: {module_name}\n")
    # Передаём стандартные input/print в методы UI
    method(input, print)


@app.command()
def run():
    """🚀 Запустить интерактивное меню (режим по умолчанию)"""
    print_welcome()
    input("\nНажмите Enter для продолжения...")
    print('\033[2J\033[H', end='')  # Очистка экрана

    print("Вы в CLI умного города\n")
    print("На выбор доступны следующие системы: \n")
    print_help(print, modules)
    print("Для справки введите --help")
    print("Для выхода введите --exit")

    while True:

        cmd = input("> ").strip()

        if cmd == "--exit":
            break
        if cmd == "--help":
            for module, command_list in commands.items():
                print(f"{module}")
                for comm, desc in command_list.items():
                    print(f"    {module} {comm} :   {desc}")
            print("Для справки по командам отдельно введите команду с флагом --help\n")
            print("Пример использования комманды:")
            print("    tms --arrive-stop --name 'Пл. Ленина'")
            print("Для справки:\n    tms --arrive-stop --help")

            print("\nexit — выход из программы")
            continue
        parts = cmd.split()

        if len(parts) < 2:
            print("Неверная команда")
            continue

        module = parts[0]
        command = parts[1]
        args = parts[2:]

        try:

            if module in commands and command in commands[module]:

                commandsmodule][command

            else:
                print("Неизвестная команда")

        except Exception as e:
            print("Ошибка:", e)

    city_ui = CityUI()
    city_ui.general_menu(input, print)


@app.command()
def module_(name: str = typer.Argument(..., help="Название модуля")):
    """
    🔧 Запустить конкретный модуль напрямую.

    Доступные модули:
      - tms      : Система общественного транспорта
      - traffic  : Управление движением
      - env      : Мониторинг окружающей среды
      - data     : Сбор и анализ данных
      - sensors  : Сенсоры
    """
    print_welcome()
    input("\nНажмите Enter для запуска модуля...")
    print('\033[2J\033[H', end='')

    city_ui = CityUI()
    run_module(city_ui, name)


# Команды-алиасы для удобства (можно запускать как `smartcity tms`)
@app.command()
def tms():
    """🚌 Система общественного транспорта"""
    city_ui = CityUI()
    run_module(city_ui, "tms")


@app.command()
def traffic():
    """🚦 Управление движением"""
    city_ui = CityUI()
    run_module(city_ui, "traffic")


@app.command()
def env():
    """🌿 Мониторинг окружающей среды"""
    city_ui = CityUI()
    run_module(city_ui, "env")


@app.command()
def data():
    """📊 Сбор и анализ данных"""
    city_ui = CityUI()
    run_module(city_ui, "data")


@app.command()
def sensors():
    """📡 Сенсоры"""
    city_ui = CityUI()
    run_module(city_ui, "sensors")


if __name__ == "__main__":
    app()