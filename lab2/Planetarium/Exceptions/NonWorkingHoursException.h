/**
 * @file NonWorkingHoursException.h
 * @author Aleks
 * @brief Исключение: обращение к помещению вне рабочего времени.
 *
 * @details
 * Выбрасывается при попытке посещения или покупки билета
 * вне установленного графика работы (с учётом обеда и пересечения полуночи).
 */

#ifndef PLANETARIUMPROJECT_NONWORKINGHOURSEXCEPTION_H
#define PLANETARIUMPROJECT_NONWORKINGHOURSEXCEPTION_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: нерабочее время.
 */
class NonWorkingHoursException : public PlanetariumException {
public:
    explicit NonWorkingHoursException(std::string message_);
};

#endif // PLANETARIUMPROJECT_NONWORKINGHOURSEXCEPTION_H