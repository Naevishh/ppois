#include "AstronomicalObject.h"
#include <cmath>
#include "../Validation/TimeValidator.h"

AstronomicalObject::AstronomicalObject(const std::string& name_, double magnitude_, double absMagnitude_,
                                       double azimuth_, double altitude_, Enums::ObjectType type_) :
        name(name_), magnitude(magnitude_), absoluteMagnitude(absMagnitude_),
        position(azimuth_, altitude_), type(type_) {}

double AstronomicalObject::getAbsoluteMagnitude() const {
    return absoluteMagnitude;
}

Enums::ObjectType AstronomicalObject::getType() const {
    return type;
}

std::string AstronomicalObject::getName() const {
    return name;
}

SkyPosition AstronomicalObject::getPosition() const {
    return position;
}

double AstronomicalObject::getMagnitude() const {
    return magnitude;
}

double AstronomicalObject::getDiameter() const {
    return diameter;
}

void AstronomicalObject::setDiameter(double diameter_){
    diameter=diameter_;
}

bool AstronomicalObject::isVisibleToNakedEye() const {
    return magnitude < 6;
}

double AstronomicalObject::calculateDistance() const {
    return pow(10, (absoluteMagnitude - magnitude + 5) / 5);
}

double AstronomicalObject::calculateAngularDiameter() const {
    return atan((diameter / 2) / calculateDistance()) * 60;
}

void AstronomicalObject::setRiseTime(int hours, int minutes, int seconds) {
    if (!TimeValidator::isValidTime(hours, minutes, seconds))
        throw std::invalid_argument("Invalid time!");
    riseTime = MyTime(hours, minutes, seconds);
}

void AstronomicalObject::setSetTime(int hours, int minutes, int seconds) {
    if (!TimeValidator::isValidTime(hours, minutes, seconds))
        throw std::invalid_argument("Invalid time!");
    setTime = MyTime(hours, minutes, seconds);
}

bool AstronomicalObject::isVisibleAtTime(const MyTime& time) const {
    if (riseTime < setTime) {
        return time >= riseTime && time <= setTime;
    } else {
        return time >= riseTime || time <= setTime;
    }
}
