/**
 * @file CapacityExceededException.h
 * @author Aleks
 * @brief Исключение: превышена вместимость помещения.
 *
 * @details
 * Выбрасывается при попытке добавить посетителей сверх лимита,
 * установленного для зала, обсерватории и т.д.
 */

#ifndef PLANETARIUMPROJECT_CAPACITYEXCEEDEDEXCEPTION_H
#define PLANETARIUMPROJECT_CAPACITYEXCEEDEDEXCEPTION_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: достигнута максимальная вместимость.
 */
class CapacityExceededException : public PlanetariumException {
public:
    explicit CapacityExceededException(std::string message_);
};

#endif // PLANETARIUMPROJECT_CAPACITYEXCEEDEDEXCEPTION_H