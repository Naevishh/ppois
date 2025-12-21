#include <stdexcept>
#include "Star.h"
#include "../Validation/StringValidator.h"

Star::Star(const std::string& name_, double magnitude_, double absMagnitude_, double azimuth_, double altitude_,
           Enums::SpectralClass spectralClass_, bool isMultiple_, double mass_) :
        AstronomicalObject(name_, magnitude_, absMagnitude_, azimuth_, altitude_, Enums::ObjectType::STAR),
        spectralClass(spectralClass_), isMultiple(isMultiple_), mass(mass_) {}

void Star::addConstellation(const std::string& constellation_) {
    if (!StringValidator::validate(constellation_)) throw std::invalid_argument("Invalid constellation name!");

    constellation = constellation_;
}

Enums::SpectralClass Star::getSpectralClass() const {
    return spectralClass;
}

bool Star::getIsMultiple() const {
    return isMultiple;
}

double Star::getMass() const {
    return mass;
}

std::string Star::getConstellation() const {
    return constellation;
}