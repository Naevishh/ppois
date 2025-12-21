/**
 * @file set_manager.h
 * @brief Заголовочный файл класса set_manager для управления списком множеств
 * @author Ваше имя
 */

#ifndef SEM3_L1_PPOIS_P2_SET_MANAGER_H
#define SEM3_L1_PPOIS_P2_SET_MANAGER_H

#include "set.h"
#include <vector>

/**
 * @brief Класс для управления списком множеств
 * 
 * @details Класс set_manager предоставляет функционал для работы со списком множеств.
 * Позволяет создавать, удалять, искать множества, выполнять операции над множествами
 * и получать информацию о хранимых множествах.
 */
class set_manager {
private:
    std::vector<cantor_set> set_list; ///< Вектор для хранения множеств

    /**
     * @brief Создает новое множество из строки
     * @param elements Строка с элементами множества
     * @return true, если множество создано, false, если такое множество уже существует
     */
    bool create_set(const std::string&);

    /**
     * @brief Удаляет множество по индексу
     * @param set_index Индекс множества для удаления
     * @return true, если множество удалено, false, если индекс некорректен
     */
    bool delete_set(size_t);

    /**
     * @brief Находит множество по его строковому представлению
     * @param elements Строковое представление множества
     * @return Индекс множества или -1, если не найдено
     */
    size_t find_set(const std::string&);

public:
    /**
     * @brief Публичный метод для создания множества
     * @param elements Строка с элементами множества
     * @return true, если множество создано, false, если такое множество уже существует
     * @see create_set()
     */
    bool create_set_help(std::string&);

    /**
     * @brief Публичный метод для удаления множества
     * @param set_number Номер множества для удаления (начиная с 1)
     * @return true, если множество удалено, false, если номер некорректен
     * @see delete_set()
     */
    bool delete_set_help(size_t);

    /**
     * @brief Получает множество по индексу
     * @param index Индекс множества
     * @return Ссылка на множество по указанному индексу
     */
    cantor_set& get_set(size_t index);

    /**
     * @brief Возвращает количество множеств в коллекции
     * @return Количество множеств
     */
    size_t get_set_count() const;

    /**
     * @brief Возвращает список всех множеств в строковом представлении
     * @return Вектор строковых представлений множеств
     */
    std::vector<std::string> list_all_sets() const;

    /**
     * @brief Выполняет операцию объединения двух множеств
     * @param index_1 Индекс первого множества
     * @param index_2 Индекс второго множества
     * @return Новое множество - результат объединения
     */
    cantor_set union_sets(size_t index_1, size_t index_2);

    /**
     * @brief Выполняет операцию пересечения двух множеств
     * @param index_1 Индекс первого множества
     * @param index_2 Индекс второго множества
     * @return Новое множество - результат пересечения
     */
    cantor_set intersection_sets(size_t index_1, size_t index_2);

    /**
     * @brief Выполняет операцию разности двух множеств
     * @param index_1 Индекс первого множества (уменьшаемое)
     * @param index_2 Индекс второго множества (вычитаемое)
     * @return Новое множество - результат разности
     */
    cantor_set difference_sets(size_t index_1, size_t index_2);

    /**
     * @brief Строит булеан множества (множество всех подмножеств)
     * @param set_index Индекс множества для построения булеана
     * @return Булеан указанного множества
     */
    cantor_set set_boolean(size_t set_index);
};

#endif //SEM3_L1_PPOIS_P2_SET_MANAGER_H
