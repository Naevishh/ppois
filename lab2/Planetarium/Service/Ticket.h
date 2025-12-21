/**
 * @file Ticket.h
 * @author Aleks
 * @brief Класс, представляющий билет на посещение помещения планетария.
 *
 * @details
 * Ticket хранит информацию о посетителе, помещении, цене и времени покупки.
 * Создаётся при успешной продаже через TicketOffice.
 */

#ifndef PLANETARIUMPROJECT_TICKET_H
#define PLANETARIUMPROJECT_TICKET_H

#include <string>
#include "../Facade/PlanetariumVenue.h"
#include "../Utils/MyTime.h"

class PlanetariumVenue;

/**
 * @brief Класс билета.
 *
 * Является результатом успешной транзакции в TicketOffice.
 */
class Ticket {
private:
    PlanetariumVenue* venue;       ///< Помещение, на которое выписан билет.
    std::string visitorName;       ///< Имя посетителя.
    MyTime purchaseTime;           ///< Время покупки (инициализируется текущим временем).
    double finalPrice;             ///< Итоговая цена с учётом скидок.

public:
    /**
     * @brief Конструктор билета.
     *
     * @param venue_ Указатель на помещение (не может быть nullptr).
     * @param visitor Имя посетителя.
     * @param finalPrice_ Итоговая цена билета.
     * @throws std::invalid_argument если venue_ равен nullptr.
     */
    Ticket(PlanetariumVenue* venue_, std::string visitor, double finalPrice_);

    /**
     * @brief Возвращает краткую информацию о билете.
     * @return Строка вида "Ticket to Main Hall for Ivan".
     */
    std::string getInfo();

    /**
     * @brief Возвращает время покупки билета.
     * @return Объект MyTime.
     */
    MyTime getPurchaseTime();

    /**
     * @brief Возвращает название помещения.
     * @return Строка с названием.
     */
    std::string getVenueName() const;

    /**
     * @brief Возвращает итоговую цену билета.
     * @return Цена в денежных единицах.
     */
    double getFinalPrice() const;

    /**
     * @brief Возвращает имя посетителя.
     * @return Строка с именем.
     */
    std::string getVisitorName() const;
};

#endif // PLANETARIUMPROJECT_TICKET_H