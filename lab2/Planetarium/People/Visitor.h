/**
 * @file Visitor.h
 * @author Aleks
 * @brief Класс для представления посетителя планетария.
 *
 * @details
 * Visitor наследуется от Human и расширяет его информацией о льготной категории
 * и списке купленных билетов. Используется при расчёте цен и проверке доступа к помещениям.
 */

#ifndef PLANETARIUMPROJECT_VISITOR_H
#define PLANETARIUMPROJECT_VISITOR_H

#include <vector>
#include "Human.h"
#include "../Service/Ticket.h"
#include "../Utils/Enums.h"

class PlanetariumVenue; // Forward declaration для избежания циклической зависимости

/**
 * @brief Класс посетителя планетария.
 *
 * Содержит категорию льгот (студент, ветеран и т.д.) и историю билетов.
 * Может проверять, имеет ли доступ к определённому помещению.
 */
class Visitor : public Human {
private:
    Enums::DiscountCategory category; ///< Категория льгот посетителя.
    std::vector<Ticket*> tickets;     ///< Список купленных билетов.

public:
    /**
     * @brief Конструктор посетителя.
     *
     * @param name_ Имя посетителя.
     * @param age_ Возраст (в годах).
     * @param category_ Категория льгот (например, STUDENT, SENIOR).
     */
    Visitor(std::string name_, int age_, Enums::DiscountCategory category_);

    /**
     * @brief Регистрирует покупку билета.
     *
     * @param ticket Указатель на объект Ticket (не проверяется на nullptr).
     * @note Метод не проверяет валидность билета — только добавляет в список.
     */
    void buyTicket(Ticket* ticket);

    /**
     * @brief Возвращает льготную категорию посетителя.
     * @return Значение перечисления DiscountCategory.
     */
    Enums::DiscountCategory getCategory() const;

    /**
     * @brief Проверяет, имеет ли посетитель билет на указанное помещение.
     *
     * @param venue Указатель на помещение планетария.
     * @return true, если среди купленных билетов есть билет на это помещение; иначе false.
     * @see Ticket::getVenueName
     */
    bool canVisitVenue(PlanetariumVenue* venue);
};

#endif // PLANETARIUMPROJECT_VISITOR_H