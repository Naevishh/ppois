/**
 * @file DegreeRangeError.h
 * @author Aleks
 * @brief Исключение: угол (азимут/высота) вне допустимого диапазона.
 *
 * @details
 * Азимут должен быть в [0, 360], высота — в [-90, 90].
 * Выбрасывается при попытке установить некорректные координаты.
 */

#ifndef PLANETARIUMPROJECT_DEGREERANGEERROR_H
#define PLANETARIUMPROJECT_DEGREERANGEERROR_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: недопустимое значение угла.
 */
class DegreeRangeError : public PlanetariumException {
public:
    explicit DegreeRangeError(std::string message_);
};

#endif // PLANETARIUMPROJECT_DEGREERANGEERROR_H