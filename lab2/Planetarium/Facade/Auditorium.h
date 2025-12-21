/**
 * @file Auditorium.h
 * @author Aleks
 * @brief Класс лекционного зала для проведения презентаций и образовательных мероприятий.
 *
 * @details
 * Auditorium наследуется от PlanetariumVenue и интегрирует проектор,
 * интерактивную доску и посадочные места.
 * Поддерживает два режима: презентация и лекция.
 */

#ifndef PLANETARIUMPROJECT_AUDITORIUM_H
#define PLANETARIUMPROJECT_AUDITORIUM_H

#include "PlanetariumVenue.h"
#include "../Inventory/Seating.h"
#include "../Inventory/Projector.h"
#include "../Inventory/InteractiveWhiteboard.h"
#include "../Events/Lecture.h"
#include "../Utils/Date.h"

/**
 * @brief Лекционный зал планетария.
 *
 * Предназначен для проведения лекций с использованием проектора и/или интерактивной доски.
 */
class Auditorium : public PlanetariumVenue {
private:
    Seating* seats;                     ///< Система посадочных мест.
    Projector* projector;               ///< Проектор для презентаций.
    InteractiveWhiteboard* board;       ///< Интерактивная доска.

public:
    /**
     * @brief Конструктор лекционного зала.
     *
     * @param name Название зала.
     * @param capacity Вместимость.
     * @param seats_ Указатель на посадочные места.
     * @param projector_ Указатель на проектор.
     * @param board_ Указатель на интерактивную доску.
     */
    Auditorium(const std::string& name, int capacity, Seating* seats_, Projector* projector_,
               InteractiveWhiteboard* board_);

    /**
     * @brief Настраивает зал для режима презентации.
     *
     * Производит проекцию на доску и переводит доску в режим проекции.
     *
     * @param date Текущая дата для проверки работоспособности устройств.
     * @throws CantUseDevice если проектор или доска не пригодны к использованию.
     * @see Projector::project, InteractiveWhiteboard::readyForProjection
     */
    void setupForPresentation(const Date& date);

    /**
     * @brief Настраивает зал для лекции.
     *
     * Зависит от потребности в проекторе:
     * - если нужен — настраивает как презентацию,
     * - иначе — переводит доску в режим лекции.
     *
     * @param date Текущая дата.
     * @param projectorNeeded Флаг: требуется ли проектор для лекции.
     * @throws CantUseDevice если нужное оборудование неисправно.
     * @see setupForPresentation, InteractiveWhiteboard::readyForLecture
     */
    void setupForLecture(const Date& date, bool projectorNeeded);

    /**
     * @brief Проводит лекцию в зале.
     *
     * @param date Текущая дата.
     * @param lecture Указатель на объект лекции.
     * @return Строка с описанием темы лекции или ошибкой.
     * @see setupForLecture
     */
    std::string holdLecture(const Date& date, Lecture* lecture);
};

#endif // PLANETARIUMPROJECT_AUDITORIUM_H