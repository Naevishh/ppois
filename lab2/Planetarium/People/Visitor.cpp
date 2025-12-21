#include "Visitor.h"

Visitor::Visitor(std::string name_, int age_, Enums::DiscountCategory category_) :
        Human(std::move(name_), age_), category(category_) {}

void Visitor::buyTicket(Ticket* ticket) {
    tickets.push_back(ticket);
}

Enums::DiscountCategory Visitor::getCategory() const {
    return category;
}

bool Visitor::canVisitVenue(PlanetariumVenue* venue) {
    for (const auto& ticket : tickets) {
        if (ticket->getVenueName() == venue->getName()) return true;
    }
    return false;
}