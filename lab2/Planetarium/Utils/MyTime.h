/**
 * @file MyTime.h
 * @author Aleks
 * @brief Класс для представления и сравнения времени (часы:минуты:секунды).
 *
 * @details
 * MyTime хранит время в виде трёх целых чисел. Поддерживает валидацию
 * через TimeValidator, строковое представление и операторы сравнения.
 * Может быть создан из системного времени.
 */

#ifndef PLANETARIUMPROJECT_TIME_H
#define PLANETARIUMPROJECT_TIME_H

#include <string>

/**
 * @brief Класс для работы с временем (без даты).
 *
 * Представляет время с точностью до секунды. Поддерживает сравнение,
 * строковое представление и получение текущего системного времени.
 */
class MyTime {
private:
    int seconds; ///< Секунды (0–59).
    int minutes; ///< Минуты (0–59).
    int hours;   ///< Часы (0–23).

public:
    /**
     * @brief Конструктор по умолчанию.
     *
     * Инициализирует объект текущим системным временем.
     */
    MyTime();

    /**
     * @brief Конструктор с заданным временем.
     *
     * @param hours_ Часы (0–23).
     * @param minutes_ Минуты (0–59).
     * @param seconds_ Секунды (0–59).
     * @throws std::invalid_argument если время некорректно.
     * @see TimeValidator::isValidTime
     */
    MyTime(int hours_, int minutes_, int seconds_);

    /**
     * @brief Возвращает строковое представление времени в формате ЧЧ:ММ:СС.
     * @return Строка вида "14:05:09".
     */
    std::string getTime() const;

    /**
     * @brief Преобразует число в двузначную строку (с ведущим нулём при необходимости).
     * @param int_ Целое число (обычно 0–59 или 0–23).
     * @return Строка: "05", "23" и т.д.
     */
    static std::string toString(int int_);

    /**
     * @brief Перегрузка оператора сравнения времени.
     * @param time Другое время для сравнения.
     * @return true, если левый объект равен правому, иначе false.
     */
    bool operator==(const MyTime& time) const;

    /**
     * @brief Перегрузка оператора сравнения времени.
     * @param time Другое время для сравнения.
     * @return true, если левый объект меньше правого, иначе false.
     */
    bool operator<(const MyTime& time) const;

    /**
     * @brief Перегрузка оператора сравнения времени.
     * @param time Другое время для сравнения.
     * @return true, если левый объект больше правого, иначе false.
     */
    bool operator>(const MyTime& time) const;

    /**
     * @brief Перегрузка оператора сравнения времени.
     * @param time Другое время для сравнения.
     * @return true, если левый объект меньше либо равен правому, иначе false.
     */
    bool operator<=(const MyTime& time) const;

    /**
     * @brief Перегрузка оператора сравнения времени.
     * @param time Другое время для сравнения.
     * @return true, если левый объект больше либо равен правому, иначе false.
     */
    bool operator>=(const MyTime& time) const;

    /**
     * @brief Создаёт объект с текущим системным временем.
     * @return MyTime, инициализированный текущим временем.
     */
    static MyTime getCurrentTime();

    /**
     * @brief Возвращает секунды.
     * @return Значение от 0 до 59.
     */
    int getSeconds() const;

    /**
     * @brief Возвращает минуты.
     * @return Значение от 0 до 59.
     */
    int getMinutes() const;

    /**
     * @brief Возвращает часы.
     * @return Значение от 0 до 23.
     */
    int getHours() const;
};

#endif // PLANETARIUMPROJECT_TIME_H