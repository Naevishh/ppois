#include "PlanetariumFacade.h"
#include "../Validation/StringValidator.h"
include <stdexcept>

PlanetariumFacade::PlanetariumFacade(PlanetariumProjector* projector, AudioSystem* system, Seating* seats,
                                     DomeShapedScreen* screen) {
    StarHall hall("StarHall", 100, projector, system, seats, screen);
    venues.push_back(hall);
}

Ticket* PlanetariumFacade::sellTicketToVisitor(const std::string& venueName, Visitor& visitor, const MyTime curTime) {
    if (!StringValidator::validate(venueName)) throw std::invalid_argument("Invalid name!");
    PlanetariumVenue* venue = findVenueByName(venueName);
    if (!venue) return nullptr;
    venue->addVisitors(1);
    return ticketOffice.sellTicket(venue, visitor, curTime);
}

void PlanetariumFacade::addVenue(PlanetariumVenue* venue) {
    venues.push_back(*venue);
    ticketOffice.addVenue(venue);
}

void PlanetariumFacade::openFacadeVenue(const std::string &venueName){
    PlanetariumVenue* venue = findVenueByName(venueName);
    if (!venue) return;
    venue->openVenue();
}

PlanetariumVenue* PlanetariumFacade::findVenueByName(const std::string& venueName) {
    if (!StringValidator::validate(venueName)) throw std::invalid_argument("Invalid name!");
    for (PlanetariumVenue &venue : venues) {
        if (venueName == venue.getName()) {
            return &venue;
        }
    }
    return nullptr;
}
