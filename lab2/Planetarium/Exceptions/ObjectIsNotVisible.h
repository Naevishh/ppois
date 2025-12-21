/**
 * @file ObjectIsNotVisible.h
 * @author Aleks
 * @brief Исключение: астрономический объект не виден в указанное время.
 *
 * @details
 * Возникает при попытке наблюдать объект, который находится ниже горизонта
 * или вне видимого временного окна.
 */

#ifndef PLANETARIUMPROJECT_OBJECTISNOTVISIBLE_H
#define PLANETARIUMPROJECT_OBJECTISNOTVISIBLE_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: объект не виден.
 */
class ObjectIsNotVisible : public PlanetariumException {
public:
    explicit ObjectIsNotVisible(std::string message_);
};

#endif // PLANETARIUMPROJECT_OBJECTISNOTVISIBLE_H