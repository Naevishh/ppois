#include "Auditorium.h"
#include "../Exceptions/CantUseDevice.h"


Auditorium::Auditorium(const std::string& name, int capacity, Seating* seats_, Projector* projector_,
                       InteractiveWhiteboard* board_) :
        PlanetariumVenue(name, capacity), seats(seats_), projector(projector_), board(board_) {}

void Auditorium::setupForPresentation(const Date& date) {
    if (!projector->canBeUsed(date) || !board->canBeUsed(date))
        throw CantUseDevice("Presentation devices are unsafe to use.");
    projector->project(board);
    board->readyForProjection();
}

void Auditorium::setupForLecture(const Date& date, bool projectorNeeded) {
    if (!board->canBeUsed(date))
        throw CantUseDevice(board->getName() + " is unsafe to use.");
    if (projectorNeeded) {
        if (!projector->canBeUsed(date))
            throw CantUseDevice(projector->getName() + " is unsafe to use.");
        projector->project(board);
        board->readyForProjection();
    } else board->readyForLecture();
}

std::string Auditorium::holdLecture(const Date& date, Lecture* lecture) {
    try {
        setupForLecture(date, lecture->isProjectorNeeded());
        return "Lecture with theme '" + lecture->getLectureTheme() + "'";
    } catch (const CantUseDevice &exception) {
        std::string message = exception.what();
        return "Error: " + message;
    }
}