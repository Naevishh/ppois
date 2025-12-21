/**
 * @file Observatory.h
 * @author Aleks
 * @brief Класс обсерватории — специализированного помещения для астрономических наблюдений.
 *
 * @details
 * Observatory наследуется от PlanetariumVenue и интегрирует телескоп,
 * купольную конструкцию и проверку погодных условий.
 * Поддерживает наведение и наблюдение астрономических объектов.
 */

#ifndef PLANETARIUMPROJECT_OBSERVATORY_H
#define PLANETARIUMPROJECT_OBSERVATORY_H

#include "PlanetariumVenue.h"
#include "../Inventory/Telescope.h"
#include "../Utils/Date.h"
#include "../Utils/MyTime.h"
#include "../Sky/SkyPosition.h"
#include "../Sky/AstronomicalObject.h"

/**
 * @brief Обсерватория планетария.
 *
 * Предназначена для реальных наблюдений через телескоп при благоприятной погоде.
 */
class Observatory : public PlanetariumVenue {
private:
    Telescope* telescope;           ///< Основной телескоп обсерватории.
    bool isDomeOpen;                ///< Открыт ли купол.
    double domeRotationAngle;       ///< Угол поворота купола (в градусах, соответствует азимуту).

public:
    /**
     * @brief Конструктор обсерватории.
     *
     * @param name_ Название помещения.
     * @param capacity_ Вместимость (количество наблюдателей).
     * @param telescope_ Указатель на телескоп.
     * @note По умолчанию: купол закрыт, угол = 0°.
     */
    Observatory(const std::string& name_, int capacity_, Telescope* telescope_);

    /**
     * @brief Проверяет, подходят ли погодные условия для наблюдений.
     *
     * @param date Дата с ассоциированной погодой.
     * @return true, если погода — SUNNY; иначе false.
     * @note В текущей реализации наблюдения возможны только в солнечную погоду.
     */
    static bool checkWeatherConditions(const Date& date);

    /**
     * @brief Открывает купол обсерватории.
     */
    void openDome();

    /**
     * @brief Устанавливает купол в позицию, соответствующую небесным координатам.
     *
     * @param position Объект SkyPosition с азимутом и высотой.
     * @note Используется только азимут для поворота купола.
     */
    void setDomeToPosition(const SkyPosition& position);

    /**
     * @brief Поворачивает купол на заданный угол.
     * @param angle Угол поворота (в градусах, может быть отрицательным).
     */
    void rotateDome(double angle);

    /**
     * @brief Выполняет наблюдение указанного астрономического объекта.
     *
     * Проверяет:
     * - погоду,
     * - работоспособность телескопа,
     * - видимость объекта в указанное время,
     * - возможность наблюдения (яркость, размер).
     *
     * @param object Объект для наблюдения.
     * @param date Текущая дата (для проверки погоды и ТО).
     * @param time Текущее время (для проверки видимости).
     * @return Строка с подтверждением наблюдения.
     * @throws BadWeather если погода не солнечная.
     * @throws CantUseDevice если телескоп не пригоден к использованию.
     * @throws ObjectIsNotVisible если объект не виден в указанное время.
     * @throws DeviceCapabilityException если объект слишком тусклый или мал.
     */
    std::string observeObject(const AstronomicalObject& object, const Date& date, const MyTime& time);
};

#endif // PLANETARIUMPROJECT_OBSERVATORY_H