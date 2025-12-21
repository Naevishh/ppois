#include "TicketOffice.h"
#include "Ticket.h"
#include <stdexcept>
#include "../Exceptions/VenueClosedException.h"
#include "../Exceptions/NonWorkingHoursException.h"
#include "../Exceptions/CapacityExceededException.h"

TicketOffice::TicketOffice() : totalRevenue(0), calculator(5, 10) {}

TicketOffice::TicketOffice(int maxFreeAge, int maxDiscountAge) :
        totalRevenue(0), calculator(maxFreeAge, maxDiscountAge) {}

double TicketOffice::getPrice(PlanetariumVenue* venue, const Visitor& visitor) {
    return calculator.calculatePrice(venue->getTicketPrice(), visitor);
}

Ticket* TicketOffice::sellTicket(PlanetariumVenue* venue, Visitor& visitor, const MyTime& currentTime) {
    checkVenue(venue, currentTime);
    if (!venue->IsOpen()) throw VenueClosedException(venue->getName() + " is closed.");
    double price = getPrice(venue, visitor);
    Ticket* newTicket = new Ticket(venue, visitor.getName(), price);
    soldTickets.push_back(newTicket);
    totalRevenue += price;
    return newTicket;
}

void TicketOffice::checkVenue(PlanetariumVenue* venue, const MyTime& currentTime) {
    if (!venue->IsOpen())
        throw VenueClosedException("Помещение закрыто по техническим причинам.");

    MyTime openTime = venue->getOpeningTime();
    MyTime closeTime = venue->getClosingTime();

    bool isOpeningAfterClosing = openTime > closeTime;

    bool inWorkingHours;
    if (isOpeningAfterClosing) {
        inWorkingHours = (currentTime >= openTime) || (currentTime <= closeTime);
    } else {
        inWorkingHours = (currentTime >= openTime) && (currentTime <= closeTime);
    }

    if (!inWorkingHours) {
        throw NonWorkingHoursException("Нерабочее время!");
    }

    if (venue->getCurrentVisitors() + 1 > venue->getCapacity()) {
        throw CapacityExceededException("Все билеты проданы.");
    }
}

void TicketOffice::addVenue(PlanetariumVenue* venue) {
    availableVenues.push_back(venue);
}

std::string TicketOffice::printReport() const {
    return "Total revenue: " + std::to_string(totalRevenue) + "\n" +
           "Tickets sold: " + std::to_string(soldTickets.size());
}