/**
 * @file DeviceCapabilityException.h
 * @author Aleks
 * @brief Исключение: превышение возможностей устройства.
 *
 * @details
 * Например, телескоп не может наблюдать слишком тусклый объект,
 * или проектор не поддерживает нужное разрешение.
 */

#ifndef PLANETARIUMPROJECT_DEVICECAPABILITYEXCEPTION_H
#define PLANETARIUMPROJECT_DEVICECAPABILITYEXCEPTION_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: устройство не поддерживает запрашиваемую операцию.
 */
class DeviceCapabilityException : public PlanetariumException {
public:
    explicit DeviceCapabilityException(std::string message_);
};

#endif // PLANETARIUMPROJECT_DEVICECAPABILITYEXCEPTION_H