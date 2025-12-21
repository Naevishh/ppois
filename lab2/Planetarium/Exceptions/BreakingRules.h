/**
 * @file BreakingRules.h
 * @author Aleks
 * @brief Исключение: нарушение правил поведения в планетарии.
 *
 * @details
 * Например, попытка потрогать экспонат, помеченный как "hands-off".
 */

#ifndef PLANETARIUMPROJECT_BREAKINGRULES_H
#define PLANETARIUMPROJECT_BREAKINGRULES_H

#include "PlanetariumException.h"
#include <string>

/**
 * @brief Исключение: посетитель нарушил правила.
 */
class BreakingRules : public PlanetariumException {
public:
    explicit BreakingRules(std::string message_);
};

#endif // PLANETARIUMPROJECT_BREAKINGRULES_H