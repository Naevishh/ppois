#include "Stargazing.h"

Stargazing::Stargazing(const std::string& name, double duration, Enums::ActivityTheme theme, StarHall* hall_) :
        Activity(name, duration, theme, hall_), hall(hall_) {}

void Stargazing::addShow(Enums::BuiltInPlanetariumShow show) {
    if (includeShow) {
        shows.push_back(show);
    }
}

void Stargazing::addObjectToWatch(AstronomicalObject* object) {
    objectsToWatch.push_back(object);
}

std::string Stargazing::hold(const Date& date) {
    for (const auto &object: objectsToWatch) {
        hall->watchObject(date, object);
    }
    for (const auto &show: shows) {
        hall->watchShow(date, show);
    }
    return "Stargazing '" + getName() + "' is held on " + date.getDate() + ".";
}

void Stargazing::enableShow() {
    includeShow = true;
}