/**
 * @file set.h
 * @brief Заголовочный файл класса cantor_set для работы с канторовкими множествами
 * @author Ященко Александра
 */

#ifndef SEM3_L1_PPOIS_P2_SET_H
#define SEM3_L1_PPOIS_P2_SET_H

#include <iostream>
#include <string>
#include <vector>
#include <variant>

/**
 * @brief Класс для работы с канторовкими множествами
 * 
 * @details Класс реализует функционал для работы с канторовкими множествами,
 * включая ориентированные и неориентированные множества, операции над множествами
 * и вложенные структуры. Поддерживает элементы типа char и вложенные множества.
 */
class cantor_set{
private:
    using element = std::variant<char, cantor_set>; ///< Тип элемента множества
    using vec_element=std::vector<std::variant<char, cantor_set>>; ///< Тип контейнера для элементов
    vec_element set_elements; ///< Вектор элементов множества
    bool is_directed; ///< Флаг ориентированности множества

    /**
     * @brief Инициализирует элементы множества из строки
     * @param elements_string Строка с элементами множества
     * @param start_brace Начальная скобка '{' или '<'
     * @param position Позиция в строке для парсинга
     * @return Инициализированное множество
     */
    cantor_set initialize_set_elems(const std::string&,const char& ,size_t&);

    /**
     * @brief Сравнивает два элемента множества
     * @param first_elem Первый элемент для сравнения
     * @param second_elem Второй элемент для сравнения
     * @return true, если элементы равны, иначе false
     */
    bool compare_elems(const element&, const element &) const;

    /**
     * @brief Сравнивает два множества
     * @param first_set Первое множество для сравнения
     * @param second_set Второе множество для сравнения
     * @return true, если множества равны, иначе false
     */
    bool compare_sets(const cantor_set &, const cantor_set &) const;

    /**
     * @brief Находит элемент в множестве по строке
     * @param cantor_set_ Множество для поиска
     * @param input_string Строка с элементом для поиска
     * @return Индекс элемента или -1, если не найден
     */
    int find_element(const cantor_set &, const std::string &);

    /**
     * @brief Находит элемент в текущем множестве по строке
     * @param input_string Строка с элементом для поиска
     * @return Индекс элемента или -1, если не найден
     */
    int find_element(const std::string &);

    /**
     * @brief Находит элемент в текущем множестве
     * @param elem_to_find Элемент для поиска
     * @return Индекс элемента или -1, если не найден
     */
    int find_element(const element &);

    /**
     * @brief Находит элемент в указанном множестве
     * @param cantor_set_ Множество для поиска
     * @param elem_to_find Элемент для поиска
     * @return Индекс элемента или -1, если не найден
     */
    int find_element(const cantor_set &, const element &);

    /**
     * @brief Добавляет элемент в множество
     * @param elem_to_add Элемент для добавления
     * @return true, если элемент добавлен, false, если уже существует
     */
    bool add_element(const element &);

    /**
     * @brief Удаляет элемент из множества
     * @param elem_to_delete Элемент для удаления
     * @return true, если элемент удален, false, если не найден
     */
    bool delete_element(const element &);

public:
    /**
     * @brief Конструктор с символом-скобкой
     * @param start_brace Символ '{' или '<' для определения типа множества
     */
    explicit cantor_set(char);

    /**
     * @brief Конструктор со строкой элементов
     * @param elements_string Строка с элементами множества
     */
    explicit cantor_set(const std::string&);

    /**
     * @brief Конструктор с C-строкой элементов
     * @param elements_string C-строка с элементами множества
     */
    explicit cantor_set(const char*);

    /**
     * @brief Конструктор копирования
     * @param other_set Множество для копирования
     */
    cantor_set(const cantor_set &);

    /**
     * @brief Оператор присваивания
     * @param other_set Множество для присваивания
     * @return Ссылка на текущий объект
     */
    cantor_set& operator=(const cantor_set &);

    /**
     * @brief Инициализатор элемента из строки
     * @param input_string Строка для инициализации элемента
     * @return Инициализированный элемент
     */
    element element_initializer(const std::string &);

    /**
     * @brief Вспомогательный метод для добавления элемента по строке
     * @param string_to_add Строка с элементом для добавления
     * @return true, если элемент добавлен, false, если уже существует
     */
    bool add_helper(std::string&);

    /**
     * @brief Вспомогательный метод для удаления элемента по строке
     * @param string_to_delete Строка с элементом для удаления
     * @return true, если элемент удален, false, если не найден
     */
    bool delete_helper(std::string&);

    /**
     * @brief Проверяет пустое ли множество
     * @return true, если множество пустое, иначе false
     */
    bool is_empty();

    /**
     * @brief Проверяет является ли множество ориентированным
     * @return true, если множество ориентированное, иначе false
     */
    bool is_directed_set() const;

    /**
     * @brief Возвращает количество элементов в множестве
     * @return Количество элементов
     */
    size_t set_length();

    /**
     * @brief Оператор сравнения равенства множеств
     * @param other_set Множество для сравнения
     * @return true, если множества равны, иначе false
     */
    bool operator==(const cantor_set &) const;

    /**
     * @brief Оператор сравнения неравенства множеств
     * @param other_set Множество для сравнения
     * @return true, если множества не равны, иначе false
     */
    bool operator!=(const cantor_set &) const;

    /**
     * @brief Формирует строковое представление элемента множества
     * @param elem_to_print Элемент для печати
     * @param printed_set Строка для накопления результата
     * @return Строковое представление элемента
     */
    std::string print_set(const element &, std::string&) const;

    /**
     * @brief Вспомогательный метод для печати множества
     * @param set_to_print Множество для печати
     * @return Строковое представление множества
     */
    static std::string print_helper(const cantor_set &);

    /**
     * @brief Оператор проверки принадлежности элемента множеству
     * @param input_string Строка с элементом для проверки
     * @return true, если элемент принадлежит множеству, иначе false
     */
    bool operator[](std::string &);

    /**
     * @brief Оператор объединения с присваиванием
     * @param other_set Множество для объединения
     * @return Ссылка на текущее множество после объединения
     */
    cantor_set& operator+=(cantor_set&);

    /**
     * @brief Оператор объединения множеств
     * @param other_set Множество для объединения
     * @return Новое множество - результат объединения
     */
    cantor_set operator+(cantor_set&);

    /**
     * @brief Оператор пересечения с присваиванием
     * @param other_set Множество для пересечения
     * @return Ссылка на текущее множество после пересечения
     */
    cantor_set& operator*=(cantor_set&);

    /**
     * @brief Оператор пересечения множеств
     * @param other_set Множество для пересечения
     * @return Новое множество - результат пересечения
     */
    cantor_set operator*(cantor_set&);

    /**
     * @brief Оператор разности с присваиванием
     * @param other_set Множество для вычитания
     * @return Ссылка на текущее множество после вычитания
     */
    cantor_set& operator-=(cantor_set&);

    /**
     * @brief Оператор разности множеств
     * @param other_set Множество для вычитания
     * @return Новое множество - результат вычитания
     */
    cantor_set operator-(cantor_set&);

    /**
     * @brief Вычисляет булеан множества (множество всех подмножеств)
     * @param other_set Множество для вычисления булеана
     * @return Булеан множества
     */
    cantor_set set_boolean(cantor_set&);

};

/**
 * @brief Оператор вывода множества в поток
 * @param output Поток вывода
 * @param set_to_print Множество для вывода
 * @return Поток вывода
 */
std::ostream& operator<<(std::ostream&, const cantor_set &);

/**
 * @brief Оператор ввода множества из потока
 * @param input Поток ввода
 * @param set_to_input Множество для ввода
 * @return Поток ввода
 */
std::istream& operator>>(std::istream&, cantor_set &);

#endif //SEM3_L1_PPOIS_P2_SET_H
