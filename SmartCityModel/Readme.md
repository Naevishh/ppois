# SmartCityModel

> Модель умного города для оптимизации городской инфраструктуры  
> *Лабораторная работа №1 по курсу «Проектирование ПО интеллектуальных систем»*

---

## Описание проекта

Проект реализует программную систему для моделирования работы умного города в соответствии с вариантом 25.

**Предметная область**: внедрение технологий для улучшения городской инфраструктуры.

**Ключевые сущности**:

- Умный город (координатор систем)
- Сенсоры (сбор данных)
- Системы управления транспортом
- Энергосберегающие технологии
- Общественные сервисы

**Поддерживаемые операции**:

- Управление транспортным потоком
- Мониторинг состояния окружающей среды
- Оптимизация системы освещения
- Предоставление общественных сервисов
- Сбор и анализ данных для улучшения городской планировки

---

## Требования

- Python 3.10 или выше
- Зависимости: см. `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## Установка и запуск

Для работы с проектом требуется **Python 3.10** или выше.

1. Клонируйте репозиторий и перейдите в директорию с папкой проекта:

```bash
git clone https://github.com/Naevishh/ppois.git
cd ppois
```

2. Установите зависимости

```bash
pip install -r SmartCityModel/requirements.txt
```

## Использование CLI

Система предоставляет интерактивный интерфейс командной строки. Запуск осуществляется из корневой папки `ppois`:

```bash
python -m SmartCityModel
```

### Глобальные команды

Эти команды доступны на любом этапе работы с интерфейсом:

| Команда  | Описание                                                 |
|----------|----------------------------------------------------------|
| `--help` | Показать подробную справку по всем модулям и их командам |
| `--exit` | Завершить работу программы и выйти из CLI                |

#### `--help` — справка по командам

При вводе `--help` система выводит:

1. Список всех доступных модулей
2. Для каждого модуля — список команд с кратким описанием и синтаксисом
3. Примеры использования команд

**Пример вывода справки:**

```
tms
  tms --add-stop : Добавить остановку (--name <Название>)
  tms --add-route : Создать маршрут (--stops <...>)
  tms --arrive-stop : Информация о прибытии (--stop <...>)
  ...
Для справки по командам отдельно введите команду с флагом --help
Пример использования команды:
  tms --arrive-stop --name 'Пл. Ленина'
Пример использования справки:
  tms --arrive-stop --help
```

#### `--exit` — выход из программы

Команда корректно завершает работу CLI, освобождает ресурсы и возвращает управление в терминал.

```bash
> --exit
# Программа завершена, возврат в оболочку
```

---

## Описание работы программы по модулям

Программная система **SmartCityModel** построена по модульному принципу. Каждый модуль отвечает за определённую
предметную область умного города и предоставляет набор команд для взаимодействия через CLI.

Модули взаимодействуют через единое ядро (`City`), которое координирует данные между подсистемами. Все модули
поддерживают:

- Аннотации типов для всех публичных интерфейсов
- Обработку исключений для корректного завершения операций
- Документирование методов в формате Google-style docstrings

Ниже приведено описание каждого модуля, его сущностей и доступных операций.

---

### Модуль `citizens` (Жители города)

Модуль отвечает за моделирование жителей умного города — их регистрацию, хранение данных и взаимодействие с городскими
сервисами.

#### Основные сущности

| Класс            | Описание                                                              |
|------------------|-----------------------------------------------------------------------|
| `Human`          | Модель жителя: содержит ФИО, возраст, адрес, уникальный идентификатор |
| `UserRepository` | Репозиторий для хранения и поиска пользователей по ID                 |

#### Функциональность

- **Регистрация жителя**: создание нового объекта `Human` с валидацией входных данных
- **Авторизация**: поиск пользователя по ID через `UserRepository`
- **Получение информации**: вывод данных о текущем авторизованном пользователе
- **Валидация**: проверка корректности возраста, адреса и других полей

#### Интеграция с CLI

Функционал модуля `citizens` доступен через команды модуля **`services`**:

```bash
# Регистрация нового жителя
> services --register --name "Анна" --surname "Иванова" --age 25 --street "Ленина" --house "10"

# Авторизация по ID
> services --login --id "USER_001"

# Просмотр данных текущего пользователя
> services --whoami
```

### Модуль `city` (Ядро системы умного города)

Модуль `city` является центральным компонентом системы **SmartCityModel**. Он отвечает за инициализацию, координацию и
управление всеми подсистемами умного города.

#### Основные сущности

| Класс       | Описание                                                                                   |
|-------------|--------------------------------------------------------------------------------------------|
| `SmartCity` | Главный класс-координатор: инициализирует районы, сервисы, транспорт, энергетику и сенсоры |
| `CityUI`    | Интерфейс для взаимодействия CLI с ядром `SmartCity`                                       |

#### Функциональность

- **Инициализация системы**: автоматическое создание трёх районов (`center_1`, `suburb_1`, `suburb_2`) с
  предустановленными объектами инфраструктуры
- **Координация подсистем**: управление взаимодействием между модулями `transport`, `energy`, `sensors`, `services`,
  `environment`
- **Управление данными**: централизованное хранение ссылок на все объекты города (остановки, перекрёстки, сенсоры,
  пользователи)
- **Генерация тестовых данных**: создание демо-объектов для демонстрации работы системы без ручной настройки

#### Интеграция с CLI

Модуль `city` не имеет прямых команд в CLI — он работает «за кулисами». Все пользовательские команды обрабатываются
через интерфейсы подмодулей (`tms`, `env`, `sensors` и др.), которые получают доступ к данным через экземпляр
`SmartCity`.

Пример внутренней работы:

```python
# В cli.py при запуске команды 'tms --add-stop'
city_ui = CityUI()  # Создаёт экземпляр SmartCity
city_ui.tms_ui.add_stop("Пл. Ленина")  # Вызов метода через UI-обёртку
```

### Модуль `core` (Базовые компоненты и утилиты)

Модуль `core` предоставляет фундаментальные компоненты системы **SmartCityModel**, которые используются всеми остальными
модулями. Он содержит перечисления, базовые классы, исключения и утилиты валидации.

#### Структура модуля

```
SmartCityModel/core/
├── __init__.py      # Экспорт публичных символов
├── base.py          # Базовый класс SmartDevice
├── enums.py         # Перечисления (Domain, VehicleType, уровни сенсоров и др.)
├── exceptions.py    # Кастомные исключения предметной области
├── helpers.py       # Вспомогательные функции для CLI (show_menu, print_help)
└── utils.py         # Валидаторы входных данных
```

#### Основные компоненты

##### Перечисления (enums.py)

Модуль определяет типизированные константы для всей системы:

| Перечисление         | Описание                                   | Значения                                                                              |
|----------------------|--------------------------------------------|---------------------------------------------------------------------------------------|
| `Domain`             | Домены применения технологий умного города | TRANSPORTATION, ECOLOGY, INFRASTRUCTURE, SAFETY, HEALTHCARE, EDUCATION, HOUSING       |
| `VehicleType`        | Типы транспортных средств                  | CAR, BUS, TRAM, TROLLEYBUS, TRUCK, AMBULANCE, FIRE_TRUCK, POLICE, BICYCLE, MOTORCYCLE |
| `TrafficLightColor`  | Состояния светофора                        | GREEN, YELLOW, RED                                                                    |
| `Direction`          | Направления движения                       | NORTH, SOUTH, EAST, WEST                                                              |
| `AirQualityLevel`    | Уровни качества воздуха                    | EXCELLENT, GOOD, MODERATE, POOR, HAZARDOUS (с кодами 1-5 и метками)                   |
| `TemperatureLevel`   | Уровни температуры                         | VERY_COLD, COLD, COMFORTABLE, WARM, HOT                                               |
| `HumidityLevel`      | Уровни влажности                           | VERY_DRY, DRY, COMFORTABLE, HUMID, VERY_HUMID                                         |
| `NoiseLevel`         | Уровни шума                                | QUIET, MODERATE, LOUD, VERY_LOUD, DANGEROUS                                           |
| `PlanningMetricType` | Метрики городского планирования            | ECOLOGY_SCORE, TRANSPORT_LOAD, INFRASTRUCTURE_DENSITY, LIVEABILITY_INDEX              |
| `MeasurementType`    | Типы измерений сенсоров                    | OCCUPANCY, DISTANCE, AIR_QUALITY, TRAFFIC_INTENSITY и др.                             |

Перечисления `AirQualityLevel`, `TemperatureLevel`, `HumidityLevel`, `NoiseLevel` наследуются от базового класса
`LabeledEnum`, который предоставляет методы `from_code()` и `from_label()` для преобразования между кодом, меткой и
экземпляром перечисления.

##### Базовый класс (base.py)

Класс `SmartDevice` является абстракцией для всех устройств умного города:

```python
class SmartDevice:
    def __init__(self, device_keyword: str, domain: Domain) -> None:
        self.device_id = device_keyword + str(uuid.uuid4())[:6]
        self.domain = domain
```

Каждое устройство получает уникальный идентификатор, сформированный из ключевого слова и первых 6 символов UUID, а также
привязку к домену.

##### Исключения (exceptions.py)

Модуль определяет иерархию исключений для обработки ошибок предметной области:

| Исключение            | Назначение                                   |
|-----------------------|----------------------------------------------|
| `HospitalException`   | Ошибки при работе с медицинскими сервисами   |
| `TransportException`  | Ошибки в транспортной подсистеме             |
| `SensorValueError`    | Некорректные значения сенсоров               |
| `ObjectNotFoundError` | Объект с указанным идентификатором не найден |

Все исключения наследуются от базового `Exception` и могут быть перехвачены на уровне CLI для вывода человекочитаемых
сообщений.

##### Утилиты валидации (utils.py)

Модуль предоставляет классы для строгой проверки входных данных:

- `RussianStringValidator` — проверка строк на русском языке (только кириллица, дефисы, точки; настройка
  минимальной/максимальной длины, разрешение пробелов)
- `LatinStringValidator` — проверка строк на латинице с поддержкой цифр и специальных символов
- `IdentifierValidator` — валидация технических идентификаторов (латиница, цифры, подчёркивание)
- `NumberValidator` — проверка числовых значений с поддержкой диапазонов, ограничения количества цифр и знаков после
  запятой
- `ValidationError`, `NumberValidationError` — специализированные исключения для ошибок валидации

Для удобства в модуле определены глобальные экземпляры валидаторов:

- `NAME_VALIDATOR` — для имён и фамилий (2-50 символов, кириллица)
- `ADDRESS_VALIDATOR` — для адресов (2-100 символов)
- `AGE_VALIDATOR` — для возраста (0-150)
- `HOUSE_NUMBER_VALIDATOR` — для номеров домов (1-9999)
- `GRADE_VALIDATOR` — для оценок (0-10)
- `SENSOR_VALUE_VALIDATOR` — для значений сенсоров (-60 до 1000000)
- `ID_VALIDATOR` — для технических идентификаторов

##### Вспомогательные функции (helpers.py)

Функции для улучшения пользовательского опыта в CLI:

- `smooth_print(text, print_func, char_delay, line_delay)` — вывод текста с эффектом печатной машинки
- `show_menu(options, get_user_input, print_func, prompt)` — универсальная функция отображения меню с обработкой ввода
- `print_help(options, print_func)` — вывод краткой справки по командам
- `print_detailed_help(module, command, ui, print_func)` — вывод расширенной справки с учётом текущего состояния
  системы (доступные районы, сенсоры, маршруты и т.д.)

#### Интеграция с другими модулями

Модуль `core` не имеет прямого интерфейса CLI. Его компоненты импортируются и используются во всех функциональных
модулях:

- `Domain` и `VehicleType` используются в `transport`, `sensors`, `energy`
- Валидаторы из `utils` применяются при обработке пользовательского ввода в `services`, `tms`, `sensors`
- Исключения из `exceptions` выбрасываются при ошибках бизнес-логики и перехватываются в `cli.py`
- Функции `show_menu` и `print_help` используются для построения интерактивного меню в каждом подмодуле

#### Пример использования

```python
from SmartCityModel.core import (
    Domain,
    RussianStringValidator,
    ValidationError,
    SmartDevice
)

# Валидация имени пользователя
validator = RussianStringValidator(min_length=2, max_length=50)
try:
    name = validator.validate("Анна")  # Возвращает "Анна"
    invalid = validator.validate("Anna123")  # Выбросит ValidationError
except ValidationError as e:
    print(f"Ошибка валидации: {e}")

# Создание устройства
device = SmartDevice(device_keyword="sensor_", domain=Domain.ECOLOGY)
print(device.device_id)  # Например: "sensor_a1b2c3"
print(device.domain.value)  # "ecology"
```

### Модуль `energy` (Энергосберегающие технологии)

Модуль `energy` реализует подсистему управления энергопотреблением и генерацией в модели умного города. Он отвечает за
балансировку спроса и предложения энергии, оптимизацию работы устройств и интеграцию возобновляемых источников.

#### Структура модуля

```
SmartCityModel/energy/
├── __init__.py          # Экспорт публичных классов
├── devices.py           # Умные устройства: SmartThermostat, SmartHome, SmartLight
├── generation.py        # Источники энергии: SolarPanel, WindTurbine, BatteryStorage
├── grid.py              # CityEnergyGrid — координатор энергосистемы
└── lighting.py          # SmartLightningSystem — управление освещением
```

#### Основные компоненты

##### Генерация и хранение энергии (generation.py)

Классы для моделирования возобновляемых источников и систем накопления:

| Класс            | Описание                                                                  | Ключевые методы                                                 |
|------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------|
| `SolarPanel`     | Солнечная панель, вырабатывающая энергию пропорционально уровню освещения | `produce_electricity()`                                         |
| `WindTurbine`    | Ветрогенератор с зависимостью выработки от скорости ветра                 | `set_wind_speed()`, `produce_electricity()`                     |
| `BatteryStorage` | Аккумулятор для хранения излишков энергии                                 | `store_energy()`, `release_energy()`, `get_charge_percentage()` |

Особенности реализации:

- `SolarPanel` получает данные от сенсора освещённости и рассчитывает выработку по формуле: `light_level * 0.5`
- `WindTurbine` начинает генерацию только при скорости ветра от 3 м/с, выбрасывает `SensorValueError` при некорректных
  значениях
- `BatteryStorage` наследуется от `SmartDevice`, имеет ёмкость и текущий заряд, поддерживает частичную зарядку/разрядку

##### Умные устройства (devices.py)

Классы потребителей энергии с поддержкой оптимизации:

| Класс             | Описание                                                             | Ключевые методы                                        |
|-------------------|----------------------------------------------------------------------|--------------------------------------------------------|
| `SmartThermostat` | Термостат с энергосберегающей логикой климат-контроля                | `optimize_climate()`, `get_energy_consumption()`       |
| `SmartHome`       | Агрегатор метрик умного дома: вода, электричество, климат, освещение | `get_energy_consumption()`, `get_metrics()`            |
| `SmartLight`      | Умный светильник с реакцией на движение и уровень освещённости       | `turn_on()`, `set_level()`, `get_energy_consumption()` |

Особенности реализации:

- `SmartThermostat` снижает потребление, если температура выше 22 °C (отключает нагрев)
- `SmartLight` автоматически регулирует яркость в зависимости от внешнего освещения и включает свет при обнаружении
  движения через `MotionSensor`
- Все устройства возвращают потребление в ваттах через унифицированный метод `get_energy_consumption()`

##### Система освещения (lighting.py)

Класс `SmartLightningSystem` координирует группу умных светильников:

```python
class SmartLightningSystem:
    def optimize_lightning(self) -> None:
        """Вызывает set_level() для каждого светильника в системе"""
        for light in self.smart_lights:
            light.set_level()

    def get_energy_consumption(self) -> float:
        """Суммарное потребление всех светильников"""
        return sum(l.get_energy_consumption() for l in self.smart_lights)
```

##### Энергосеть города (grid.py)

Класс `CityEnergyGrid` — центральный компонент модуля, отвечающий за балансировку энергосистемы:

```python
class CityEnergyGrid:
    def __init__(self, generators: list, storages: list, consumers: list) -> None:
        self.generators = generators  # SolarPanel, WindTurbine
        self.storages = storages  # BatteryStorage
        self.consumers = consumers  # SmartLight, SmartHome, etc.
```

Метод `balance_energy()` реализует основной алгоритм оптимизации:

1. Подсчёт суммарной выработки всеми генераторами
2. Подсчёт базового потребления всеми устройствами
3. Расчёт баланса: `surplus = production - consumption`
4. При избытке энергии — зарядка аккумуляторов
5. При дефиците — разрядка аккумуляторов, при необходимости — предупреждение о подключении к внешней сети

Возвращаемое значение:

```python
{
    "production": float,  # общая выработка
    "consumption": float,  # общее потребление
    "surplus": float,  # баланс (положительный — излишек, отрицательный — дефицит)
    "result": str  # человекочитаемое описание результата
}
```

Метод `optimize_all()` вызывает оптимизацию на всех устройствах-потребителях (в частности, на `SmartLightningSystem`),
после чего выполняет балансировку.

#### Интеграция с CLI

Функционал модуля `energy` доступен через команду `energy` в интерактивном CLI:

```bash
# Запуск оптимизации энергопотребления
> energy --optimize

# Просмотр текущего состояния энергосистемы
> energy --status
```

Внутренняя реализация в `cli.py`:

```python
def handle_energy_optimize(city_ui):
    result = city_ui.city.energy_grid.optimize_all()
    print(f"Баланс: {result['result']}")
    print(f"Выработка: {result['production']} Вт")
    print(f"Потребление: {result['consumption']} Вт")
```

#### Обработка ошибок

- Модуль использует исключение `SensorValueError` из `core.exceptions` для валидации входных данных сенсоров
- Некорректные значения скорости ветра (< 0 или > 25 м/с) вызывают исключение с пояснением
- Все исключения перехватываются на уровне CLI и выводятся в человекочитаемом виде

#### Пример использования

```python
from SmartCityModel.energy import (
    SolarPanel, WindTurbine, BatteryStorage,
    SmartLight, SmartThermostat, CityEnergyGrid
)
from SmartCityModel.sensors import LightLevelSensor, MotionSensor, TemperatureSensor

# Создание сенсоров
light_sensor = LightLevelSensor("light_01", 80)  # 80% освещённости
motion_sensor = MotionSensor("motion_01")
temp_sensor = TemperatureSensor("temp_01", 20)

# Создание устройств
panel = SolarPanel(light_sensor)
turbine = WindTurbine()
turbine.set_wind_speed(10)  # 10 м/с
battery = BatteryStorage(capacity=1000)

light = SmartLight(light_sensor, motion_sensor)
thermostat = SmartThermostat(temp_sensor)

# Инициализация энергосети
grid = CityEnergyGrid(
    generators=[panel, turbine],
    storages=[battery],
    consumers=[light, thermostat]
)

# Балансировка
result = grid.balance_energy()
print(result["result"])  # "Производство покрыло потребление."
print(f"Излишек: {result['surplus']} Вт")
```

### Модуль `environment` (Мониторинг окружающей среды)

Модуль `environment` реализует подсистему мониторинга экологического состояния умного города. Он отвечает за сбор,
агрегацию и анализ данных с датчиков качества воздуха, температуры, влажности и уровня шума.

#### Структура модуля

```
SmartCityModel/environment/
├── __init__.py          # Экспорт: EnvironmentMonitoringSystem
└── monitoring.py        # Класс EnvironmentMonitoringSystem
```

#### Основные компоненты

##### Класс `EnvironmentMonitoringSystem` (monitoring.py)

Единственный класс модуля, предоставляющий функционал экологического мониторинга.

**Метод `environmental_monitoring_operation`**

Основной метод класса, выполняющий анализ состояния окружающей среды.

Сигнатура:

```python
def environmental_monitoring_operation(
        self,
        air: list,
        temp: list,
        humid: list,
        noise: list
) -> dict:
```

Параметры:

- `air` — список сенсоров качества воздуха (`AirQualitySensor`)
- `temp` — список температурных сенсоров (`TemperatureSensor`)
- `humid` — список сенсоров влажности (`HumiditySensor`)
- `noise` — список сенсоров уровня шума (`NoiseSensor`)

Алгоритм работы:

1. Для каждой категории сенсоров вычисляется среднее арифметическое значение статуса (код уровня от 1 до 5)
2. На основе среднего значения определяется итоговый уровень через метод `from_code()` соответствующего перечисления
3. Рассчитывается общий средний показатель по всем категориям
4. Возвращается словарь с результатами

Возвращаемое значение:

```python
{
    "air": AirQualityLevel,  # Уровень качества воздуха
    "temperature": TemperatureLevel,  # Уровень температуры
    "humidity": HumidityLevel,  # Уровень влажности
    "noise": NoiseLevel,  # Уровень шума
    "average": float  # Средний показатель по всем категориям (1.0–5.0)
}
```

Вспомогательные функции внутри метода:

- `get_average(sensors: list) -> float` — вычисление среднего значения по списку сенсоров
- `get_level(enum_class, average: float)` — преобразование среднего значения в уровень перечисления с ограничением
  диапазона 1–5

#### Интеграция с другими модулями

Модуль `environment` тесно связан с модулем `sensors`:

- Получает списки сенсоров из объектов `District`, которые создаются в модуле `city`
- Использует перечисления из `core.enums`: `AirQualityLevel`, `TemperatureLevel`, `HumidityLevel`, `NoiseLevel`
- Результаты мониторинга передаются в CLI через интерфейс `EnvironmentMonitoringUI`

#### Интеграция с CLI

Функционал модуля доступен через команду `env` в интерактивном интерфейсе:

```bash
# Получить текущее состояние окружающей среды
> env --state
```

Внутренняя реализация в `cli.py`:

```python
def handle_env(ui: EnvironmentMonitoringUI, args: list, print_func) -> None:
    if cmd == "--state":
        results = ui.get_environment_state()
        output = ui.format_environment_state(results)
        print_func(output)
```

Метод `get_environment_state()` в `EnvironmentMonitoringUI`:

1. Собирает все сенсоры соответствующих типов из всех районов города
2. Вызывает `environmental_monitoring_operation()` ядра мониторинга
3. Возвращает словарь с результатами для форматирования и вывода

#### Обработка ошибок

- Метод устойчив к пустым спискам сенсоров: при отсутствии данных возвращается значение 0 для среднего
- Значения уровней ограничиваются диапазоном 1–5 через `max(1, min(5, round(average)))`, что предотвращает выход за
  пределы допустимых кодов перечислений
- Все исключения, возникающие при доступе к сенсорам, перехватываются на уровне CLI и выводятся в человекочитаемом виде

#### Пример использования

```python
from SmartCityModel.environment import EnvironmentMonitoringSystem
from SmartCityModel.sensors import (
    AirQualitySensor, TemperatureSensor,
    HumiditySensor, NoiseSensor
)

# Создание тестовых сенсоров
air_sensors = [
    AirQualitySensor("air_01", 3),  # Moderate
    AirQualitySensor("air_02", 2),  # Good
]
temp_sensors = [TemperatureSensor("temp_01", 4)]  # Warm
humid_sensors = [HumiditySensor("humid_01", 3)]  # Comfortable
noise_sensors = [NoiseSensor("noise_01", 2)]  # Moderate

# Инициализация системы мониторинга
monitoring = EnvironmentMonitoringSystem()

# Получение результатов
results = monitoring.environmental_monitoring_operation(
    air=air_sensors,
    temp=temp_sensors,
    humid=humid_sensors,
    noise=noise_sensors
)

# Вывод результатов
print(f"Качество воздуха: {results['air'].label}")  # Good
print(f"Температура: {results['temperature'].label}")  # Warm
print(f"Влажность: {results['humidity'].label}")  # Comfortable
print(f"Уровень шума: {results['noise'].label}")  # Moderate
print(f"Средний показатель: {results['average']:.2f}")  # 2.75
```

### Модуль `sensors` (Система сбора данных)

Модуль `sensors` реализует иерархию классов для моделирования датчиков умного города. Он обеспечивает сбор данных о
состоянии окружающей среды, транспортных потоках и параметрах энергопотребления.

#### Структура модуля

```
SmartCityModel/sensors/
├── __init__.py          # Экспорт всех публичных классов сенсоров
├── base_sensor.py       # Базовый абстрактный класс Sensor
├── environment_sensors.py  # Сенсоры экологического мониторинга
├── traffic_sensors.py      # Сенсоры транспортной инфраструктуры
└── energy_sensors.py       # Сенсоры энергосистемы и ЖКХ
```

#### Базовый класс `Sensor` (base_sensor.py)

Все сенсоры наследуются от абстрактного базового класса `Sensor`, который определяет единый интерфейс:

```python
class Sensor:
    def __init__(self, sensor_id_keyword: str, domain: Domain, m_type: MeasurementType) -> None:
        self.sensor_id = sensor_id_keyword + str(uuid.uuid4())[:6]
        self.domain = domain
        self.measurement_type = m_type

    def set_value(self, value) -> None:
        pass

    def get_status(self):
        pass
```

Особенности реализации:

- Уникальный идентификатор формируется из префикса и первых 6 символов UUID
- Каждый сенсор привязан к домену (`Domain`) и типу измерения (`MeasurementType`)
- Методы `set_value` и `get_status` переопределяются в наследниках для специфичной логики

#### Сенсоры экологического мониторинга (environment_sensors.py)

| Класс               | Описание                                                   | Методы                                             | Возвращаемый тип `get_status()` |
|---------------------|------------------------------------------------------------|----------------------------------------------------|---------------------------------|
| `AirQualitySensor`  | Датчик качества воздуха (концентрация загрязнений, мкг/м³) | `set_value(concentration: int)`                    | `AirQualityLevel`               |
| `TemperatureSensor` | Датчик температуры (°C)                                    | `set_value(temperature: int)`, `get_temperature()` | `TemperatureLevel`              |
| `HumiditySensor`    | Датчик влажности (зависит от `TemperatureSensor`)          | `set_value(concentration: float)`                  | `HumidityLevel`                 |
| `NoiseSensor`       | Датчик уровня шума (дБ)                                    | `set_value(decibels: float)`                       | `NoiseLevel`                    |

Особенности реализации:

- `AirQualitySensor`: уровни качества определяются по пороговым значениям концентрации (0-50: Excellent, 51-100: Good,
  101-150: Moderate, 151-200: Poor, >200: Hazardous)
- `TemperatureSensor`: уровни температуры определяются по диапазонам (<=10: VeryCold, 11-18: Cold, 19-24: Comfortable,
  25-30: Warm, >30: Hot)
- `HumiditySensor`: использует уравнение Арден-Бака для расчёта плотности насыщенного пара и вычисления относительной
  влажности в процентах; требует ссылки на `TemperatureSensor` для корректных вычислений
- `NoiseSensor`: уровни шума определяются по диапазонам в дБ (<40: Quiet, 40-59: Moderate, 60-79: Loud, 80-99:
  VeryLoud, >=100: Dangerous)

#### Сенсоры транспортной инфраструктуры (traffic_sensors.py)

| Класс                      | Описание                                  | Методы                                                    | Возвращаемый тип `get_status()`             |
|----------------------------|-------------------------------------------|-----------------------------------------------------------|---------------------------------------------|
| `TrafficFlowSensor`        | Датчик интенсивности транспортного потока | `set_value(count: int)`                                   | `int` (транспортных средств в минуту)       |
| `PedestrianCrossingSensor` | Датчик количества пешеходов на переходе   | `set_value(pedestrians: int)`                             | `int` (количество ожидающих)                |
| `AITrafficCamera`          | Камера с аналитикой на базе ИИ            | `detect_event(vehicle_type: VehicleType, incident: bool)` | `dict` с полями `vehicle_type` и `incident` |

Особенности реализации:

- Все сенсоры валидируют входные значения и выбрасывают `SensorValueError` при выходе за допустимые диапазоны
- `AITrafficCamera` возвращает словарь с последним зафиксированным событием, что позволяет интегрировать модуль с
  системами анализа инцидентов

#### Сенсоры энергосистемы и ЖКХ (energy_sensors.py)

| Класс              | Базовый класс | Описание                              | Методы                                                 | Возвращаемый тип `get_status()` |
|--------------------|---------------|---------------------------------------|--------------------------------------------------------|---------------------------------|
| `LightLevelSensor` | `Sensor`      | Датчик уровня внешнего освещения      | `set_value(level: int)`                                | `int` (уровень 0-100)           |
| `MotionSensor`     | `Sensor`      | Датчик движения с поддержкой callback | `detect_motion(is_moving: bool)`, `set_callback(func)` | `bool` (есть движение)          |
| `WaterMeter`       | `SmartDevice` | Счётчик расхода воды                  | `set_value(volume: int)`, `get_water_volume()`         | — (использует отдельный геттер) |
| `ElectricityMeter` | `SmartDevice` | Счётчик потребления электроэнергии    | `set_value(energy: float)`, `get_energy()`             | — (использует отдельный геттер) |

Особенности реализации:

- `MotionSensor` поддерживает установку callback-функции через `set_callback()`, которая автоматически вызывается при
  обнаружении движения — это позволяет реализовать реактивное управление освещением
- `WaterMeter` и `ElectricityMeter` наследуются от `SmartDevice`, так как представляют собой не просто сенсоры, а
  устройства с уникальным идентификатором и привязкой к домену `HOUSING`

#### Валидация и обработка ошибок

Все сенсоры используют единый механизм валидации:

- Отрицательные значения или значения, превышающие физически возможные пределы, вызывают исключение `SensorValueError` с
  человекочитаемым сообщением
- Примеры проверок:
    - Концентрация загрязнений: 0-500 мкг/м³
    - Температура: -50 до +60 °C
    - Уровень шума: 0-150 дБ
    - Количество транспортных средств: 0-200 в минуту

Пример обработки ошибки:

```python
sensor = AirQualitySensor()
try:
    sensor.set_value(600)  # Превышает лимит 500
except SensorValueError as e:
    print(f"Ошибка: {e}")  # "Концентрация слишком высокая."
```

#### Интеграция с CLI

Функционал модуля `sensors` доступен через команду `sensors` в интерактивном интерфейсе:

```bash
# Показать список доступных районов
> sensors --list-districts

# Показать сенсоры в районе по категории
> sensors --list-sensors --district "center_1" --category "environment"

# Установить значение сенсора
> sensors --set --district "center_1" --type "air_quality" --value 42
```

Внутренняя реализация в `cli.py` использует методы `get_status()` для получения текущих показаний и `set_value()` для
симуляции изменения параметров среды.

#### Пример использования

```python
from SmartCityModel.sensors import (
    AirQualitySensor, TemperatureSensor, HumiditySensor,
    TrafficFlowSensor, LightLevelSensor, MotionSensor
)

# Создание сенсоров
air = AirQualitySensor()
temp = TemperatureSensor()
humidity = HumiditySensor(temp)  # Требует ссылку на температурный сенсор

# Установка значений
air.set_value(85)  # Хорошее качество воздуха
temp.set_value(22)  # Комфортная температура
humidity.set_value(12.5)  # Концентрация пара в г/м³

# Получение статусов
print(air.get_status())  # AirQualityLevel.GOOD
print(temp.get_status())  # TemperatureLevel.COMFORTABLE
print(humidity.get_status())  # HumidityLevel.COMFORTABLE

# Датчик движения с реакцией
light = LightLevelSensor()
motion = MotionSensor()


def turn_on_light():
    print("Свет включён!")


motion.set_callback(turn_on_light)
motion.detect_motion(True)  # Автоматически вызовет turn_on_light()
```

### Модуль `services` (Общественные сервисы)

Модуль `services` реализует подсистему предоставления общественных услуг в модели умного города. Он отвечает за
взаимодействие жителей с медицинскими, образовательными и коммунальными сервисами.

#### Структура модуля

```
SmartCityModel/services/
├── __init__.py          # Экспорт публичных классов
├── base.py              # Абстрактный базовый класс PublicService
├── hospital.py          # Сервис медицинских услуг (класс Hospital)
├── education.py         # Сервис образовательных услуг (класс EducationService)
└── utilities.py         # Сервис коммунальных услуг (класс UtilitiesService)
```

#### Базовый класс `PublicService` (base.py)

Абстрактный класс, определяющий единый интерфейс для всех общественных сервисов:

```python
class PublicService(ABC):
    def __init__(self, name: str, address: tuple, service_id: str, service_category: Domain) -> None:
        self.name = name
        self.address = address
        self.service_category = service_category
        self.service_id = service_id
        self.is_active = True
        self.current_load = 0
        self.available_actions = []

    @abstractmethod
    def provide_service(self, action_type, person: Human) -> None:
        pass

    def get_status(self) -> dict:
        return {
            "active": self.is_active,
            "current_load": self.current_load
        }
```

Особенности реализации:

- Все сервисы привязаны к домену через параметр `service_category` (тип `Domain`)
- Метод `provide_service` объявлен абстрактным — каждый наследник реализует собственную логику обработки запросов
- Атрибут `available_actions` содержит список доступных операций для отображения в справке CLI

#### Сервис медицинских услуг (hospital.py)

Класс `Hospital` предоставляет функционал для работы с медицинскими услугами.

**Доступные действия:**
| Действие | Описание | Параметры |
|----------|----------|-----------|
| `get_ticket` | Запись к врачу | `doctor_name` (ключ: psychiatrist/therapist/surgeon) |
| `order_certificate` | Заказ справки | `purpose` (цель справки, 2-500 символов) |
| `call_ambulance` | Вызов скорой помощи | не требует параметров (используется адрес пациента) |

**Основные методы:**

```python
def order_ticket_to_doctor(self, doctor_name: str, patient: Human) -> str:
    """Записать пациента к врачу. Возвращает номер талона."""


def order_certificate(self, purpose: str, patient: Human) -> str:
    """Сформировать текст справки с данными пациента."""


def call_ambulance(self, address: tuple) -> str:
    """Сгенерировать подтверждение вызова скорой помощи."""


def get_available_doctors(self) -> Dict[str, Dict[str, Any]]:
    """Вернуть словарь с информацией о доступных врачах и количестве мест."""
```

**Особенности реализации:**

- Врачи хранятся в словаре с ключами `psychiatrist`, `therapist`, `surgeon`
- Для каждого врача отслеживается лимит талонов (`limit`) и текущее количество выданных (`current`)
- При превышении лимита выбрасывается исключение `HospitalException`
- Валидация цели справки выполняется через `RussianStringValidator` (мин. 2 символа, разрешены пробелы)

#### Сервис образовательных услуг (education.py)

Класс `EducationService` предоставляет функционал для записи на курсы и управления успеваемостью.

**Доступные действия:**
| Действие | Описание | Параметры |
|----------|----------|-----------|
| `enroll_course` | Запись на курс | `course_name` (название курса) |
| `set_grade` | Установка оценки | `subject`, `grade` (1-10) |
| `get_grades` | Просмотр оценок | не требует параметров |

**Основные методы:**

```python
def enroll_course(self, course_name: str, student: Human) -> str:
    """Записать студента на курс. Уменьшает количество доступных мест."""


def set_grade(self, student: Human, subject: str, grade: int) -> str:
    """Установить оценку студенту по предмету."""


def get_grades(self, student: Human) -> Dict[str, Any]:
    """Вернуть словарь с оценками студента."""


def get_available_courses(self) -> Dict[str, int]:
    """Вернуть словарь доступных курсов с количеством мест."""
```

**Особенности реализации:**

- Доступные курсы: `Python` (50 мест), `DataScience` (30 мест)
- Успеваемость хранится в структуре `grade_book`: `{ student_id: { subject: grade } }`
- Валидация названия курса — через `LATIN_STR_VALIDATOR`, предмета — через `NAME_VALIDATOR`, оценки — через
  `GRADE_VALIDATOR` (диапазон 1-10)
- Методы `format_grades_output` и `format_courses_output` возвращают отформатированные строки для вывода в CLI

#### Сервис коммунальных услуг (utilities.py)

Класс `UtilitiesService` предоставляет функционал для просмотра показаний счётчиков и подачи заявок в ЖКХ.

**Доступные действия:**
| Действие | Описание | Параметры |
|----------|----------|-----------|
| `view_metrics` | Просмотр показаний счётчиков | не требует параметров (используется адрес пользователя) |
| `report_issue` | Подача заявки о проблеме | `description` (10-500 символов) |

**Основные методы:**

```python
def auto_collect_metrics(self, address: tuple) -> Dict[str, int]:
    """Симулировать сбор данных с датчиков умного дома."""


def view_metrics(self, address: tuple) -> Dict[str, Any]:
    """Вернуть показания воды и электричества по адресу."""


def report_issue(self, description: str) -> Dict[str, Any]:
    """Создать заявку с уникальным ID и статусом."""


def register_home(self, home: SmartHome) -> str:
    """Зарегистрировать умный дом в реестре сервиса."""
```

**Класс `SmartHomeRegistry`:**

- Внутренний реестр для хранения объектов `SmartHome` по ключу-адресу
- Методы: `register_home()`, `get_home()`

**Особенности реализации:**

- Показания счётчиков (`water`, `electricity`) получаются через метод `get_metrics()` объекта `SmartHome`
- Заявки получают уникальный ID через хеширование описания: `hash(description) % 1000`
- Валидация описания проблемы — через `RussianStringValidator` (10-500 символов)
- Методы `format_metrics_output` и `format_issue_output` возвращают человекочитаемые строки

#### Интеграция с другими модулями

Модуль `services` взаимодействует с несколькими компонентами системы:

- **`citizens`**: класс `Human` передаётся как параметр во все методы предоставления услуг
- **`core`**: используются перечисления `Domain`, валидаторы (`NAME_VALIDATOR`, `GRADE_VALIDATOR` и др.), исключение
  `HospitalException`
- **`energy`**: класс `SmartHome` используется в `UtilitiesService` для получения метрик потребления

#### Интеграция с CLI

Функционал модуля `services` доступен через команду `services` в интерактивном интерфейсе:

```bash
# Регистрация нового жителя
> services --register --name "Анна" --surname "Иванова" --age 25 --street "Ленина" --house "10"

# Авторизация по ID
> services --login --id "USER_001"

# Просмотр данных текущего пользователя
> services --whoami

# Запись к врачу
> services --get-ticket --doctor therapist

# Заказ справки
> services --order-certificate --purpose "Для университета"

# Просмотр оценок
> services --get-grades

# Запись на курс
> services --enroll-course --name Python

# Просмотр показаний счётчиков
> services --view-metrics

# Подача заявки в ЖКХ
> services --report-issue --description "Не работает лифт в подъезде"
```

Внутренняя реализация в `cli.py` использует универсальный метод `provide_service()` каждого сервиса, который принимает
действие и необходимые параметры, а возвращает отформатированную строку для вывода.

#### Обработка ошибок

Модуль использует следующие механизмы обработки ошибок:

- **Валидация входных данных**: все пользовательские строки и числа проверяются через валидаторы из `core.utils`; при
  нарушении правил выбрасывается `ValueError`
- **Бизнес-логика**: при отсутствии мест у врача или на курсе выбрасывается специфичное исключение (`HospitalException`)
  или возвращается человекочитаемое сообщение
- **Отсутствие данных**: если дом не найден в реестре или показания ещё не собраны, выбрасывается `ValueError` с
  пояснением
- Все исключения перехватываются на уровне CLI и выводятся в формате: `Ошибка: <сообщение>`

#### Пример использования

```python
from SmartCityModel.services import Hospital, EducationService, UtilitiesService
from SmartCityModel.citizens import Human, UserRepository
from SmartCityModel.energy import SmartHome

# Создание пользователя
user_repo = UserRepository()
user_id = user_repo.register_user(
    name="Анна", surname="Иванова", age=25,
    street="Ленина", house=10, apartment=5
)
patient = user_repo.get_user(user_id)

# Работа с медицинским сервисом
hospital = Hospital("Горбольница №1", ("Ленина", 1), "HOSP_001")

# Запись к терапевту
ticket = hospital.order_ticket_to_doctor("therapist", patient)
print(ticket)  # Талон к врачу Терапевт №1. Пациент: Иванова А.

# Заказ справки
certificate = hospital.order_certificate("Для визы", patient)
print(certificate)  # Справка: Для визы ...

# Работа с образовательным сервисом
education = EducationService("Учебный центр", ("Мира", 5), "EDU_001")

# Запись на курс
enroll_result = education.enroll_course("Python", patient)
print(enroll_result)  # Вы записаны на курс 'Python'.

# Установка оценки
grade_result = education.set_grade(patient, "Python", 9)
print(grade_result)  # Оценка 9 по предмету 'Python' установлена.

# Просмотр оценок
grades = education.get_grades(patient)
print(education.format_grades_output(grades))

# Работа с коммунальным сервисом
utilities = UtilitiesService("ЖЭК", ("Ленина", 1), "UTIL_001")

# Регистрация умного дома
home = SmartHome(address=("Ленина", 10, 5), area=75)
utilities.register_home(home)

# Просмотр показаний
metrics = utilities.view_metrics(patient.address)
print(utilities.format_metrics_output(metrics))

# Подача заявки
issue = utilities.report_issue("Не работает отопление в квартире")
print(utilities.format_issue_output(issue))
```

### Модуль `transport` (Система управления транспортом)

Модуль `transport` реализует подсистему управления общественным транспортом и дорожным движением в модели умного города.
Он отвечает за мониторинг транспортных средств, расчёт времени прибытия и интеллектуальное регулирование светофоров.

#### Структура модуля

```
SmartCityModel/transport/
├── __init__.py          # Экспорт публичных классов
├── models.py            # Базовые модели: остановки, маршруты, транспорт
├── monitoring.py        # Система мониторинга транспорта (TransportMonitoringSystem)
└── traffic_control.py   # Управление трафиком: светофоры, перекрёстки, TrafficManager
```

#### Основные компоненты

##### Модели транспорта (models.py)

Классы для представления элементов транспортной инфраструктуры:

| Класс                    | Описание                                                           | Ключевые методы                                               |
|--------------------------|--------------------------------------------------------------------|---------------------------------------------------------------|
| `BusStop`                | Остановка общественного транспорта с информационным табло          | `update_passengers()`, `set_display()`, `get_status()`        |
| `RouteStop`              | Связка остановки с её порядковым номером на маршруте               | — (контейнер для связи)                                       |
| `PublicTransportVehicle` | Транспортное средство (автобус, трамвай, троллейбус)               | `report_stop_passed()`, `update_passengers()`, `get_status()` |
| `TransportRoute`         | Маршрут с последовательностью остановок и транспортными средствами | `add_vehicle()`, `get_status()`                               |

Особенности реализации:

- Все классы, представляющие устройства, наследуются от `SmartDevice` и получают уникальный `device_id`
- `BusStop` хранит количество ожидающих пассажиров и сообщение на табло, которое обновляется системой мониторинга
- `PublicTransportVehicle` отслеживает индекс последней пройденной остановки через `report_stop_passed()` — это заменяет
  необходимость в GPS-координатах
- Валидация: количество пассажиров не может быть отрицательным или превышать 60 человек

##### Система мониторинга (monitoring.py)

Класс `TransportMonitoringSystem` координирует данные о маршрутах, транспортных средствах и остановках.

**Основные методы:**

```python
def register_route(self, route: TransportRoute) -> None:
    """Регистрирует маршрут и все его остановки/транспорт в системе"""


def register_vehicle(self, vehicle: PublicTransportVehicle) -> None:
    """Регистрирует транспортное средство и связывает его с маршрутом"""


def calculate_eta(self, vehicle: PublicTransportVehicle, stop: RouteStop, route: TransportRoute) -> Optional[float]:
    """
    Рассчитывает ожидаемое время прибытия (в минутах) транспорта до остановки.
    Возвращает None, если транспорт уже проехал остановку или ещё не начал движение.
    """


def get_arrival_info(self, stop_id: str) -> dict:
    """
    Получает информацию о ближайших прибытиях транспорта на остановку.
    Обновляет табло остановки и возвращает словарь с данными для вывода.
    """
```

Алгоритм расчёта ETA:

1. Определяется индекс последней пройденной остановки транспортным средством
2. Вычисляется количество оставшихся остановок до целевой
3. Базовое время = количество остановок × среднее время между остановками
4. Добавляется случайная погрешность (0-2 минуты) для реалистичности
5. Результат округляется до одного знака после запятой

##### Управление трафиком (traffic_control.py)

Классы для интеллектуального регулирования дорожного движения:

| Класс               | Описание                                                         | Ключевые методы                                                |
|---------------------|------------------------------------------------------------------|----------------------------------------------------------------|
| `SmartTrafficLight` | Умный светофор с анализом потока и инцидентов                    | `get_traffic_request()`, `set_color()`                         |
| `Intersection`      | Перекрёсток с набором светофоров и картой конфликтов направлений | `regulate_intersection()`                                      |
| `TrafficManager`    | Адаптер для интеграции TMS и системы управления трафиком         | `prioritize_public_transport()`, `link_stop_to_intersection()` |

**Логика приоритизации в `SmartTrafficLight.get_traffic_request()`:**

Светофор анализирует данные с сенсоров и камеры, присваивая приоритет запросу:

| Условие                                                            | Приоритет | Причина             |
|--------------------------------------------------------------------|-----------|---------------------|
| Зафиксирован инцидент (авария)                                     | 100       | INCIDENT            |
| Приближается экстренный транспорт (скорая, пожарная, полиция)      | 90        | EMERGENCY           |
| Приближается общественный транспорт (автобус, трамвай, троллейбус) | 60        | PUBLIC_TRANSPORT    |
| Высокая интенсивность потока (>15 ед./мин)                         | 50        | HIGH_FLOW           |
| Ожидают пешеходы (при низком приоритете других)                    | 5         | PEDESTRIANS_WAITING |
| Базовое состояние                                                  | 10        | FLOW                |

**Регулирование перекрёстка (`Intersection.regulate_intersection()`):**

1. Собираются запросы от всех светофоров перекрёстка
2. Выбирается направление с наивысшим приоритетом (лидер)
3. Светофоры, чьи направления конфликтуют с лидером, переключаются на красный
4. Остальные светофоры получают зелёный сигнал
5. Метод возвращает `True`, если причиной переключения стал инцидент

**Интеграция через `TrafficManager`:**

Класс `TrafficManager` реализует сценарий «зелёная волна» для общественного транспорта:

```python
def prioritize_public_transport(self) -> str | None:
    """
    1. Проверяет все маршруты в TMS
    2. Для общественного транспорта находит следующую остановку
    3. Если остановка связана с перекрёстком — запрашивает приоритет
    4. Возвращает сообщение об успешной активации или None
    """
```

Метод `link_stop_to_intersection()` связывает остановку из TMS с направлением на перекрёстке, обеспечивая корректную
работу приоритизации.

#### Интеграция с другими модулями

Модуль `transport` взаимодействует с несколькими компонентами системы:

- **`core`**: используются перечисления `Domain`, `VehicleType`, `TrafficLightColor`, `Direction`; базовый класс
  `SmartDevice`; исключение `TransportException`
- **`sensors`**: `TrafficFlowSensor`, `AITrafficCamera`, `PedestrianCrossingSensor` предоставляют данные для принятия
  решений светофорами
- **`city`**: при инициализации `SmartCity` создаются районы с остановками, маршрутами и перекрёстками, которые
  регистрируются в `TransportMonitoringSystem` и `TrafficManager`

#### Интеграция с CLI

Функционал модуля `transport` доступен через команду `tms` в интерактивном интерфейсе:

```bash
# Добавить остановку
> tms --add-stop --name "Пл. Ленина"

# Создать маршрут
> tms --add-route --stops "stop_001,stop_002,stop_003"

# Добавить транспорт на маршрут
> tms --add-vehicle --route "route_001" --type bus

# Получить информацию о прибытии на остановку
> tms --arrive-stop --name "Пл. Ленина"

# Показать список маршрутов
> tms --view-routes

# Запустить приоритизацию общественного транспорта
> tms --prioritize
```

Внутренняя реализация в `cli.py` использует методы `get_arrival_info()` для получения данных о прибытии и
`prioritize_public_transport()` для активации «зелёной волны».

#### Обработка ошибок

Модуль использует исключение `TransportException` из `core.exceptions` для обработки ошибочных ситуаций:

- Отрицательное или чрезмерное количество пассажиров →
  `TransportException("Количество пассажиров не может быть отрицательным.")`
- Попытка связать остановку с несуществующим перекрёстком → `TransportException("Перекресток не найден")`
- Некорректное направление при связывании остановки с перекрёстком → `TransportException` с описанием допустимых
  направлений оси

Все исключения перехватываются на уровне CLI и выводятся в человекочитаемом виде.

#### Пример использования

```python
from SmartCityModel.transport import (
    BusStop, RouteStop, PublicTransportVehicle, TransportRoute,
    TransportMonitoringSystem, SmartTrafficLight, Intersection, TrafficManager
)
from SmartCityModel.sensors import TrafficFlowSensor, AITrafficCamera, PedestrianCrossingSensor
from SmartCityModel.core import VehicleType, TrafficLightColor, Direction

# Создание остановки
stop = BusStop("Пл. Ленина")
stop.update_passengers(5)

# Создание маршрута
route_stop1 = RouteStop(stop, index=0)
route_stop2 = RouteStop(BusStop("Вокзал"), index=1)
route = TransportRoute("route_001", [route_stop1, route_stop2])

# Создание транспорта
bus = PublicTransportVehicle(VehicleType.BUS, "route_001")
route.add_vehicle(bus)

# Регистрация в системе мониторинга
tms = TransportMonitoringSystem()
tms.register_route(route)

# Имитация движения: транспорт проехал первую остановку
bus.report_stop_passed(0)

# Запрос информации о прибытии на вторую остановку
arrival_info = tms.get_arrival_info(route_stop2.bus_stop.device_id)
print(arrival_info["arrivals"])  # [{'vehicle_id': 'bus_...', 'eta_minutes': 3.0, ...}]

# Создание светофора с сенсорами
flow_sensor = TrafficFlowSensor()
camera = AITrafficCamera()
ped_sensor = PedestrianCrossingSensor()
light = SmartTrafficLight(flow_sensor, camera, ped_sensor)

# Запрос приоритета (симуляция инцидента)
camera.detect_event(VehicleType.AMBULANCE, incident=True)
request = light.get_traffic_request()
print(request["priority"])  # 100
print(request["reason"])  # "INCIDENT"

# Создание перекрёстка и регулирование
light2 = SmartTrafficLight(TrafficFlowSensor(), AITrafficCamera())
intersection = Intersection("cross_001", [light, light2])
warning = intersection.regulate_intersection()
print(warning)  # True, если был инцидент

# Интеграция через TrafficManager
tm = TrafficManager(tms)
tm.register_intersection(intersection)
tm.link_stop_to_intersection(route_stop2.bus_stop.device_id, "cross_001", Direction.NORTH)
result = tm.prioritize_public_transport()
print(result)  # Сообщение об активации приоритета или None
```

### Модуль `ui` (Интерфейсы взаимодействия с системой)

Модуль `ui` реализует слой адаптеров между интерфейсом командной строки и бизнес-логикой системы. Каждый класс модуля
инкапсулирует логику взаимодействия с конкретной подсистемой умного города, обеспечивая разделение ответственности и
упрощение тестирования.

#### Структура модуля

```
SmartCityModel/ui/
├── __init__.py          # Экспорт всех публичных UI-классов
├── city_ui.py           # Главный интерфейс: CityUI
├── transport_ui.py      # Адаптеры для TMS и управления трафиком
├── environment_ui.py    # Адаптер для мониторинга окружающей среды
├── sensors_ui.py        # Адаптер для работы с сенсорами
├── services_ui.py       # Адаптер для общественных сервисов
├── energy_ui.py         # Адаптер для энергосистемы
└── urban_planning_ui.py # Адаптер для анализа данных городского планирования
```

#### Главный класс `CityUI` (city_ui.py)

Класс `CityUI` является точкой входа для всех пользовательских интерфейсов. Он инициализирует экземпляр ядра `SmartCity`
и создаёт экземпляры всех специализированных UI-адаптеров.

```python
class CityUI:
    def __init__(self) -> None:
        self.city = SmartCity()
        self.tms_ui = TransportSystemUI(self.city)
        self.traffic_ui = TrafficManagementUI(self.city)
        self.env_ui = EnvironmentMonitoringUI(self.city)
        self.urban_planning_ui = UrbanPlanningDataAnalysisUI(self.city)
        self.sensors_ui = SensorUI(self.city)
        self.services_ui = PublicServiceUI(self.city)
        self.energy_ui = EnergyUI(self.city)
```

Особенности реализации:

- Все под-интерфейсы получают ссылку на единый экземпляр `SmartCity`, что обеспечивает согласованность данных между
  модулями
- Класс не содержит бизнес-логики — только делегирование вызовов соответствующим адаптерам
- Инициализация всех компонентов происходит в конструкторе, что гарантирует готовность системы к работе сразу после
  создания объекта

#### Адаптеры подсистем

Каждый UI-класс предоставляет унифицированный интерфейс для CLI: методы принимают параметры, вызывают бизнес-логику и
возвращают данные в формате, готовом для отображения.

| Класс                         | Отвечает за              | Ключевые методы                                                                   |
|-------------------------------|--------------------------|-----------------------------------------------------------------------------------|
| `TransportSystemUI`           | Управление транспортом   | `add_stop()`, `add_route()`, `add_vehicle()`, `arrive_at_stop()`, `list_routes()` |
| `TrafficManagementUI`         | Регулирование трафика    | `add_intersection()`, `trigger_accident()`, `manage_flow()`                       |
| `EnvironmentMonitoringUI`     | Экологический мониторинг | `get_environment_state()`, `format_environment_state()`                           |
| `SensorUI`                    | Работа с сенсорами       | `get_district_list()`, `set_district_sensor()`, `set_smart_home_sensor()`         |
| `PublicServiceUI`             | Общественные сервисы     | `register_user()`, `login_user()`, `access_hospital()`, `access_school()`         |
| `EnergyUI`                    | Энергосистема            | `generate_report()`                                                               |
| `UrbanPlanningDataAnalysisUI` | Анализ данных            | `generate_report()`, `format_report()`                                            |

#### Принципы проектирования адаптеров

1. **Разделение ответственности**: каждый класс отвечает только за свою предметную область
2. **Форматирование вывода**: методы `format_*_output()` возвращают строки, готовые к печати в CLI, что упрощает
   изменение представления без изменения бизнес-логики
3. **Обработка ошибок**: адаптеры не перехватывают исключения бизнес-логики — они пробрасываются на уровень CLI для
   централизованной обработки
4. **Зависимость от абстракций**: все адаптеры зависят от интерфейса `SmartCity`, а не от конкретных реализаций
   подсистем

#### Интеграция с CLI

Модуль `ui` не имеет прямого интерфейса — он используется исключительно через `cli.py`. Пример взаимодействия:

```python
# В cli.py при обработке команды 'tms --add-stop --name "Пл. Ленина"'
def handle_tms(ui: TransportSystemUI, args: list[str], print_func):
    params = parse_flags(args[1:])
    name = params.get("--name")
    stop_id = ui.add_stop(name)  # Вызов метода адаптера
    print_func(f"Остановка добавлена: {stop_id}")
```

Адаптер `TransportSystemUI` в свою очередь делегирует вызов ядру:

```python
# В ui/transport_ui.py
def add_stop(self, name: str) -> str:
    stop = BusStop(name)  # Создание объекта бизнес-логики
    self.city.register_stop(stop)  # Регистрация через ядро
    return stop.device_id
```

#### Пример использования

```python
from SmartCityModel.ui import CityUI

# Инициализация главного интерфейса
city_ui = CityUI()

# Регистрация пользователя через адаптер сервисов
user_id = city_ui.services_ui.register_user(
    name="Анна", surname="Иванова", age=25,
    street="Ленина", house=10
)
print(f"ID пользователя: {user_id}")

# Добавление остановки через адаптер транспорта
stop_id = city_ui.tms_ui.add_stop("Пл. Ленина")
print(f"Остановка: {stop_id}")

# Получение состояния окружающей среды
env_state = city_ui.env_ui.get_environment_state()
output = city_ui.env_ui.format_environment_state(env_state)
print(output)

# Оптимизация энергии
energy_report = city_ui.energy_ui.generate_report()
print(energy_report)
```

### Модуль `urban_planning` (Анализ данных городского планирования)

Модуль `urban_planning` реализует подсистему сбора и анализа данных для улучшения городской планировки. Он агрегирует
метрики из различных источников и предоставляет рекомендации по развитию районов.

#### Структура модуля

```
SmartCityModel/urban_planning/
├── __init__.py          # Экспорт: District, UrbanPlanningDataAnalyzer
├── analyzer.py          # Класс UrbanPlanningDataAnalyzer
└── models.py            # Класс District
```

#### Основные компоненты

##### Класс `District` (models.py)

Модель района умного города, агрегирующая данные от различных подсистем.

**Атрибуты:**

- `district_id` — уникальный идентификатор района
- `air_quality_sensors`, `temperature_sensors`, `humidity_sensors`, `noise_sensors` — списки экологических сенсоров
- `traffic_sensors` — сенсоры транспортного потока
- `intersections` — перекрёстки с интеллектуальным управлением
- `smart_homes`, `lights`, `storages`, `generators` — объекты энергосистемы
- `metrics_readings` — история замеров метрик
- `last_updated` — время последнего обновления данных

**Методы:**

| Метод                                      | Описание                                                         |
|--------------------------------------------|------------------------------------------------------------------|
| `register_intersection(intersection)`      | Добавляет перекрёсток в район                                    |
| `auto_collect_sensor_data(ecology: float)` | Собирает текущие показания сенсоров и сохраняет метрики          |
| `get_average(metric: str)`                 | Возвращает среднее значение указанной метрики по истории замеров |
| `get_all_intersections()`                  | Возвращает список всех перекрёстков района                       |

##### Класс `UrbanPlanningDataAnalyzer` (analyzer.py)

Анализатор данных для градостроительного планирования.

**Методы:**

| Метод                                                      | Описание                                                        |
|------------------------------------------------------------|-----------------------------------------------------------------|
| `register_district(district: District)`                    | Регистрирует район для последующего анализа                     |
| `calculate_metric(district_id, metric_type, ecology=None)` | Рассчитывает значение конкретной метрики для района             |
| `generate_planning_report(district_ids=None)`              | Генерирует структурированный отчёт с рекомендациями по развитию |

**Поддерживаемые метрики (PlanningMetricType):**

| Метрика                  | Описание                                 | Диапазон |
|--------------------------|------------------------------------------|----------|
| `ECOLOGY_SCORE`          | Экологический рейтинг района             | 0–100    |
| `TRANSPORT_LOAD`         | Нагрузка на транспортную инфраструктуру  | 0–100    |
| `INFRASTRUCTURE_DENSITY` | Плотность застройки и инфраструктуры     | 0–100    |
| `LIVEABILITY_INDEX`      | Композитный индекс пригодности для жизни | 0–100    |

**Логика расчёта рекомендаций:**

Метод `calculate_metric` возвращает не только числовое значение, но и текстовую рекомендацию:

```python
{
    "district_id": "center_1",
    "metric": "ecology_score",
    "value": 72.5,
    "timestamp": "2026-04-05T14:30:00",
    "recommendation": "Удовлетворительная экология. Рассмотреть высадку деревьев вдоль магистралей."
}
```

#### Интеграция с CLI

Функционал модуля доступен через команду `data` в интерактивном интерфейсе:

```bash
# Сгенерировать и вывести отчёт по городскому планированию
> data --print-report
```

#### Пример использования

```python
from SmartCityModel.urban_planning import UrbanPlanningDataAnalyzer, District
from SmartCityModel.core import PlanningMetricType

# Инициализация анализатора
analyzer = UrbanPlanningDataAnalyzer()

# Регистрация района (обычно выполняется при инициализации SmartCity)
# analyzer.register_district(district)

# Расчёт конкретной метрики
result = analyzer.calculate_metric(
    district_id="center_1",
    metric_type=PlanningMetricType.ECOLOGY_SCORE,
    ecology=0.85  # нормализованное значение от сенсоров
)
print(result["recommendation"])

# Генерация полного отчёта
report = analyzer.generate_planning_report(district_ids=["center_1", "suburb_1"])
for district in report["districts"]:
    print(f"Район {district['district_id']}:")
    for metric, data in district["metrics"].items():
        print(f"  {metric}: {data['value']} — {data['recommendation']}")
```

## Тестирование

Проект покрыт модульными тестами, написанными с использованием фреймворка `pytest`. Тесты расположены в директории
`tests/` и сгруппированы по модулям системы.

### Структура тестов

| Файл                     | Покрываемый модуль                                       |
|--------------------------|----------------------------------------------------------|
| `test_core.py`           | Базовые компоненты: перечисления, валидаторы, исключения |
| `test_citizens.py`       | Модуль жителей города                                    |
| `test_city.py`           | Ядро системы `SmartCity`                                 |
| `test_energy.py`         | Энергосберегающие технологии                             |
| `test_environment.py`    | Мониторинг окружающей среды                              |
| `test_sensors.py`        | Система сбора данных с датчиков                          |
| `test_services.py`       | Общественные сервисы                                     |
| `test_transport.py`      | Управление транспортом                                   |
| `test_ui.py`             | Интерфейсы взаимодействия                                |
| `test_urban_planning.py` | Анализ данных городского планирования                    |

### Запуск тестов

```bash
# Все тесты с подробным выводом
pytest tests/ -v

# Тесты конкретного модуля
pytest tests/test_core.py -v

# Тесты с отчётом о покрытии
pytest --cov=SmartCityModel --cov-report=term-missing tests/
```

### Требования к тестам

- Каждый публичный метод покрыт хотя бы одним тестом
- Тесты изолированы и не зависят от порядка выполнения
- Для проверки исключений используется `pytest.raises()`
- Названия тестовых методов отражают проверяемое поведение: `test_<method>_<scenario>`

## Структура проекта SmartCityModel

```
ppois/
└── SmartCityModel/
    ├── __init__.py              # Инициализация пакета
    ├── __main__.py              # Точка входа для python -m SmartCityModel
    ├── cli.py                   # Интерфейс командной строки (парсинг аргументов, обработка команд)
    ├── requirements-test.txt    # Зависимости для тестирования
    │
    ├── core/                    # Базовые компоненты и утилиты
    │   ├── __init__.py
    │   ├── base.py              # Базовый класс SmartDevice
    │   ├── enums.py             # Перечисления (Domain, VehicleType, уровни сенсоров и др.)
    │   ├── exceptions.py        # Кастомные исключения
    │   ├── helpers.py           # Вспомогательные функции для CLI
    │   └── utils.py             # Валидаторы входных данных
    │
    ├── citizens/                # Модуль жителей города
    │   ├── __init__.py
    │   ├── models.py            # Класс Human
    │   └── repository.py        # Класс UserRepository
    │
    ├── city/                    # Ядро системы
    │   ├── __init__.py
    │   └── smart_city.py        # Класс SmartCity
    │
    ├── data/                    # Хранение данных
    │   └── users_db.json        # JSON-файл с данными пользователей
    │
    ├── energy/                  # Энергосберегающие технологии
    │   ├── __init__.py
    │   ├── devices.py           # SmartThermostat, SmartHome, SmartLight
    │   ├── generation.py        # SolarPanel, WindTurbine, BatteryStorage
    │   ├── grid.py              # CityEnergyGrid
    │   └── lighting.py          # SmartLightningSystem
    │
    ├── environment/             # Мониторинг окружающей среды
    │   ├── __init__.py
    │   └── monitoring.py        # EnvironmentMonitoringSystem
    │
    ├── sensors/                 # Система сбора данных
    │   ├── __init__.py
    │   ├── base_sensor.py       # Абстрактный класс Sensor
    │   ├── environment_sensors.py  # AirQualitySensor, TemperatureSensor, HumiditySensor, NoiseSensor
    │   ├── traffic_sensors.py      # TrafficFlowSensor, PedestrianCrossingSensor, AITrafficCamera
    │   └── energy_sensors.py       # LightLevelSensor, MotionSensor, WaterMeter, ElectricityMeter
    │
    ├── services/                # Общественные сервисы
    │   ├── __init__.py
    │   ├── base.py              # Абстрактный класс PublicService
    │   ├── education.py         # EducationService
    │   ├── hospital.py          # Hospital
    │   └── utilities.py         # UtilitiesService, SmartHomeRegistry
    │
    ├── transport/               # Управление транспортом
    │   ├── __init__.py
    │   ├── models.py            # BusStop, RouteStop, PublicTransportVehicle, TransportRoute
    │   ├── monitoring.py        # TransportMonitoringSystem
    │   └── traffic_control.py   # SmartTrafficLight, Intersection, TrafficManager
    │
    ├── ui/                      # Интерфейсы взаимодействия
    │   ├── __init__.py
    │   ├── city_ui.py           # CityUI (главный адаптер)
    │   ├── energy_ui.py         # EnergyUI
    │   ├── environment_ui.py    # EnvironmentMonitoringUI
    │   ├── sensors_ui.py        # SensorUI
    │   ├── services_ui.py       # PublicServiceUI
    │   ├── transport_ui.py      # TransportSystemUI, TrafficManagementUI
    │   └── urban_planning_ui.py # UrbanPlanningDataAnalysisUI
    │
    ├── urban_planning/          # Анализ данных городского планирования
    │   ├── __init__.py
    │   ├── analyzer.py          # UrbanPlanningDataAnalyzer
    │   └── models.py            # District
    │
    └── tests/                   # Модульные тесты
        ├── test_citizens.py
        ├── test_city.py
        ├── test_core.py
        ├── test_energy.py
        ├── test_environment.py
        ├── test_sensors.py
        ├── test_services.py
        ├── test_transport.py
        ├── test_ui.py
        └── test_urban_planning.py
```
