#include "Telescope.h"
#include <cmath>

Telescope::Telescope(const std::string& name_, double diameter_, double focalLength_, Enums::TelescopeType type_) :
        Device(name_), objectiveDiameter(diameter_), focalLength(focalLength_), type(type_),
        position(0, 0) {}

void Telescope::focus(double azimuth_, double altitude_) {
    try{
        position.setAzimuth(azimuth_);
        position.setAltitude(altitude_);
    }catch (...) {
        throw;
    }
}

double Telescope::calculateResolution() const {
    return 116 / objectiveDiameter;
}

bool Telescope::canObserve(const AstronomicalObject& object) const {
    if (object.getMagnitude() > calculateLimitingMagnitude()) {
        return false;
    }
    if (object.getType() == Enums::ObjectType::STAR) {
        return true;
    }
    double angularSize = object.calculateAngularDiameter();
    return angularSize >= calculateResolution();
}

double Telescope::calculateLimitingMagnitude() const {
    return 2.7 + 5 * log10(objectiveDiameter);
}