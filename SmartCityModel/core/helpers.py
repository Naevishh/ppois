# ui/helpers.py

import time
from typing import Any


def smooth_print(text: str, print_func, char_delay: float = 0.02, line_delay: float = 0.05):
    """
    Плавный посимвольный вывод текста (typewriter-эффект).

    :param text: текст для вывода
    :param print_func: функция для вывода (например, print)
    :param char_delay: задержка между символами в секундах
    :param line_delay: дополнительная задержка после каждой строки
    """
    for line in text.split('\n'):
        for char in line:
            print_func(char, end='', flush=True)
            time.sleep(char_delay)
        print_func()  # перенос строки
        time.sleep(line_delay)


def show_menu(options: list, get_user_input, print_func, prompt: str = "Выберите опцию:") -> str | int | Any | None:
    """
    Универсальная функция для вывода меню.
    options: список кортежей [(ключ, название), ...]
    Возвращает выбранный ключ или None при ошибке.
    """
    print_func()
    # Важно: создаём копию, чтобы не модифицировать исходный список при каждом вызове
    options_with_exit = options + [('', "Выход")]

    print_func(prompt)
    for i, (key, label) in enumerate(options_with_exit, 1):
        print_func(f"{i}. {label}")

    print_func()
    while True:
        try:
            choice = int(get_user_input())
            if 1 <= choice <= len(options_with_exit):
                return options_with_exit[choice - 1][0]
            print_func(f"Ошибка: введите число от 1 до {len(options_with_exit)}")
        except ValueError:
            print_func("Ошибка: нужно ввести число")
        except KeyboardInterrupt:
            print_func("\nВвод прерван пользователем.")
            return None

def print_help(print_func, commands: list[tuple[str, str]]):
    ext_commands= commands
    for (command, desc) in commands:
        print_func(f"{command}     {desc}")

if __name__=='__main__':
    ops=[(1, "op1"), (2, "op2")]
    k=show_menu(ops, input, print)
