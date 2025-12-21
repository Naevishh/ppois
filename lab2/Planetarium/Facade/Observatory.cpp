#include "Observatory.h"
#include <stdexcept>
#include "../Exceptions/BadWeather.h"
#include "../Exceptions/ObjectIsNotVisible.h"
#include "../Exceptions/DeviceCapabilityException.h"
#include "../Exceptions/CantUseDevice.h"



Observatory::Observatory(const std::string& name_, int capacity_, Telescope* telescope_) :
        PlanetariumVenue(name_, capacity_), telescope(telescope_), isDomeOpen(false),
        domeRotationAngle(0) {}

bool Observatory::checkWeatherConditions(const Date& date) {
    return date.getWeather() == Enums::WeatherCondition::SUNNY;
}

void Observatory::openDome() {
    isDomeOpen = true;
}

void Observatory::setDomeToPosition(const SkyPosition& position) {
    domeRotationAngle = position.getAzimuth();
}

void Observatory::rotateDome(double angle) {
    domeRotationAngle += angle;
}

std::string Observatory::observeObject(const AstronomicalObject& object, const Date& date, const MyTime& time) {
    if (!checkWeatherConditions(date))
        throw BadWeather("Unsuitable weather for observation.");
    if (!telescope->canBeUsed(date)) throw CantUseDevice(telescope->getName() + " is unsafe to use.");
    if (!telescope->active()) telescope->turnOn();
    openDome();
    if (!object.isVisibleAtTime(time))
        throw ObjectIsNotVisible(object.getName() + " cannot be seen now.");
    setDomeToPosition(object.getPosition());
    if (!telescope->canObserve(object))
        throw DeviceCapabilityException(object.getName() + " is too faint or small for telescope '" + telescope->getName() + "'.");
    return object.getName() + " is being observed.";
}