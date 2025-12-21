/**
 * @file PlanetariumFacade.h
 * @author Aleks
 * @brief Фасад для упрощённого взаимодействия с планетарием.
 *
 * @details
 * PlanetariumFacade предоставляет единый интерфейс для:
 * - продажи билетов,
 * - управления помещениями,
 * - открытия залов.
 * Скрывает сложность внутренней архитектуры (TicketOffice, Venue и т.д.).
 */

#ifndef PLANETARIUMPROJECT_PLANETARIUMFACADE_H
#define PLANETARIUMPROJECT_PLANETARIUMFACADE_H

#include <string>
#include <vector>
#include "StarHall.h"
#include "../Service/TicketOffice.h"
#include "../People/Visitor.h"
#include "../Utils/MyTime.h"

/**
 * @brief Фасад планетария — единая точка входа для клиентского кода.
 */
class PlanetariumFacade {
private:
    TicketOffice ticketOffice;            ///< Касса для продажи билетов.
    std::vector<PlanetariumVenue> venues; ///< Список помещений (включая StarHall).

public:
    /**
     * @brief Конструктор с автоматическим созданием StarHall.
     *
     * @param projector Купольный проектор.
     * @param system Аудиосистема.
     * @param seats Посадочные места.
     * @param screen Купольный экран.
     * @note Создаёт один StarHall с именем "StarHall" и вместимостью 100.
     */
    PlanetariumFacade(PlanetariumProjector* projector, AudioSystem* system, Seating* seats,
                      DomeShapedScreen* screen);

    /**
     * @brief Продаёт билет посетителю на указанное помещение.
     *
     * @param venueName Название помещения.
     * @param visitor Посетитель.
     * @param curTime Текущее время (для проверки рабочих часов).
     * @return Указатель на билет, или nullptr, если помещение не найдено.
     * @throws std::invalid_argument если название помещения недопустимо.
     * @see TicketOffice::sellTicket
     */
    Ticket* sellTicketToVisitor(const std::string& venueName, Visitor& visitor, const MyTime curTime);

    /**
     * @brief Добавляет новое помещение в список доступных.
     *
     * @param venue Указатель на помещение.
     * @note Помещение копируется в вектор (хранится по значению).
     * @see TicketOffice::addVenue
     */
    void addVenue(PlanetariumVenue* venue);

    /**
     * @brief Открывает помещение по его названию.
     *
     * @param venueName Название помещения.
     * @note Если помещение не найдено — ничего не происходит.
     */
    void openFacadeVenue(const std::string& venueName);

    /**
     * @brief Находит помещение по названию.
     *
     * @param venueName Название помещения.
     * @return Указатель на PlanetariumVenue, или nullptr, если не найдено.
     * @throws std::invalid_argument если название недопустимо.
     */
    PlanetariumVenue* findVenueByName(const std::string& venueName);
};

#endif // PLANETARIUMPROJECT_PLANETARIUMFACADE_H