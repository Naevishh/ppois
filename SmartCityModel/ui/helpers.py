def show_menu(options, get_user_input, print_func, prompt="Выберите опцию:"):
    """
    Универсальная функция для вывода меню.
    options: список кортежей [(ключ, название), ...]
    Возвращает выбранный ключ или None при ошибке.
    """
    print_func(prompt)
    for i, (key, label) in enumerate(options, 1):
        print_func(f"{i}. {label}")

    try:
        choice = int(get_user_input())
        if 1 <= choice <= len(options):
            return options[choice - 1][0]
        print_func("Ошибка: номер вне диапазона")
    except ValueError:
        print_func("Ошибка: нужно ввести число")

    return None
