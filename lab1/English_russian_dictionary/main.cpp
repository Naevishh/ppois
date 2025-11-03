/**
 * @file main.cpp
 * @brief Главный модуль программы для работы со словарем
 * @details
 * Этот файл содержит точку входа в программу и реализацию пользовательского интерфейса
 * для работы с англо-русским словарем. Программа предоставляет возможности добавления,
 * удаления, поиска и изменения слов в словаре, а также загрузки данных из файла.
 *
 * @author Ященко Александра
 * @see Dictionary.h
 * @see String_validator.h
 */

#include <iostream>
#include <string>
#include <windows.h>
#include <stdexcept>
#include <limits>
#include "Dictionary/Dictionary.h"
#include "Dictionary/String_validator.h"

/**
 * @brief Выводит количество слов в словаре
 * @param dictionary_ Ссылка на объект словаря
 */
void get_word_number(dictionary& dictionary_) {
    std::cout << "Количество слов в словаре: " << dictionary_.get_size() << "\n";
}

/**
 * @brief Ввод слова с клавиатуры с валидацией
 * @details
 * Функция запрашивает ввод слова, удаляет лишние пробелы и проверяет,
 * что слово не пустое. В случае ошибки выводит сообщение и запрашивает повторный ввод.
 * @return Введенное слово в нижнем регистре
 */
std::string input_word() {
    std::string word_to_input;
    while (true) {
        std::getline(std::cin, word_to_input);

        string_validator::remove_spaces(word_to_input);

        if (!word_to_input.empty()) break;
        std::cout << "Ошибка: слово не может быть пустым.\n Попробуйте снова: ";
    }
    return string_validator::to_lower(word_to_input);
}

/**
 * @brief Ввод английского слова с валидацией
 * @param english_word Строка для сохранения введенного слова
 * @return Валидное английское слово или пустая строка при ошибке
 */
std::string input_english_word(std::string& english_word) {
    std::cout << "Введите английское слово: ";
    english_word = input_word();
    if (!string_validator::valid_english_word(english_word)) {
        std::cout << "Слово введено некорректно.\n";
        return "";
    }
    return english_word;
}

/**
 * @brief Ввод русского слова с валидацией
 * @param russian_word Строка для сохранения введенного слова
 * @return Валидное русское слово или пустая строка при ошибке
 */
std::string input_russian_word(std::string& russian_word) {
    russian_word = input_word();
    if (!string_validator::valid_russian_word(russian_word)) {
        std::cout << "Слово введено некорректно.\n";
        return "";
    }
    return russian_word;
}

/**
 * @brief Добавление новой пары слов в словарь
 * @details
 * Функция запрашивает у пользователя английское слово и его русский перевод,
 * выполняет валидацию введенных данных и добавляет пару в словарь.
 * @param dictionary_ Ссылка на объект словаря
 */
void add_word(dictionary& dictionary_) {
    std::cout << "Введите английское слово: ";
    std::string english_word = input_word();
    if (!string_validator::valid_english_word(english_word)) {
        std::cout << "Слово введено некорректно.\n";
        return;
    }
    std::cout << "Введите перевод: ";
    std::string russian_word = input_word();
    if (!string_validator::valid_russian_word(russian_word)) {
        std::cout << "Слово введено некорректно.\n";
        return;
    }
    try {
        dictionary_ += std::make_pair(english_word, russian_word);
        std::cout << "Слово успешно добавлено.\n";
    } catch (const std::exception& exception) {
        std::cout << "Ошибка при добавлении слова: " << exception.what() << "\n";
    }
}

/**
 * @brief Удаление слова из словаря
 * @param dictionary_ Ссылка на объект словаря
 */
void delete_word(dictionary& dictionary_) {
    if (!dictionary_.is_empty()) {
        std::string english_word;
        if (!input_english_word(english_word).empty()) {
            if (!dictionary_.contains_word(english_word)) {
                std::cout << "Такого слова в словаре нет.\n";
                return;
            }
            dictionary_ -= english_word;
            std::cout << "Пара слов успешно удалена.\n";
        }
    } else std::cout << "Словарь пуст.\n";
}

/**
 * @brief Поиск перевода английского слова
 * @details
 * Функция ищет перевод указанного английского слова в словаре
 * и выводит результат на экран.
 * @param dictionary_ Ссылка на объект словаря
 */
void find_translation(dictionary& dictionary_) {
    if (!dictionary_.is_empty()) {
        std::string english_word;
        if(input_english_word(english_word).empty()) return;
        if (!dictionary_.contains_word(english_word)) {
            std::cout << "Такого слова в словаре нет.\n";
            return;
        }
        if (dictionary_[english_word].empty()){
            std::cout << "Перевод не найден.\n";
            return;
        }
        try {
            std::cout << "Английское слово: " << english_word << "\n" << "Перевод: " << dictionary_[english_word]
                      << "\n";
        } catch (const std::out_of_range &exception) {
            std::cout << "Поймано исключение: " << exception.what() << std::endl;
        }
    } else std::cout << "Словарь пуст.\n";
}

/**
 * @brief Изменение перевода существующего слова
 * @param dictionary_ Ссылка на объект словаря
 */
void change_translation(dictionary& dictionary_) {
    if (!dictionary_.is_empty()) {
        std::string english_word;
        if (input_english_word(english_word).empty()) return;
        if (!dictionary_.contains_word(english_word)) {
            std::cout << "Такого слова в словаре нет.\n";
            return;
        }
        std::string new_russian_word;
        std::cout << "Введите новый перевод: ";
        if(input_russian_word(new_russian_word).empty()) return;
        dictionary_[english_word] = new_russian_word;
        try {
            std::cout << "Английское слово: " << english_word << "\n" << "Новый перевод: " << dictionary_[english_word]
                      << "\n";
        } catch (const std::out_of_range &exception) {
            std::cout << "Поймано исключение: " << exception.what() << std::endl;
        }
    } else std::cout << "Словарь пуст.\n";
}

/**
 * @brief Вывод всего содержимого словаря на экран
 * @param dictionary_ Ссылка на объект словаря
 */
void print_dictionary_helper(dictionary& dictionary_) {
    if (!dictionary_.is_empty()) {
        std::cout << dictionary_;
    } else std::cout << "Словарь пуст.\n";

}

/**
 * @brief Загрузка словаря из файла
 * @details
 * Функция загружает словарь из файла "dictionary.txt" в текущей директории.
 * @param dictionary_ Ссылка на объект словаря
 */
void upload_from_file(dictionary& dictionary_) {
    std::string file_name = "dictionary.txt";
    dictionary_.read_from_file(file_name);
    if (!dictionary_.is_empty()) std::cout << "Словарь загружен из файла.\n";
}

/**
 * @brief Главная функция программы
 * @brief Точка входа в программу
 * @details
 * Функция инициализирует консоль для поддержки UTF-8, создает объект словаря
 * и предоставляет пользовательское меню для взаимодействия со словарем.
 * @return Код завершения программы (0 - успешное завершение)
 * @see dictionary
 */
int main() {

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    dictionary my_dictionary;

    while(true){
        int menu_option;
        std::cout <<  "Меню выбора операции:\n"
                  << "  1.  Добавить слово\n"
                  << "  2.  Удалить слово\n"
                  << "  3.  Найти перевод слова\n"
                  << "  4.  Заменить перевод слова\n"
                  << "  5.  Определить количество слов в словаре\n"
                  << "  6.  Напечатать содержимое словаря\n"
                  << "  7.  Загрузить словарь из файла\n"
                  << "  0.  Выйти\n" << "Ваш выбор: ";
        while (!(std::cin >> menu_option) || menu_option<0 || menu_option>13) {
            std::cout << "Ошибка! Сделайте выбор заново. \n" << "Ваш выбор: ";
            std::cin.clear();
            std::cin.ignore(1000, '\n');
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        switch(menu_option){
            case 1:
                add_word(my_dictionary);
                break;
            case 2:
                delete_word(my_dictionary);
                break;
            case 3:
                find_translation(my_dictionary);
                break;
            case 4:
                change_translation(my_dictionary);
                break;
            case 5:
                get_word_number(my_dictionary);
                break;
            case 6:
                print_dictionary_helper(my_dictionary);
                break;
            case 7:
                upload_from_file(my_dictionary);
                break;
            default:
                return 0;
        }
    }
}