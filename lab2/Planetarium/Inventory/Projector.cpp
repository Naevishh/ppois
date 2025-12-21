#include <stdexcept>
#include "Projector.h"

Projector::Projector(std::string name_, double brightness_, double throwRatio_, double fov_) :
        Device(std::move(name_)), brightness(brightness_), throwDistance(10),
        throwRatio(throwRatio_), fov(fov_) {}

void Projector::adjustBrightness(int level) {
    brightness += level;
}

void Projector::setProjectionSize(double screenSize) {
    if(screenSize<0 || screenSize>15) throw std::invalid_argument("Invalid size!");
    throwDistance = throwRatio * screenSize;
}

void Projector::project(Screen* screen) {
    if (!active()) turnOn();
    setProjectionSize(screen->getLength());
}

void Projector::setThrowDistance(double throwDistance_) {
    if(throwDistance_<0) throw std::invalid_argument("Invalid distance!");
    throwDistance = throwDistance_;
}

void Projector::setTechnology(Enums::ProjectionTechnology tech) {
    technology = tech;
}

void Projector::setResolution(Enums::StandardResolution res) {
    resolution = res;
}

void Projector::setLamp(Enums::LightSource light) {
    lamp = light;
}

double Projector::getBrightness() const {
    return brightness;
}

double Projector::getThrowDistance() const {
    return throwDistance;
}

double Projector::getThrowRatio() const {
    return throwRatio;
}

double Projector::getFov() const {
    return fov;
}