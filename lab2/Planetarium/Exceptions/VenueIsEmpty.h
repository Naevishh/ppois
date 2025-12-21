/**
 * @file VenueIsEmpty.h
 * @author Aleks
 * @brief Исключение: попытка удалить посетителей из пустого помещения.
 *
 * @details
 * Выбрасывается, когда операция (например, вычитание посетителей) невозможна,
 * потому что в помещении нет никого.
 */

#ifndef PLANETARIUMPROJECT_VENUEISEMPTY_H
#define PLANETARIUMPROJECT_VENUEISEMPTY_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: зал пуст.
 *
 * Наследуется от PlanetariumException.
 */
class VenueIsEmpty : public PlanetariumException {
public:
    /**
     * @brief Конструктор с сообщением об ошибке.
     * @param message_ Описание ситуации.
     */
    explicit VenueIsEmpty(std::string message_);
};

#endif // PLANETARIUMPROJECT_VENUEISEMPTY_H