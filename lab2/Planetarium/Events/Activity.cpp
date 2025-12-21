#include <stdexcept>
#include "Activity.h"
#include "../Validation/StringValidator.h"
#include "../Facade/PlanetariumVenue.h"

Activity::Activity(const std::string& name_, double duration_, Enums::ActivityTheme theme_, PlanetariumVenue* activityPlace_):
        name(name_), duration(duration_), host(nullptr), theme(theme_), activityPlace(activityPlace_) {}

void Activity::addQualifiedPosition(Enums::EmployeePosition position) {
    ableToHold.push_back(position);
}

void Activity::setRules(const std::string &rules_) {
    if (!StringValidator::validate(rules_)) throw std::invalid_argument("Invalid argument!");
    rules = rules_;
}

bool Activity::canBeHeldBy(const Employee& employee) {
    for(const auto& position : ableToHold) {
        if(employee.getPosition() == position) return true;
    }
    return false;
}

void Activity::appointHost(Employee* employee) {
    if (canBeHeldBy(*employee)) host = employee;
    activityPlace->chooseCurator(this);
}

void Activity::setHost(Employee* employee) {
    host = employee;
}

bool Activity::isPossible() {
    return activityPlace->IsOpen();
}

std::string Activity::getName() const {
    return name;
}

double Activity::getDuration() const {
    return duration;
}

Employee* Activity::getHost() const {
    return host;
}

std::vector<Enums::EmployeePosition> Activity::getAbleToHold() const {
    return ableToHold;
}

Enums::ActivityTheme Activity::getTheme() const {
    return theme;
}

PlanetariumVenue* Activity::getActivityPlace() const {
    return activityPlace;
}

std::string Activity::hold(const Date& date) {
    return name + " is being held on " + date.getDate() + ".";
}

PlanetariumVenue* Activity::getPlace() const {
    return activityPlace;
}