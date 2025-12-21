#include "Event.h"
#include <stdexcept>
#include "../Exceptions/BreakingRules.h"


Event::Event(std::string eventName_, Date eventDate_, int visitorsNumber_, Employee* organiser_) :
        eventName(std::move(eventName_)), eventDate(eventDate_), visitors(visitorsNumber_),
        organizer(organiser_) {}

std::string Event::getName() const {
    return eventName;
}

void Event::addVisitor(Visitor* visitor) {
    for (const auto& activity : activities) {
        if (!visitor->canVisitVenue(activity.getActivityPlace())) {
            throw BreakingRules(visitor->getName() + " doesn't have ticket for" + activity.getName());
        }
    }
    visitors.push_back(visitor);
}

double Event::calculateWholePrice() {
    for (const auto& activity : activities) {

    }
    return 0;
}

void Event::includeActivity(const Activity& activity) {
    activities.push_back(activity);
}

double Event::eventDuration(double breakTime) const {
    if(breakTime<0 || breakTime>60) throw std::invalid_argument("Invalid break!");
    double total = 0;
    for (const auto& activity : activities) {
        total += activity.getDuration();
    }
    total += breakTime * (activities.size() - 1);
    return total;
}

int Event::getVisitorsNumber() const {
    return visitors.size();
}

std::string Event::getOrganizerName() const {
    return organizer->getName();
}

void Event::setOrganizer(Employee* organizer_) {
    organizer = organizer_;
}