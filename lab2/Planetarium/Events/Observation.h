/**
 * @file Observation.h
 * @author Aleks
 * @brief Класс мероприятия "Астрономические наблюдения" через телескоп.
 *
 * @details
 * Observation наследуется от Activity и представляет реальные наблюдения
 * через телескоп в обсерватории в заданное время суток.
 */

#ifndef PLANETARIUMPROJECT_OBSERVATION_H
#define PLANETARIUMPROJECT_OBSERVATION_H

#include "Activity.h"
#include "../Facade/Observatory.h"
#include "../Sky/AstronomicalObject.h"
#include "../Utils/MyTime.h"
#include <vector>

/**
 * @brief Мероприятие "Наблюдение через телескоп".
 *
 * Требует конкретного времени суток и благоприятной погоды.
 */
class Observation : public Activity {
private:
    Observatory* observatory;                     ///< Обсерватория с телескопом.
    std::vector<AstronomicalObject*> objectsToObserve; ///< Объекты для наблюдения.
    MyTime observationTime;                       ///< Время наблюдения (фиксированное для всего мероприятия).

public:
    /**
     * @brief Конструктор мероприятия.
     *
     * @param name Название мероприятия.
     * @param duration Продолжительность в часах.
     * @param theme Тематика (например, SCIENCE).
     * @param observatory_ Указатель на обсерваторию.
     * @param time Время наблюдения (часы:минуты:секунды).
     */
    Observation(const std::string& name, double duration, Enums::ActivityTheme theme, Observatory* observatory_,
                const MyTime& time);

    /**
     * @brief Добавляет астрономический объект в список наблюдений.
     * @param object Указатель на объект.
     */
    void addObject(AstronomicalObject* object);

    /**
     * @brief Выполняет наблюдения всех объектов через телескоп.
     *
     * @param date Дата проведения (для проверки погоды и ТО оборудования).
     * @return Строка с подтверждением выполнения.
     * @throws PlanetariumException при плохой погоде, невидимости объекта и т.д.
     * @see Observatory::observeObject
     */
    std::string hold(const Date& date) override;
};

#endif // PLANETARIUMPROJECT_OBSERVATION_H