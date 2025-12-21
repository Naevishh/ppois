#include "PlanetariumProjector.h"
#include <stdexcept>
#include "../Exceptions/IncompatibleDevices.h"
#include "../Exceptions/DeviceCapabilityException.h"
#include <cmath>

PlanetariumProjector::PlanetariumProjector(const std::string& name, double brightness_, double throwRatio_, double fov_) :
        Projector(name, brightness_, throwRatio_, fov_) {}

void PlanetariumProjector::setProjectionSize(double screenRadius) {
    if(screenRadius<0 || screenRadius>15) throw std::invalid_argument("Invalid radius!");
    setThrowDistance(screenRadius / sin((getFov()*M_PI/180) / 2));
}

void PlanetariumProjector::addObject(AstronomicalObject* object){
    objects.push_back(object);
}

void PlanetariumProjector::projectObject(DomeShapedScreen* screen, AstronomicalObject* object) {
    if (!screen->isProjectorCompatible(*this))
        throw IncompatibleDevices(getName() + " is not compatible with the screen.");
    bool hasObject = false;
    for (const auto& obj : objects) {
        if (obj->getName() == object->getName()) {
            hasObject = true;
            break;
        }
    }
    if (!hasObject) throw DeviceCapabilityException("Planetarium projector doesn't have " + object->getName() + ".");
    project(screen);
    currentObjectName = object->getName();
}

void PlanetariumProjector::projectShow(DomeShapedScreen* screen, const Enums::BuiltInPlanetariumShow& show) {
    if (!screen->isProjectorCompatible(*this))
        throw IncompatibleDevices(getName() + " is not compatible with the screen.");
    project(screen);
    currentShow = show;
}

Enums::BuiltInPlanetariumShow PlanetariumProjector::getShow() const{
    return currentShow;
}
