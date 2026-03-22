from decimal import Decimal, InvalidOperation
from typing import Union, Optional, Callable


class ValidationError(Exception):
    """Специальное исключение для ошибок валидации."""
    pass


class StringValidator:
    def __init__(self, min_length: int = 1, max_length: int = 100) -> None:
        """
        Инициализация валидатора.
        :param min_length: Минимальная допустимая длина строки.
        :param max_length: Максимальная допустимая длина (защита от длинных строк).
        """
        if min_length < 1:
            raise ValueError("Минимальная длина не может быть меньше 1")
        if max_length < min_length:
            raise ValueError("Максимальная длина не может быть меньше минимальной")

        self.min_length = min_length
        self.max_length = max_length

        # Набор допустимых русских букв (включая ё)
        self.russian_letters = set(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        )

    def validate(self, value: str) -> str:
        """
        Проверяет строку. Если все хорошо — возвращает очищенную строку.
        Если нет — выбрасывает ValidationError с понятным сообщением.
        """

        # 2. Убираем лишние пробелы по краям (пользователь часто ставит пробелы случайно)
        cleaned_value = value.strip()

        # 3. Проверка на пустоту (после trim)
        if not cleaned_value:
            raise ValidationError("Строка не может быть пустой или состоять из пробелов")

        # 4. Проверка длины (защита от очень длинных строк)
        if len(cleaned_value) < self.min_length:
            raise ValidationError(f"Строка слишком короткая (минимум {self.min_length} симв.)")

        if len(cleaned_value) > self.max_length:
            raise ValidationError(f"Строка слишком длинная (максимум {self.max_length} симв.)")

        # 5. Посимвольная проверка (Белый список)
        has_letter = False
        for char in cleaned_value:
            if char == '.':
                continue  # Точки разрешены
            elif char in self.russian_letters:
                has_letter = True  # Нашли русскую букву
            else:
                # Сюда попадут цифры, латиница, пробелы внутри, смайлики и т.д.
                raise ValidationError(f"Недопустимый символ: '{char}' (разрешены только русские буквы и точки)")

        # 6. Проверка обязательного наличия букв
        if not has_letter:
            raise ValidationError("Строка должна содержать хотя бы одну букву")

        return cleaned_value


class NumberValidationError(Exception):
    """Специальное исключение для ошибок валидации чисел."""
    pass


class NumberValidator:
    def __init__(
            self,
            min_value: Optional[Union[int, float]] = None,
            max_value: Optional[Union[int, float]] = None,
            max_digits: int = 15,
            max_decimal_places: int = 5,
            allow_negative: bool = True
    ) -> None:
        """
        Инициализация валидатора чисел.

        :param min_value: Минимальное допустимое значение (None = без ограничений)
        :param max_value: Максимальное допустимое значение (None = без ограничений)
        :param max_digits: Максимальное количество цифр (защита от длинных чисел)
        :param max_decimal_places: Максимальное количество знаков после запятой (для float)
        :param allow_negative: Разрешены ли отрицательные числа
        """
        if max_digits < 1:
            raise ValueError("max_digits должен быть >= 1")
        if max_decimal_places < 0:
            raise ValueError("max_decimal_places не может быть отрицательным")
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError("min_value не может быть больше max_value")

        self.min_value = min_value
        self.max_value = max_value
        self.max_digits = max_digits
        self.max_decimal_places = max_decimal_places
        self.allow_negative = allow_negative

    def validate_int(self, value: Union[str, int]) -> int:
        """
        Валидация целого числа.
        Возвращает int, если успешно.
        """
        # 1. Проверка типа
        if value is None:
            raise NumberValidationError("Значение не может быть пустым (None)")

        if isinstance(value, bool):
            raise NumberValidationError("Булевый тип не допускается")

        # 2. Преобразование к строке для анализа
        str_value = str(value).strip()

        if not str_value:
            raise NumberValidationError("Строка не может быть пустой")

        # 3. Проверка на допустимые символы (цифры и минус)
        if not str_value.lstrip('-').isdigit():
            raise NumberValidationError(f"Недопустимые символы в числе: '{str_value}'")

        # 4. Проверка на отрицательность
        if str_value.startswith('-') and not self.allow_negative:
            raise NumberValidationError("Отрицательные числа не разрешены")

        # 5. Проверка длины (защита от переполнения)
        digit_count = len(str_value.lstrip('-'))
        if digit_count > self.max_digits:
            raise NumberValidationError(f"Слишком много цифр (максимум {self.max_digits})")

        # 6. Преобразование в int
        try:
            int_value = int(str_value)
        except (ValueError, OverflowError):
            raise NumberValidationError("Не удалось преобразовать в целое число")

        # 7. Проверка диапазона
        if self.min_value is not None and int_value < self.min_value:
            raise NumberValidationError(f"Число меньше минимума ({self.min_value})")
        if self.max_value is not None and int_value > self.max_value:
            raise NumberValidationError(f"Число больше максимума ({self.max_value})")

        return int_value

    def validate_float(self, value: Union[str, int, float]) -> float:
        """
        Валидация числа с плавающей точкой.
        Возвращает float, если успешно.
        """
        # 1. Проверка типа
        if value is None:
            raise NumberValidationError("Значение не может быть пустым (None)")

        if isinstance(value, bool):
            raise NumberValidationError("Булевый тип не допускается")

        # 2. Преобразование к строке и нормализация
        str_value = str(value).strip()

        if not str_value:
            raise NumberValidationError("Строка не может быть пустой")

        # Замена запятой на точку (для русской раскладки)
        str_value = str_value.replace(',', '.')

        # 3. Проверка формата с помощью Decimal (точнее, чем float)
        try:
            decimal_value = Decimal(str_value)
        except InvalidOperation:
            raise NumberValidationError(f"Недопустимый формат числа: '{str_value}'")

        # 4. Проверка на отрицательность
        if decimal_value < 0 and not self.allow_negative:
            raise NumberValidationError("Отрицательные числа не разрешены")

        # 5. Проверка количества цифр
        # Убираем знак и точку для подсчета цифр
        digits_only = str_value.replace('-', '').replace('.', '')
        if len(digits_only) > self.max_digits:
            raise NumberValidationError(f"Слишком много цифр (максимум {self.max_digits})")

        # 6. Проверка знаков после запятой
        if '.' in str_value:
            decimal_part = str_value.split('.')[1]
            if len(decimal_part) > self.max_decimal_places:
                raise NumberValidationError(f"Слишком много знаков после запятой (максимум {self.max_decimal_places})")

        # 7. Преобразование в float
        try:
            float_value = float(decimal_value)
        except (ValueError, OverflowError):
            raise NumberValidationError("Не удалось преобразовать в число с плавающей точкой")

        # 8. Проверка диапазона
        if self.min_value is not None and float_value < self.min_value:
            raise NumberValidationError(f"Число меньше минимума ({self.min_value})")
        if self.max_value is not None and float_value > self.max_value:
            raise NumberValidationError(f"Число больше максимума ({self.max_value})")

        return float_value


class SafeInput:
    """Помощник для безопасного ввода с валидацией."""

    @staticmethod
    def get_string(prompt: str, validator: StringValidator, get_input_func: Callable[[], str],
                   print_func: Callable[[str], None]) -> str:
        print_func(prompt)
        while True:
            try:
                raw = get_input_func()
                return validator.validate(raw)
            except Exception as e:
                print_func(f"❌ Ошибка: {e}. Попробуйте снова.")

    @staticmethod
    def get_int(prompt: str, validator: NumberValidator, get_input_func: Callable[[], str],
                print_func: Callable[[str], None]) -> int:
        print_func(prompt)
        while True:
            try:
                raw = get_input_func()
                return validator.validate_int(raw)
            except Exception as e:
                print_func(f"❌ Ошибка: {e}. Попробуйте снова.")

    @staticmethod
    def get_float(prompt: str, validator: NumberValidator, get_input_func: Callable[[], str],
                  print_func: Callable[[str], None]) -> float:
        print_func(prompt)
        while True:
            try:
                raw = get_input_func()
                return validator.validate_float(raw)
            except Exception as e:
                print_func(f"❌ Ошибка: {e}. Попробуйте снова.")


# Глобальные экземпляры валидаторов для удобного импорта
# Для имён (ФИО, названия остановок, улиц)
NAME_VALIDATOR = StringValidator(min_length=2, max_length=50)

# Для адресов (улицы, названия)
ADDRESS_VALIDATOR = StringValidator(min_length=2, max_length=100)

# Для возраста (0-150 лет)
AGE_VALIDATOR = NumberValidator(min_value=0, max_value=150, allow_negative=False)

# Для номеров домов (1-9999)
HOUSE_NUMBER_VALIDATOR = NumberValidator(min_value=1, max_value=9999, allow_negative=False)

# Для количества пассажиров (0-1000)
PASSENGER_VALIDATOR = NumberValidator(min_value=0, max_value=1000, allow_negative=False)

# Для оценок (1-10)
GRADE_VALIDATOR = NumberValidator(min_value=0, max_value=10, allow_negative=False)

SENSOR_VALUE_VALIDATOR = NumberValidator(min_value=-60, max_value=1000000, allow_negative=True)
