/**
 * @file main.cpp
 * @brief Главный модуль программы для работы с Канторовскими множествами
 * @author Ваше имя
 */

#include <iostream>
#include <string>
#include <windows.h>
#include <limits>
#include "Cantor_set/set.h"
#include "Cantor_set/set_manager.h"
#include <sstream>

/**
 * @brief Получает целочисленный ввод от пользователя
 * @return Введенное пользователем целое число
 * @details Функция обеспечивает валидацию ввода, проверяя, что введены только цифры
 * и что число не равно нулю
 */
int get_integer_input() {
    std::string input;
    while (true) {
        std::cout << "Введите число: ";
        std::getline(std::cin, input);
        if (input.empty()) {
            std::cout << "Ввод не может быть пустым!\n";
            continue;
        }
        if (input.find_first_not_of("0123456789") != std::string::npos) {
            std::cout << "Только цифры!\n";
            continue;
        }
        std::stringstream ss(input);
        int number;
        if (ss >> number && ss.eof() && number!=0) return number;
        std::cout << "Неверный формат числа!\n";
    }
}

/**
 * @brief Проверяет валидность введенной строки
 * @param input_string Строка для проверки
 * @param is_element Флаг, указывающий является ли строка элементом (true) или множеством (false)
 * @return true, если строка валидна, false в противном случае
 */
bool valid_input(std::string& input_string){
    if(input_string.size()==1){
        if (input_string.find_first_not_of("abcdefghijklmnopqrstuvwxyz") != std::string::npos) {
            std::cout << "Только латинские буквы!\n";
            return false;
        }
    }
    return true;
}

/**
 * @brief Получает строковый ввод от пользователя
 * @param is_element Флаг, указывающий запрашивается ли элемент (true) или множество (false)
 * @return Введенная пользователем строка
 */
std::string get_string_input(bool is_element) {
    std::string input_string;
    while (true) {
        is_element ? std::cout << "Введите элемент: " : std::cout << "Введите множество: ";
        std::getline(std::cin, input_string);
        if (input_string.empty()) {
            std::cout << "Строка не может быть пустой!\n";
            continue;
        }
        if (input_string.length() > 100) {
            std::cout << "Строка слишком длинная!\n";
            continue;
        }
        if(!valid_input(input_string)) continue;
        break;
    }
    return input_string;
}

/**
 * @brief Получает номер множества от пользователя с валидацией
 * @param set_manager_ Менеджер множеств для проверки существующих множеств
 * @return Корректный номер множества
 */
size_t input_set_number(set_manager& set_manager_){
    size_t set_number=get_integer_input();
    int all_sets_number=set_manager_.set_manager::get_set_count();
    while (set_number>all_sets_number) {
        std::cout << "Ошибка! Множеств всего " << all_sets_number << ". ";
        set_number=get_integer_input();
    }
    set_number--;
    return set_number;
}

/**
 * @brief Создает новое множество
 * @param set_manager_ Менеджер множеств для создания
 */
void create_new_set(set_manager& set_manager_){
    std::string new_set=get_string_input(false);
    try{
        if (set_manager_.create_set_help(new_set)){
            std::cout << "Множество успешно создано.\n";
        }else{
            std::cout << "Такое множество уже существует.\n";
        }
    } catch (const std::exception &exception) {
        std::cout << "Ошибка при создании множества: " << exception.what() << "\n";
    }
}

/**
 * @brief Удаляет существующее множество
 * @param set_manager_ Менеджер множеств для удаления
 */
void delete_set_(set_manager& set_manager_){
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, которое хотите удалить. ";
    int set_number=get_integer_input();
    if (set_manager_.delete_set_help(set_number)){
        std::cout << "Множество успешно удалено.\n";
    }else{
        std::cout << "Множества с таким номером не существует.\n";
    }
}

/**
 * @brief Выводит элементы указанного множества
 * @param set_manager_ Менеджер множеств для вывода
 */
void print_set_elems(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, элементы которого хотите просмотреть. ";
    size_t set_number = input_set_number(set_manager_);
    std::cout << set_number + 1 << ". " << cantor_set::print_helper(set_manager_.get_set(set_number)) << "\n";
}

/**
 * @brief Выводит все существующие множества
 * @param set_manager_ Менеджер множеств для вывода
 */
void print_all_sets(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Список всех множеств:\n";
    std::vector<std::string> set_list_to_print = set_manager_.list_all_sets();
    for (size_t i = 0; i < set_list_to_print.size(); ++i) {
        std::cout << i + 1 << ". " << set_list_to_print[i] << "\n";
    }
}

/**
 * @brief Добавляет элемент в указанное множество
 * @param set_manager_ Менеджер множеств для добавления
 */
void add_set_element(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, в которое хотите добавить элемент. ";
    size_t set_number = input_set_number(set_manager_);
    std::string input_element = get_string_input(true);
    try{
        if (!set_manager_.get_set(set_number).add_helper(input_element)) {
            std::cout << "Такой элемент уже существует в выбранном множестве.\n";
        } else {
            std::cout << "Элемент успешно добавлен в множество.\n";
        }
    } catch (const std::exception &exception) {
        std::cout << "Ошибка при добавлении элемента: " << exception.what() << "\n";
    }
}

/**
 * @brief Удаляет элемент из указанного множества
 * @param set_manager_ Менеджер множеств для удаления
 */
void delete_set_element(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, из которого хотите удалить элемент. ";
    size_t set_number = input_set_number(set_manager_);
    if (set_manager_.get_set(set_number).is_empty()) {
        std::cout << "Данное множество пустое.\n";
        return;
    }
    std::string input_element = get_string_input(true);
    try {
        if (!set_manager_.get_set(set_number).delete_helper(input_element)) {
            std::cout << "Такого элемента не существует в выбранном множестве.\n";
        } else {
            std::cout << "Элемент успешно удален из множества.\n";
        }
    } catch (const std::exception &exception) {
        std::cout << "Ошибка при удалении элемента: " << exception.what() << "\n";
    }
}

/**
 * @brief Выводит мощность (размер) указанного множества
 * @param set_manager_ Менеджер множеств для проверки
 */
void get_set_size(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, мощность которого хотите узнать. ";
    size_t set_number = input_set_number(set_manager_);
    std::cout << "Мощность множества равна " << set_manager_.get_set(set_number).set_length() << "\n";
}

/**
 * @brief Проверяет является ли множество пустым
 * @param set_manager_ Менеджер множеств для проверки
 */
void is_set_empty(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества для проверки на пустое множество. ";
    size_t set_number = input_set_number(set_manager_);
    if (set_manager_.get_set(set_number).is_empty()) {
        std::cout << "Данное множество пустое.\n";
    } else {
        std::cout << "Данное множество не пустое.\n";
    }
}

/**
 * @brief Проверяет принадлежность элемента множеству
 * @param set_manager_ Менеджер множеств для проверки
 */
void is_element_contained(set_manager& set_manager_) {
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества, которое хотите проверить. ";
    size_t set_number = input_set_number(set_manager_);
    if (set_manager_.get_set(set_number).is_empty()) {
        std::cout << "Данное множество пустое.\n";
        return;
    }
    std::string element_to_find = get_string_input(true);
    try {
        if (set_manager_.get_set(set_number)[element_to_find]) {
            std::cout << "Элемент найден в множестве.\n";
        } else {
            std::cout << "Элемент не найден в множестве.\n";
        }
    } catch (const std::exception &exception) {
        std::cout << "Ошибка при поиске элемента: " << exception.what() << "\n";
    }
}

/**
 * @brief Выполняет операцию объединения двух множеств
 * @param set_manager_ Менеджер множеств для операции
 */
void get_union(set_manager& set_manager_){
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер первого множества для объединения. ";
    size_t set_number_1=input_set_number(set_manager_);
    std::cout << "Укажите номер второго множества для объединения. ";
    size_t set_number_2=input_set_number(set_manager_);
    std::cout << "Объединение множеств: ";
    std::cout << cantor_set::print_helper(set_manager_.union_sets(set_number_1, set_number_2)) << "\n";
}

/**
 * @brief Выполняет операцию пересечения двух множеств
 * @param set_manager_ Менеджер множеств для операции
 */
void get_intersection(set_manager& set_manager_){
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер первого множества для пересечения. ";
    size_t set_number_1=input_set_number(set_manager_);
    std::cout << "Укажите номер второго множества для пересечения. ";
    size_t set_number_2=input_set_number(set_manager_);
    std::cout << "Пересечение множеств: ";
    std::cout << cantor_set::print_helper(set_manager_.intersection_sets(set_number_1, set_number_2)) << "\n";
}

/**
 * @brief Выполняет операцию разности двух множеств
 * @param set_manager_ Менеджер множеств для операции
 */
void get_difference(set_manager& set_manager_){
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер первого множества для разности. ";
    size_t set_number_1=input_set_number(set_manager_);
    std::cout << "Укажите номер второго множества для разности. ";
    size_t set_number_2=input_set_number(set_manager_);
    std::cout << "Разность множеств: ";
    std::cout << cantor_set::print_helper(set_manager_.difference_sets(set_number_1, set_number_2)) << "\n";
}

/**
 * @brief Вычисляет и выводит булеан множества
 * @param set_manager_ Менеджер множеств для операции
 */
void get_boolean(set_manager& set_manager_){
    if (set_manager_.get_set_count() == 0) {
        std::cout << "Не найдено ни одного множества.\n";
        return;
    }
    std::cout << "Укажите номер множества для нахождения булеана. ";
    size_t set_number=input_set_number(set_manager_);
    std::cout << "Булеан множества: ";
    std::cout << cantor_set::print_helper(set_manager_.set_boolean(set_number)) << "\n";
}

/**
 * @brief Главная функция программы
 * @return Код завершения программы
 * @details Основная функция, реализующая интерактивное меню для работы с канторовкими множествами.
 * Предоставляет пользователю интерфейс для выполнения различных операций над множествами.
 */
int main() {

    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    set_manager set_manager_;

    while(true){
        int menu_option;
        std::cout <<  "Меню выбора операции:\n"
                  << "  1.  Создать множество\n"
                  << "  2.  Удалить множество\n"
                  << "  3.  Вывести элементы множества\n"
                  << "  4.  Вывести все множества\n"
                  << "  5.  Добавить элемент в множество\n"
                  << "  6.  Удалить элемент из множества\n"
                  << "  7.  Узнать мощность множества\n"
                  << "  8.  Проверить множество на наличие элементов\n"
                  << "  9.  Проверить принадлежность элемента множеству\n"
                  << "  10.  Операция объединения двух множеств\n"
                  << "  11.  Операция пересечения двух множеств\n"
                  << "  12.  Операция разности двух множеств\n"
                  << "  13.  Построение булеана множества\n"
                  << "  0.  Выйти\n" << "Ваш выбор: ";
        while (!(std::cin >> menu_option) || menu_option<0 || menu_option>13) {
            std::cout << "Ошибка! Сделайте выбор заново. \n" << "Ваш выбор: ";
            std::cin.clear();
            std::cin.ignore(1000, '\n');
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        switch(menu_option){
            case 1:
                create_new_set(set_manager_);
                break;
            case 2:
                delete_set_(set_manager_);
                break;
            case 3:
                print_set_elems(set_manager_);
                break;
            case 4:
                print_all_sets(set_manager_);
                break;
            case 5:
                add_set_element(set_manager_);
                break;
            case 6:
                delete_set_element(set_manager_);
                break;
            case 7:
                get_set_size(set_manager_);
                break;
            case 8:
                is_set_empty(set_manager_);
                break;
            case 9:
                is_element_contained(set_manager_);
                break;
            case 10:
                get_union(set_manager_);
                break;
            case 11:
                get_intersection(set_manager_);
                break;
            case 12:
                get_difference(set_manager_);
                break;
            case 13:
                get_boolean(set_manager_);
                break;
            default:
                return 0;
        }
    }
}
