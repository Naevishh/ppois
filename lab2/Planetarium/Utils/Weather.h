/**
 * @file Weather.h
 * @author Ященко Александра
 * @brief Класс для представления и генерации погодных условий.
 *
 * @details
 * Класс Weather инкапсулирует состояние погоды, представленное перечислением
 * WeatherCondition из Enums.h. Поддерживает создание фиксированной погоды
 * или случайной (на основе rand()). Используется в связке с классом Date.
 */

#ifndef PLANETARIUMPROJECT_WEATHER_H
#define PLANETARIUMPROJECT_WEATHER_H

#include <vector>
#include <cstdlib>
#include "Enums.h"

using wCondition = Enums::WeatherCondition;

/**
 * @brief Класс, представляющий погодные условия.
 *
 * Может быть инициализирован явно или случайно. Содержит методы доступа
 * и преобразования по индексу.
 */
class Weather {
private:
    /**
     * @brief Генерирует случайное погодное условие.
     * @return Случайный элемент из фиксированного списка WeatherCondition.
     */
    wCondition getRandomWeather();

    Enums::WeatherCondition weather; ///< Текущее погодное условие.

public:
    /**
     * @brief Конструктор по умолчанию.
     *
     * Инициализирует погоду случайным значением.
     */
    explicit Weather();

    /**
     * @brief Получает погодное условие по индексу.
     *
     * @param index Индекс (0–8). При выходе за пределы возвращает SUNNY.
     * @return Соответствующий WeatherCondition.
     */
    static wCondition getWeatherByIndex(size_t index);

    /**
     * @brief Конструктор с указанием конкретного условия.
     * @param condition Желаемое погодное условие.
     */
    Weather(const wCondition& condition);

    /**
     * @brief Возвращает текущее погодное условие.
     * @return Значение перечисления WeatherCondition.
     */
    wCondition getWeatherCondition() const;
};

#endif // PLANETARIUMPROJECT_WEATHER_H