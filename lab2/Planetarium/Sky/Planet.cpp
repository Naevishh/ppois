#include "Planet.h"
#include "../Exceptions/DegreeRangeError.h"
#include <cmath>

Planet::Planet(const std::string& name_,  double magnitude_, double absMagnitude_, double azimuth_,
       double altitude_, Enums::PlanetType type_, double orbitalPeriod_, double semiMajorAxis_,
       double semiMinorAxis_, double mass_) :
        AstronomicalObject(name_, magnitude_, absMagnitude_, azimuth_, altitude_,
                           Enums::ObjectType::PLANET), type(type_), hostStar(nullptr),
        orbitalPeriod(orbitalPeriod_), semiMajorAxis(semiMajorAxis_),
        semiMinorAxis(semiMinorAxis_), mass(mass_){}

double Planet::getEccentricity() const{
    double b=semiMinorAxis;
    double a=semiMajorAxis;
    return sqrt(1-b*b/(a*a));
}
double Planet::getDistanceToHostStar(double trueAnomaly) const {
    if (trueAnomaly>360 || trueAnomaly<0) throw DegreeRangeError("Истинная аномалия может быть от 0° до 360°");
    double e=getEccentricity();
    double a=semiMajorAxis;
    return (a * (1 - e*e)) / (1 + e * cos(trueAnomaly));
}

void Planet::addMoon(const Moon& moon){ moons.push_back(moon); }
int Planet::getMoonCount() const { return moons.size(); }

void Planet::setHostStar(std::shared_ptr<Star> star) {
    hostStar = std::move(star);
}

double Planet::calculateOrbitLength() const {
    double a=semiMajorAxis;
    double b=semiMinorAxis;
    return 2*3.14*sqrt((a*a+b*b)/2);
}

Enums::PlanetType Planet::getPlanetType() const{
    return type;
}
