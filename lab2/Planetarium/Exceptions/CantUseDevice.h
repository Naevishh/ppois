/**
 * @file CantUseDevice.h
 * @author Aleks
 * @brief Исключение: устройство нельзя использовать (вне гарантии или требует ТО).
 *
 * @details
 * Проверяется через Device::canBeUsed(). Выбрасывается, если гарантия истекла
 * или прошло больше времени, чем разрешено интервалом ТО.
 */

#ifndef PLANETARIUMPROJECT_CANTUSEDEVICE_H
#define PLANETARIUMPROJECT_CANTUSEDEVICE_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: устройство небезопасно или не пригодно к использованию.
 */
class CantUseDevice : public PlanetariumException {
public:
    explicit CantUseDevice(std::string message_);
};

#endif // PLANETARIUMPROJECT_CANTUSEDEVICE_H