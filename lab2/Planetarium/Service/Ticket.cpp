#include "Ticket.h"
#include <stdexcept>

Ticket::Ticket(PlanetariumVenue* venue_, std::string visitor, double finalPrice_) :
        venue(venue_), visitorName(std::move(visitor)), finalPrice(finalPrice_), purchaseTime() {
    if(!venue_){
        throw std::invalid_argument("Ticket must have a venue!");
    }
}

std::string Ticket::getInfo() {
    return "Ticket to " + venue->getName() + " for " + visitorName;
}

MyTime Ticket::getPurchaseTime() {
    return purchaseTime;
}

std::string Ticket::getVenueName() const {
    return venue->getName();
}

double Ticket::getFinalPrice() const {
    return finalPrice;
}

std::string Ticket::getVisitorName() const {
    return visitorName;
}

