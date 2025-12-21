/**
 * @file IncompatibleDevices.h
 * @author Aleks
 * @brief Исключение: попытка использовать несовместимые устройства.
 *
 * @details
 * Например, купольный проектор с плоским экраном, или неподдерживаемый тип подключения.
 */

#ifndef PLANETARIUMPROJECT_INCOMPATIBLEDEVICES_H
#define PLANETARIUMPROJECT_INCOMPATIBLEDEVICES_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: устройства несовместимы.
 */
class IncompatibleDevices : public PlanetariumException {
public:
    explicit IncompatibleDevices(std::string message_);
};

#endif // PLANETARIUMPROJECT_INCOMPATIBLEDEVICES_H