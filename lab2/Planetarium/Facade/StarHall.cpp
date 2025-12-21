#include "StarHall.h"
#include <stdexcept>
#include "../Exceptions/CantUseDevice.h"

StarHall::StarHall(const std::string& name, int capacity,
                   PlanetariumProjector* projector, AudioSystem* sound,
                   Seating* hallSeats, DomeShapedScreen* screen) :
        PlanetariumVenue(name, capacity), domeProjector(projector),
        surroundSound(sound), seats(hallSeats), domeScreen(screen) {}

void StarHall::setupForProjection(const Date& date) {
    if (!domeProjector->canBeUsed(date) || !domeScreen->canBeUsed(date))
        throw CantUseDevice("Projection devices are unsafe to use.");

    domeProjector->project(domeScreen);
    surroundSound->setUpSystem();
}

std::string StarHall::watchObject(const Date& date, AstronomicalObject* objectToWatch) {
    try {
        setupForProjection(date);
        domeProjector->projectObject(domeScreen, objectToWatch);
    } catch (const std::exception &exception) {
        std::string message = exception.what();
        return "Error: " + message;
    }
    return objectToWatch->getName() + " is being projected";
}

std::string StarHall::watchShow(const Date& date, const Enums::BuiltInPlanetariumShow& showToWatch) {
    try {
        setupForProjection(date);
        domeProjector->projectShow(domeScreen, showToWatch);
    } catch (const std::exception &exception) {
        std::string message = exception.what();
        return "Error: " + message;
    }
    return "The show is going on.";
}

PlanetariumProjector* StarHall::getProjector() const {return domeProjector; }

DomeShapedScreen* StarHall::getScreen() const {return domeScreen;}