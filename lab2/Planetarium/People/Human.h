/**
 * @file Human.h
 * @author Aleks
 * @brief Базовый класс для всех людей в системе (посетители, сотрудники).
 *
 * @details
 * Содержит общие атрибуты: имя и возраст. Является родительским для Visitor и Employee.
 */

#ifndef PLANETARIUMPROJECT_HUMAN_H
#define PLANETARIUMPROJECT_HUMAN_H

#include <string>

/**
 * @brief Абстрактный базовый класс для представления человека.
 *
 * Хранит только имя и возраст. Используется как основа для Visitor и Employee.
 */
class Human {
private:
    std::string name; ///< Полное имя человека.
    int age;          ///< Возраст в годах (≥ 0).

public:
    /**
     * @brief Конструктор человека.
     *
     * @param name_ Имя (перемещается во внутреннее поле).
     * @param age_ Возраст в годах.
     */
    Human(std::string name_, int age_);

    /**
     * @brief Возвращает имя человека.
     * @return Строка с именем.
     */
    std::string getName() const;

    /**
     * @brief Возвращает возраст человека.
     * @return Возраст в годах.
     */
    int getAge() const;
};

#endif // PLANETARIUMPROJECT_HUMAN_H