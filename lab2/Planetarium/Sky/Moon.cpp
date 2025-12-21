#include "Moon.h"
#include "Planet.h"

Moon::Moon(const std::string& name_,  double magnitude_, double absMagnitude_, double azimuth_,
     double altitude_, Planet* hostPlanet_, double period_, double mass_) :
        AstronomicalObject(name_, magnitude_, absMagnitude_, azimuth_, altitude_,Enums::ObjectType::MOON),
        hostPlanet(hostPlanet_), orbitalPeriod(period_), mass(mass_){}

double Moon::getDistanceToPlanet(double diameterFromPlanet) const {
    if(diameterFromPlanet<0) throw std::invalid_argument("Invalid diameter!");
    double radianDiameter = diameterFromPlanet * M_PI / 180.0;
    return getDiameter()/2/tan(radianDiameter/2);
}

double Moon::getAngularVelocity() const {
    return 2 * 3.14 / orbitalPeriod;
}

double Moon::calculateSurfaceGravity() const {
    const double G = 6.67430e-11;
    return G * mass / pow(getDiameter() / 2, 2);
}

std::string Moon::getHostPlanetName() const { return hostPlanet->getName(); }

Planet* Moon::getHostPlanet() const { return hostPlanet; }
double Moon::getOrbitalPeriod() const { return orbitalPeriod; }
double Moon::getMass() const { return mass; }

