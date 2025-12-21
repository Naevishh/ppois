/**
 * @file VenueClosedException.h
 * @author Aleks
 * @brief Исключение: помещение планетария закрыто.
 *
 * @details
 * Выбрасывается при попытке провести мероприятие, продать билет
 * или войти в помещение, которое в данный момент закрыто.
 */

#ifndef PLANETARIUMPROJECT_VENUECLOSEDEXCEPTION_H
#define PLANETARIUMPROJECT_VENUECLOSEDEXCEPTION_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: помещение закрыто.
 */
class VenueClosedException : public PlanetariumException {
public:
    explicit VenueClosedException(std::string message_);
};

#endif // PLANETARIUMPROJECT_VENUECLOSEDEXCEPTION_H