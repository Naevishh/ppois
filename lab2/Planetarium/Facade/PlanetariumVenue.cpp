#include "PlanetariumVenue.h"
#include <stdexcept>
#include <cstdlib>
#include "../Events/Activity.h"
#include "../Events/Event.h"
#include "../People/Employee.h"
#include "../Exceptions/VenueClosedException.h"
#include "../Exceptions/CapacityExceededException.h"
#include "../Exceptions/VenueIsEmpty.h"

PlanetariumVenue::PlanetariumVenue(std::string name_, int capacity_) :
        name(std::move(name_)), capacity(capacity_), isOpen(false),
        currentVisitors(0), ticketPrice(30), schedule() {}

void PlanetariumVenue::openVenue() {
    this->isOpen = true;
}

void PlanetariumVenue::closeVenue() {
    this->isOpen = false;
    this->currentVisitors = 0;
}

void PlanetariumVenue::chooseCurator(Activity* activity) {
    if (!curators.empty()) {
        int random_index = rand() % static_cast<int>(curators.size());
        activity->setHost(curators[random_index]);
    }
}

std::string PlanetariumVenue::hostEvent(const Event& event) {
    if (!isOpen) throw VenueClosedException("The" + name + " is closed!");
    try {
        addVisitors(event.getVisitorsNumber());
        return ("An event is being held: \" " + event.getName() +
                " \". Organizer: " + event.getOrganizerName() + ".");
    } catch (const std::exception &exception) {
        std::string message = exception.what();
        return "Error: " + message;
    }
}

void PlanetariumVenue::addVisitors(int visitorsNumber) {
    if(visitorsNumber<0) throw std::invalid_argument("Invalid visitors number!");
    if (visitorsNumber + currentVisitors > capacity)
        throw CapacityExceededException(name + "  is full.");
    currentVisitors += visitorsNumber;
}

void PlanetariumVenue::removeVisitors(int visitorsNumber) {
    if(visitorsNumber<0) throw std::invalid_argument("Invalid visitors number!");
    if (currentVisitors == 0) throw VenueIsEmpty(name + " has no visitors");
    if (currentVisitors < visitorsNumber)
        throw std::out_of_range(name + " has only " + std::to_string(currentVisitors) + " visitors");
    currentVisitors-=visitorsNumber;
}

void PlanetariumVenue::setTicketPrice(double price) {
    if(price<0) throw std::invalid_argument("Invalid price!");
    ticketPrice = price;
}

void PlanetariumVenue::addCurator(Employee* curator) {
    if (curator == nullptr) {
        throw std::invalid_argument("Curator cannot be null.");
    }
    curators.push_back(curator);
}

void PlanetariumVenue::setSchedule(int openingHour, int openingMinutes, int workdayDuration, int lunchStartHour,
                                   int lunchStartMinutes, int lunchDuration) {
    schedule = Schedule(openingHour, openingMinutes, workdayDuration, lunchStartHour,
                        lunchStartMinutes, lunchDuration);
}

std::string PlanetariumVenue::getName() const {
    return name;
}

int PlanetariumVenue::getCapacity() const {
    return capacity;
}

std::vector<Employee*> PlanetariumVenue::getCurators() const {
    return curators;
}

bool PlanetariumVenue::IsOpen() const {
    return isOpen;
}

int PlanetariumVenue::getCurrentVisitors() const {
    return currentVisitors;
}

double PlanetariumVenue::getTicketPrice() const {
    return ticketPrice;
}

MyTime PlanetariumVenue::getOpeningTime() const {
    return schedule.getOpeningTime();
}

MyTime PlanetariumVenue::getClosingTime() const {
    return schedule.getClosingTime();
}

MyTime PlanetariumVenue::getLunchStart() const {
    return schedule.getLunchStart();
}

MyTime PlanetariumVenue::getLunchEnd() const {
    return schedule.getLunchEnd();
}