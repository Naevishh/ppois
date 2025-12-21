/**
 * @file BadWeather.h
 * @author Aleks
 * @brief Исключение: неблагоприятные погодные условия для наблюдений.
 *
 * @details
 * В текущей реализации наблюдения разрешены только при солнечной погоде (SUNNY).
 * Любые другие условия (дождь, туман и т.д.) вызывают это исключение.
 */

#ifndef PLANETARIUMPROJECT_BADWEATHER_H
#define PLANETARIUMPROJECT_BADWEATHER_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: плохая погода.
 */
class BadWeather : public PlanetariumException {
public:
    explicit BadWeather(std::string message_);
};

#endif // PLANETARIUMPROJECT_BADWEATHER_H