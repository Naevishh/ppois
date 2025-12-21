#include "Observation.h"

Observation::Observation(const std::string& name, double duration, Enums::ActivityTheme theme, Observatory* observatory_,
                         const MyTime& time) :
        Activity(name, duration, theme, observatory_),
        observatory(observatory_), observationTime(time) {}

void Observation::addObject(AstronomicalObject* object) {
    objectsToObserve.push_back(object);
}

std::string Observation::hold(const Date& date) {
    for (const auto &object: objectsToObserve) {
        observatory->observeObject(*object, date, observationTime);
    }
    return "Observation '" + getName() + "' is held on " + date.getDate() + ".";
}