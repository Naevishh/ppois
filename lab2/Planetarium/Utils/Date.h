/**
 * @file Date.h
 * @author Aleks
 * @brief Класс для представления даты с привязанной погодой.
 *
 * @details
 * Date хранит день, месяц и год, а также ассоциированное погодное условие.
 * Поддерживает валидацию через TimeValidator, сравнение, прибавление лет
 * и получение текущей даты.
 */

#ifndef PLANETARIUMPROJECT_DATE_H
#define PLANETARIUMPROJECT_DATE_H

#include <string>
#include "Weather.h"

/**
 * @brief Класс для работы с календарной датой.
 *
 * Содержит информацию о дне, месяце, годе и связанной погоде.
 * Поддерживает операции сравнения и арифметики (прибавление лет).
 */
class Date {
private:
    int day;     ///< День месяца (1–31).
    int month;   ///< Месяц (1–12).
    int year;    ///< Год (например, 2025).
    Weather weather_; ///< Погодное условие на эту дату.

public:
    /**
     * @brief Конструктор с заданной датой.
     *
     * @param year_ Год.
     * @param month_ Месяц (1–12).
     * @param day_ День месяца.
     * @throws std::invalid_argument если дата некорректна.
     * @see TimeValidator::isValidDate
     */
    Date(int year_, int month_, int day_);

    /**
     * @brief Возвращает строковое представление даты в формате ДД.ММ.ГГГГ.
     * @return Строка вида "21.12.2025".
     */
    std::string getDate() const;

    /**
     * @brief Преобразует число в двузначную строку (с ведущим нулём при необходимости).
     * @param int_ Целое число (обычно 1–31 или 1–12).
     * @return Строка: "05", "12" и т.д.
     */
    static std::string toString(int int_);

    /**
     * @brief Возвращает погодное условие, связанное с датой.
     * @return Значение перечисления WeatherCondition.
     */
    Enums::WeatherCondition getWeather() const;

        /**
     * @brief Перегрузка оператора сравнения дат.
     * @param date Другая дата для сравнения.
     * @return true, если левый объект равен правому (совпадают день, месяц и год); иначе false.
     */
    bool operator==(const Date& date) const;

    /**
     * @brief Перегрузка оператора «меньше» для дат.
     * @param date Другая дата для сравнения.
     * @return true, если левая дата предшествует правой; иначе false.
     */
    bool operator<(const Date& date) const;

    /**
     * @brief Перегрузка оператора «больше» для дат.
     * @param date Другая дата для сравнения.
     * @return true, если левая дата следует после правой; иначе false.
     */
    bool operator>(const Date& date) const;

    /**
     * @brief Прибавляет указанное количество лет к дате.
     * @param years Количество лет (может быть отрицательным).
     * @return Новый объект Date с обновлённым годом.
     */
    Date operator+(int years) const;

    /**
     * @brief Создаёт объект с текущей системной датой.
     * @return Date, инициализированный сегодняшней датой.
     */
    static Date currentDate();

    /**
     * @brief Устанавливает год.
     * @param year_ Новое значение года.
     */
    void setYear(int year_);

    /**
     * @brief Устанавливает месяц.
     * @param month_ Новое значение месяца.
     */
    void setMonth(int month_);

    /**
     * @brief Устанавливает день.
     * @param day_ Новое значение дня.
     */
    void setDay(int day_);

    /**
     * @brief Устанавливает погоду для даты.
     * @param weather Новый объект Weather.
     */
    void setWeather(const Weather& weather);
};

#endif // PLANETARIUMPROJECT_DATE_H