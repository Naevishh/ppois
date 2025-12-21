/**
 * @file StarHall.h
 * @author Aleks
 * @brief Специализированное помещение планетария для купольных проекций.
 *
 * @details
 * StarHall наследуется от PlanetariumVenue и интегрирует купольный проектор,
 * купольный экран, аудиосистему и посадочные места.
 * Поддерживает проекцию астрономических объектов и встроенных шоу.
 */

#ifndef PLANETARIUMPROJECT_STARHALL_H
#define PLANETARIUMPROJECT_STARHALL_H

#include "PlanetariumVenue.h"
#include "../Inventory/PlanetariumProjector.h"
#include "../Inventory/AudioSystem.h"
#include "../Inventory/Seating.h"
#include "../Inventory/DomeShapedScreen.h"
#include "../Sky/AstronomicalObject.h"
#include "../Utils/Date.h"

/**
 * @brief Купольный зал планетария (Star Hall).
 *
 * Предназначен для иммерсивных астрономических демонстраций.
 */
class StarHall : public PlanetariumVenue {
private:
    PlanetariumProjector* domeProjector; ///< Купольный проектор.
    AudioSystem* surroundSound;          ///< Система объёмного звука.
    Seating* seats;                      ///< Система посадочных мест.
    DomeShapedScreen* domeScreen;        ///< Купольный экран.

public:
    /**
     * @brief Конструктор зала.
     *
     * @param name Название помещения.
     * @param capacity Вместимость зала (количество мест).
     * @param projector Указатель на купольный проектор.
     * @param sound Указатель на аудиосистему.
     * @param hallSeats Указатель на посадочные места.
     * @param screen Указатель на купольный экран.
     */
    StarHall(const std::string& name, int capacity,
             PlanetariumProjector* projector, AudioSystem* sound,
             Seating* hallSeats, DomeShapedScreen* screen);

    /**
     * @brief Подготавливает зал к проекции.
     *
     * Проверяет работоспособность проектора и экрана на указанную дату,
     * запускает проекцию и настраивает звук.
     *
     * @param date Текущая дата для проверки гарантии и ТО.
     * @throws CantUseDevice если проектор или экран не пригодны к использованию.
     * @see PlanetariumProjector::project, AudioSystem::setUpSystem
     */
    void setupForProjection(const Date& date);

    /**
     * @brief Производит проекцию указанного астрономического объекта.
     *
     * @param date Текущая дата.
     * @param objectToWatch Указатель на объект для проекции.
     * @return Строка с результатом: успех или сообщение об ошибке.
     * @see setupForProjection, PlanetariumProjector::projectObject
     */
    std::string watchObject(const Date& date, AstronomicalObject* objectToWatch);

    /**
     * @brief Запускает встроенное демонстрационное шоу.
     *
     * @param date Текущая дата.
     * @param showToWatch Тип шоу (например, SOLAR_SYSTEM_DEMO).
     * @return Строка с результатом: успех или сообщение об ошибке.
     * @see setupForProjection, PlanetariumProjector::projectShow
     */
    std::string watchShow(const Date& date, const Enums::BuiltInPlanetariumShow& showToWatch);

    /**
     * @brief Возвращает указатель на купольный проектор.
     * @return Указатель на PlanetariumProjector.
     */
    PlanetariumProjector* getProjector() const;

    /**
     * @brief Возвращает указатель на купольный экран.
     * @return Указатель на DomeShapedScreen.
     */
    DomeShapedScreen* getScreen() const;
};

#endif // PLANETARIUMPROJECT_STARHALL_H