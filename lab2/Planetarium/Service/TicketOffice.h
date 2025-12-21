/**
 * @file TicketOffice.h
 * @author Aleks
 * @brief Класс для управления продажей билетов в планетарий.
 *
 * @details
 * TicketOffice отвечает за расчёт цен, продажу билетов, проверку доступности
 * помещений и формирование финансового отчёта. Использует PriceCalculator
 * для определения стоимости с учётом льгот посетителя.
 */

#ifndef PLANETARIUMPROJECT_TICKETOFFICE_H
#define PLANETARIUMPROJECT_TICKETOFFICE_H

#include <string>
#include <vector>
#include "../Facade/PlanetariumVenue.h"
#include "PriceCalculator.h"
#include "Ticket.h"
#include "../People/Visitor.h"

/**
 * @brief Класс кассы планетария.
 *
 * Управляет списком доступных помещений, проданными билетами и общей выручкой.
 */
class TicketOffice {
private:
    std::vector<PlanetariumVenue*> availableVenues; ///< Список доступных помещений.
    std::vector<Ticket*> soldTickets;               ///< Список проданных билетов.
    double totalRevenue;                            ///< Общая выручка (в рублях).
    PriceCalculator calculator;                     ///< Объект для расчёта скидок.

public:
    /**
     * @brief Конструктор по умолчанию.
     *
     * Инициализирует калькулятор с льготами: бесплатно до 5 лет, скидка до 10 лет.
     */
    TicketOffice();

    /**
     * @brief Конструктор с настраиваемыми возрастными порогами.
     *
     * @param maxFreeAge Максимальный возраст для бесплатного входа.
     * @param maxDiscountAge Максимальный возраст для детской скидки.
     */
    TicketOffice(int maxFreeAge, int maxDiscountAge);

    /**
     * @brief Рассчитывает цену билета для посетителя в указанное помещение.
     *
     * @param venue Указатель на помещение планетария.
     * @param visitor Посетитель (с категорией и возрастом).
     * @return Итоговая цена билета с учётом всех скидок.
     * @see PriceCalculator::calculatePrice
     */
    double getPrice(PlanetariumVenue* venue, const Visitor& visitor);

    /**
     * @brief Продаёт билет на указанное помещение.
     *
     * Проверяет, открыто ли помещение, не превышена ли вместимость,
     * и находится ли текущее время в рабочих часах.
     *
     * @param venue Указатель на помещение.
     * @param visitor Посетитель (передаётся по неконстантной ссылке для совместимости).
     * @param currentTime Текущее время.
     * @return Указатель на новый объект Ticket.
     * @throws VenueClosedException если помещение закрыто.
     * @throws NonWorkingHoursException если время вне рабочих часов.
     * @throws CapacityExceededException если достигнут лимит посетителей.
     * @see checkVenue
     */
    Ticket* sellTicket(PlanetariumVenue* venue, Visitor& visitor, const MyTime& currentTime);

    /**
     * @brief Проверяет, доступно ли помещение для продажи билета в указанное время.
     *
     * @param venue Указатель на помещение.
     * @param currentTime Текущее время.
     * @throws VenueClosedException если помещение закрыто.
     * @throws NonWorkingHoursException если время вне графика работы.
     * @throws CapacityExceededException если невозможно принять ещё одного посетителя.
     */
    static void checkVenue(PlanetariumVenue* venue, const MyTime& currentTime);

    /**
     * @brief Добавляет помещение в список доступных для продажи билетов.
     * @param venue Указатель на помещение планетария.
     */
    void addVenue(PlanetariumVenue* venue);

    /**
     * @brief Формирует краткий финансовый отчёт.
     * @return Строка вида: "Total revenue: 1250.0\nTickets sold: 5".
     */
    std::string printReport() const;
};

#endif // PLANETARIUMPROJECT_TICKETOFFICE_H