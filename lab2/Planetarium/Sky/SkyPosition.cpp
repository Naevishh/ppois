#include "SkyPosition.h"
#include "../Exceptions/DegreeRangeError.h"

SkyPosition::SkyPosition(double azimuth_, double altitude_) :
        azimuth(azimuth_), altitude(altitude_) {}

double SkyPosition::getAzimuth() const {
    return azimuth;
}

double SkyPosition::getAltitude() const {
    return altitude;
}

void SkyPosition::setAzimuth(double azimuth_) {
    if(azimuth_<0 || azimuth_>360) throw DegreeRangeError("Invalid azimuth!");
    azimuth = azimuth_;
}

void SkyPosition::setAltitude(double altitude_) {
    if(altitude_<-90 || altitude_>90) throw DegreeRangeError("Invalid azimuth!");
    altitude = altitude_;
}

bool SkyPosition::isAboveHorizon() const {
    return altitude >= 0;
}

std::string SkyPosition::toString() const {
    return "Az: " + std::to_string(azimuth) + "°, Alt: " + std::to_string(altitude) + "°";
}