from typing import Union, Optional
from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    """Специальное исключение для ошибок валидации."""
    pass


class StringValidator:
    def __init__(self, min_length: int = 1, max_length: int = 100):
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
        # 1. Проверка типа данных (защита от None, int, list и т.д.)
        if not isinstance(value, str):
            raise ValidationError(f"Ожидалась строка, а получен тип: {type(value).__name__}")

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

    @staticmethod
    def get_valid_input(prompt: str, str_validator: 'StringValidator') -> str:
        """
        Функция для безопасного ввода от пользователя.
        Будет спрашивать до тех пор, пока пользователь не введет корректное значение.
        """
        while True:
            try:
                user_input = input(prompt)
                # Пытаемся валидировать
                valid_string = str_validator.validate(user_input)
                return valid_string
            except ValidationError as err:
                print(f"❌ Ошибка ввода: {err}")
                print("Попробуйте еще раз.\n")
            except KeyboardInterrupt:
                print("\n\n⚠️ Ввод прерван пользователем.")
                exit(0)
            except Exception as err:
                # Ловим любые другие непредвиденные ошибки, чтобы программа не упала
                print(f"⚠️ Неожиданная ошибка: {err}")
                print("Попробуйте еще раз.\n")


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
    ):
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

    @staticmethod
    def get_valid_int(prompt: str, validator: 'NumberValidator') -> int:
        """Запрос целого числа у пользователя с повторными попытками."""
        while True:
            try:
                user_input = input(prompt)
                return validator.validate_int(user_input)
            except NumberValidationError as e:
                print(f"❌ Ошибка: {e}")
                print("Попробуйте еще раз.\n")
            except KeyboardInterrupt:
                print("\n\n⚠️ Ввод прерван пользователем.")
                exit(0)
            except Exception as e:
                print(f"⚠️ Неожиданная ошибка: {e}")
                print("Попробуйте еще раз.\n")

    @staticmethod
    def get_valid_float(prompt: str, validator: 'NumberValidator') -> float:
        """Запрос дробного числа у пользователя с повторными попытками."""
        while True:
            try:
                user_input = input(prompt)
                return validator.validate_float(user_input)
            except NumberValidationError as e:
                print(f"❌ Ошибка: {e}")
                print("Попробуйте еще раз.\n")
            except KeyboardInterrupt:
                print("\n\n⚠️ Ввод прерван пользователем.")
                exit(0)
            except Exception as e:
                print(f"⚠️ Неожиданная ошибка: {e}")
                print("Попробуйте еще раз.\n")


# ==========================================
# Пример использования и тестирования
# ==========================================

# ==========================================
# Пример использования и тестирования
# ==========================================
if __name__ == "__main__":
    # Создаем валидатор: от 1 до 50 символов
    validator = StringValidator(min_length=1, max_length=50)

    print("=== Тестирование валидатора ===")

    # Сценарий 1: Интерактивный ввод (для преподавателя)
    print("\n1. Попробуйте ввести значение (программа не примет невалидные данные):")
    result = StringValidator.get_valid_input("Введите название (рус. буквы и точки): ", validator)
    print(f"✅ Успешно принято: '{result}'")

    # Сценарий 2: Автоматические тесты (попытка "сломать" программу)
    print("\n2. Автоматические тесты на прочность:")

    test_cases = [
        ("Пустая строка", ""),
        ("Только пробелы", "   "),
        ("Только точки", "..."),
        ("Есть цифры", "Привет123"),
        ("Есть латиница", "HelloПривет"),
        ("Есть спецсимволы", "Привет!"),
        ("None (пустота)", None),
        ("Число вместо строки", 12345),
        ("Слишком длинная", "А" * 1000),
        ("Валидная строка", "Анна.Каренина"),
        ("Валидная с точкой", "Точка.В.Конце"),
    ]

    for name, test_value in test_cases:
        try:
            validator.validate(test_value)
            print(f"✅ Тест '{name}': Пройден (значение: {test_value})")
        except ValidationError as e:
            print(f"⛔ Тест '{name}': Отклонен ({e})")
        except Exception as e:
            print(f"💥 Тест '{name}': Критическая ошибка ({e})")

        # Создаем валидатор для целых чисел (от 1 до 1000)
        int_validator = NumberValidator(min_value=1, max_value=1000, allow_negative=False)

        # Создаем валидатор для дробных чисел (от 0.0 до 999.99)
        float_validator = NumberValidator(
            min_value=0.0,
            max_value=999.99,
            max_decimal_places=2,
            allow_negative=False
        )

        print("=== Тестирование NumberValidator ===\n")

        # Сценарий 1: Интерактивный ввод
        print("1. Интерактивный ввод (попробуйте сломать):")
        try:
            user_int = NumberValidator.get_valid_int("Введите целое число (1-1000): ", int_validator)
            print(f"✅ Принято целое: {user_int} (тип: {type(user_int).__name__})")

            user_float = NumberValidator.get_valid_float("Введите дробное число (0-999.99): ", float_validator)
            print(f"✅ Принято дробное: {user_float} (тип: {type(user_float).__name__})")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        # Сценарий 2: Автоматические тесты
        print("\n2. Автоматические тесты на прочность:")

        test_cases = [
            ("Пустая строка", ""),
            ("Только пробелы", "   "),
            ("None", None),
            ("Буквы", "abc"),
            ("Спецсимволы", "12@34"),
            ("Слишком длинное", "1" * 100),
            ("Отрицательное (запрещено)", "-5"),
            ("Выход за максимум", "1001"),
            ("Валидное целое", "42"),
            ("Запятая вместо точки", "3,14"),
            ("Много знаков после запятой", "3.14159265"),
            ("Валидное дробное", "123.45"),
            ("Булевый тип", True),
        ]

        print("\n--- Тесты для FLOAT ---")
        for name, test_value in test_cases:
            try:
                result = float_validator.validate_float(test_value)
                print(f"✅ Тест '{name}': Пройден ({test_value} -> {result})")
            except NumberValidationError as e:
                print(f"⛔ Тест '{name}': Отклонен ({e})")
            except Exception as e:
                print(f"💥 Тест '{name}': Критическая ошибка ({type(e).__name__}: {e})")

        print("\n--- Тесты для INT ---")
        int_test_cases = [
            ("Валидное целое", "100"),
            ("Дробное в int", "10.5"),
            ("Отрицательное", "-10"),
        ]
        for name, test_value in int_test_cases:
            try:
                result = int_validator.validate_int(test_value)
                print(f"✅ Тест '{name}': Пройден ({test_value} -> {result})")
            except NumberValidationError as e:
                print(f"⛔ Тест '{name}': Отклонен ({e})")
            except Exception as e:
                print(f"💥 Тест '{name}': Критическая ошибка ({type(e).__name__}: {e})")