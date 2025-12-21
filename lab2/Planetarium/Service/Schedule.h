/**
 * @file Schedule.h
 * @author Aleks
 * @brief Класс для представления графика работы помещения.
 *
 * @details
 * Schedule хранит время открытия, закрытия и обеденного перерыва.
 * Используется PlanetariumVenue для проверки рабочих часов.
 */

#ifndef PLANETARIUMPROJECT_SCHEDULE_H
#define PLANETARIUMPROJECT_SCHEDULE_H

#include "../Utils/MyTime.h"

/**
 * @brief График работы (расписание).
 *
 * Задаёт временные рамки работы и обеда.
 */
class Schedule {
private:
    MyTime openingTime;   ///< Время открытия.
    MyTime closingTime;   ///< Время закрытия.
    MyTime lunchStart;    ///< Начало обеда.
    MyTime lunchEnd;      ///< Конец обеда.

public:
    /**
     * @brief Конструктор с параметрами.
     *
     * @param openingHour Час открытия (0–23).
     * @param openingMinutes Минуты открытия (0–59).
     * @param workdayDuration Продолжительность рабочего дня (в часах).
     * @param lunchStartHour Час начала обеда.
     * @param lunchStartMinutes Минуты начала обеда.
     * @param lunchDuration Длительность обеда (в минутах).
     */
    Schedule(int openingHour, int openingMinutes, int workdayDuration, int lunchStartHour,
             int lunchStartMinutes, int lunchDuration);

    /**
     * @brief Конструктор по умолчанию.
     *
     * Устанавливает: 08:00–20:00, обед 12:00–13:00.
     */
    Schedule();

    /**
     * @brief Возвращает время открытия.
     * @return Объект MyTime.
     */
    MyTime getOpeningTime() const;

    /**
     * @brief Возвращает время закрытия.
     * @return Объект MyTime.
     */
    MyTime getClosingTime() const;

    /**
     * @brief Возвращает начало обеденного перерыва.
     * @return Объект MyTime.
     */
    MyTime getLunchStart() const;

    /**
     * @brief Возвращает конец обеденного перерыва.
     * @return Объект MyTime.
     */
    MyTime getLunchEnd() const;
};

#endif // PLANETARIUMPROJECT_SCHEDULE_H