from decimal import Decimal, InvalidOperation
from typing import Union, Optional


class ValidationError(Exception):
    """Специальное исключение для ошибок валидации."""
    pass


class RussianStringValidator:
    def __init__(self, min_length: int = 1, max_length: int = 100, allow_spaces: bool = False) -> None:
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
        self.allow_spaces = allow_spaces

        self.russian_letters = set(
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        )

    def validate(self, value: str) -> str:
        """
        Проверяет строку. Если все хорошо — возвращает очищенную строку.
        Если нет — выбрасывает ValidationError с понятным сообщением.
        """

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValidationError("Строка не может быть пустой или состоять из пробелов")

        if len(cleaned_value) < self.min_length:
            raise ValidationError(f"Строка слишком короткая (минимум {self.min_length} симв.)")

        if len(cleaned_value) > self.max_length:
            raise ValidationError(f"Строка слишком длинная (максимум {self.max_length} симв.)")

        has_letter = False
        for char in cleaned_value:
            if char == '.' or char == '-':
                continue
            elif char == ' ' and self.allow_spaces:
                continue
            elif char in self.russian_letters:
                has_letter = True
            else:

                raise ValidationError(f"Недопустимый символ: '{char}' (разрешены только русские буквы, дефисы и точки)")

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

        if value is None:
            raise NumberValidationError("Значение не может быть пустым (None)")

        if isinstance(value, bool):
            raise NumberValidationError("Булевый тип не допускается")

        str_value = str(value).strip()

        if not str_value:
            raise NumberValidationError("Строка не может быть пустой")

        if not str_value.lstrip('-').isdigit():
            raise NumberValidationError(f"Недопустимые символы в числе: '{str_value}'")

        if str_value.startswith('-') and not self.allow_negative:
            raise NumberValidationError("Отрицательные числа не разрешены")

        digit_count = len(str_value.lstrip('-'))
        if digit_count > self.max_digits:
            raise NumberValidationError(f"Слишком много цифр (максимум {self.max_digits})")

        try:
            int_value = int(str_value)
        except (ValueError, OverflowError):
            raise NumberValidationError("Не удалось преобразовать в целое число")

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

        if value is None:
            raise NumberValidationError("Значение не может быть пустым (None)")

        if isinstance(value, bool):
            raise NumberValidationError("Булевый тип не допускается")

        str_value = str(value).strip()

        if not str_value:
            raise NumberValidationError("Строка не может быть пустой")

        str_value = str_value.replace(',', '.')

        try:
            decimal_value = Decimal(str_value)
        except InvalidOperation:
            raise NumberValidationError(f"Недопустимый формат числа: '{str_value}'")

        if decimal_value < 0 and not self.allow_negative:
            raise NumberValidationError("Отрицательные числа не разрешены")

        digits_only = str_value.replace('-', '').replace('.', '')
        if len(digits_only) > self.max_digits:
            raise NumberValidationError(f"Слишком много цифр (максимум {self.max_digits})")

        if '.' in str_value:
            decimal_part = str_value.split('.')[1]
            if len(decimal_part) > self.max_decimal_places:
                raise NumberValidationError(f"Слишком много знаков после запятой (максимум {self.max_decimal_places})")

        try:
            float_value = float(decimal_value)
        except (ValueError, OverflowError):
            raise NumberValidationError("Не удалось преобразовать в число с плавающей точкой")

        if self.min_value is not None and float_value < self.min_value:
            raise NumberValidationError(f"Число меньше минимума ({self.min_value})")
        if self.max_value is not None and float_value > self.max_value:
            raise NumberValidationError(f"Число больше максимума ({self.max_value})")

        return float_value


class LatinStringValidator:
    """
    Валидатор для строк на латинице.
    Разрешает латинские буквы, цифры и базовые символы.
    """

    def __init__(
            self,
            min_length: int = 1,
            max_length: int = 100,
            allow_hyphen: bool = False,
            allow_spaces: bool = False,
            allow_underscore: bool = False
    ) -> None:
        """
        Инициализация валидатора.

        :param min_length: Минимальная допустимая длина строки.
        :param max_length: Максимальная допустимая длина.
        :param allow_hyphen: Разрешен ли дефис (-).
        :param allow_spaces: Разрешены ли пробелы внутри строки.
        """
        if min_length < 1:
            raise ValueError("Минимальная длина не может быть меньше 1")
        if max_length < min_length:
            raise ValueError("Максимальная длина не может быть меньше минимальной")

        self.min_length = min_length
        self.max_length = max_length
        self.allow_hyphen = allow_hyphen
        self.allow_spaces = allow_spaces
        self.allow_underscore = allow_underscore

        self.latin_letters = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    def validate(self, value: str) -> str:
        """
        Проверяет строку. Если все хорошо — возвращает очищенную строку.
        Если нет — выбрасывает ValidationError.
        """

        if value is None:
            raise ValidationError("Значение не может быть пустым (None)")

        cleaned_value = value.strip()

        if len(cleaned_value) < self.min_length:
            raise ValidationError(f"Строка слишком короткая (минимум {self.min_length} симв.)")

        if len(cleaned_value) > self.max_length:
            raise ValidationError(f"Строка слишком длинная (максимум {self.max_length} симв.)")

        has_letter = False
        for char in cleaned_value:
            if char in self.latin_letters:
                has_letter = True
            elif self.allow_hyphen and char == '-':
                continue
            elif self.allow_spaces and char == ' ':
                continue
            elif self.allow_underscore and char == '_':
                continue
            else:
                raise ValidationError("Невалидная строка")

        if not has_letter:
            raise ValidationError("Невалидная строка")

        return cleaned_value


class IdentifierValidator:
    """
    Валидатор для идентификаторов (ID).
    Разрешает латинские буквы, цифры и нижнее подчеркивание.
    Подходит для имен переменных, технических идентификаторов.
    """

    def __init__(self, min_length: int = 1, max_length: int = 50) -> None:
        """
        Инициализация валидатора.

        :param min_length: Минимальная допустимая длина.
        :param max_length: Максимальная допустимая длина.
        """
        if min_length < 1:
            raise ValueError("Минимальная длина не может быть меньше 1")
        if max_length < min_length:
            raise ValueError("Максимальная длина не может быть меньше минимальной")

        self.min_length = min_length
        self.max_length = max_length

        self.latin_letters = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.digits = set("0123456789")

    def validate(self, value: str) -> str:
        """
        Проверяет идентификатор.
        Возвращает очищенную строку или выбрасывает ValidationError.
        """
        if value is None:
            raise ValidationError("ID не может быть пустым (None)")

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValidationError("ID не может быть пустым")

        if len(cleaned_value) < self.min_length:
            raise ValidationError(f"ID слишком короткий (минимум {self.min_length} симв.)")

        if len(cleaned_value) > self.max_length:
            raise ValidationError(f"ID слишком длинный (максимум {self.max_length} симв.)")

        allowed_chars = self.latin_letters | self.digits | {'_'}
        for char in cleaned_value:
            if char not in allowed_chars:
                raise ValidationError(
                    f"Недопустимый символ в ID: '{char}'. "
                    f"Разрешены только латинские буквы, цифры, нижнее подчеркивание и дефис"
                )

        return cleaned_value


NAME_VALIDATOR = RussianStringValidator(min_length=2, max_length=50)

ADDRESS_VALIDATOR = RussianStringValidator(min_length=2, max_length=100)

AGE_VALIDATOR = NumberValidator(min_value=0, max_value=150, allow_negative=False)

HOUSE_NUMBER_VALIDATOR = NumberValidator(min_value=1, max_value=9999, allow_negative=False)

PASSENGER_VALIDATOR = NumberValidator(min_value=0, max_value=1000, allow_negative=False)

GRADE_VALIDATOR = NumberValidator(min_value=0, max_value=10, allow_negative=False)

SENSOR_VALUE_VALIDATOR = NumberValidator(min_value=-60, max_value=1000000, allow_negative=True)

ID_VALIDATOR = IdentifierValidator()

LATIN_STR_VALIDATOR = LatinStringValidator(
    min_length=2,
    max_length=100,
    allow_hyphen=True,
    allow_spaces=True
)
