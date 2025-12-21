/**
 * @file Stargazing.h
 * @author Aleks
 * @brief Класс мероприятия "Наблюдение звёздного неба" в купольном зале.
 *
 * @details
 * Stargazing наследуется от Activity и представляет программу,
 * сочетающую проекцию астрономических объектов и встроенных шоу в StarHall.
 */

#ifndef PLANETARIUMPROJECT_STARGAZING_H
#define PLANETARIUMPROJECT_STARGAZING_H

#include "Activity.h"
#include "../Facade/StarHall.h"
#include "../Sky/AstronomicalObject.h"
#include "../Utils/Enums.h"
#include <vector>

/**
 * @brief Мероприятие "Звёздное наблюдение" в купольном зале.
 *
 * Позволяет добавлять объекты и опционально встроенные шоу.
 */
class Stargazing : public Activity {
private:
    StarHall* hall;                                  ///< Купольный зал для проекции.
    std::vector<AstronomicalObject*> objectsToWatch; ///< Список объектов для демонстрации.
    bool includeShow;                                ///< Флаг: разрешено ли добавлять шоу.
    std::vector<Enums::BuiltInPlanetariumShow> shows;///< Список включённых шоу.

public:
    /**
     * @brief Конструктор мероприятия.
     *
     * @param name Название мероприятия.
     * @param duration Продолжительность в часах.
     * @param theme Тематика (например, SCIENCE, EDUCATION).
     * @param hall_ Указатель на купольный зал.
     * @note По умолчанию добавление шоу отключено (includeShow = false).
     */
    Stargazing(const std::string& name, double duration, Enums::ActivityTheme theme, StarHall* hall_);

    /**
     * @brief Добавляет встроенный показ, если включена поддержка шоу.
     * @param show Тип шоу (например, SOLAR_SYSTEM_DEMO).
     * @note Шоу игнорируется, если enableShow() не был вызван.
     */
    void addShow(Enums::BuiltInPlanetariumShow show);

    /**
     * @brief Добавляет астрономический объект в программу.
     * @param object Указатель на объект для проекции.
     */
    void addObjectToWatch(AstronomicalObject* object);

    /**
     * @brief Проводит мероприятие: проецирует все объекты и шоу.
     *
     * @param date Дата проведения.
     * @return Строка с подтверждением выполнения.
     * @see StarHall::watchObject, StarHall::watchShow
     */
    std::string hold(const Date& date) override;

    /**
     * @brief Включает возможность добавления встроенных шоу.
     */
    void enableShow();
};

#endif // PLANETARIUMPROJECT_STARGAZING_H