/**
 * @file DeviceSwitchedOff.h
 * @author Aleks
 * @brief Исключение: попытка использовать выключенное устройство.
 *
 * @details
 * Например, подключение микрофона к выключенному динамику.
 */

#ifndef PLANETARIUMPROJECT_DEVICESWITCHEDOFF_H
#define PLANETARIUMPROJECT_DEVICESWITCHEDOFF_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: устройство выключено.
 */
class DeviceSwitchedOff : public PlanetariumException {
public:
    explicit DeviceSwitchedOff(std::string message_);
};

#endif // PLANETARIUMPROJECT_DEVICESWITCHEDOFF_H