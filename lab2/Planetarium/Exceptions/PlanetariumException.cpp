#include "PlanetariumException.h"

PlanetariumException::PlanetariumException(std::string message_) : message(std::move(message_)) {}

const char* PlanetariumException::what() const noexcept {
    return message.c_str();
}
