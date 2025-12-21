#include "Museum.h"
#include "../Validation/StringValidator.h"
#include <stdexcept>

Museum::Museum(std::string name_, int capacity_, int exhibitsNumber_, Enums::Theme theme_) :
        PlanetariumVenue(std::move(name_), capacity_),
        exhibitsNumber(exhibitsNumber_), theme(theme_) {}

Exhibit* Museum::findExhibit(const std::string& name) {
    for (const auto& exhibit : exhibits) {
        if (exhibit->getName() == name) return exhibit;
    }
    return nullptr;
}

double Museum::getAverageRating() {
    double total = 0;
    for (const auto& exhibit : exhibits) {
        total += exhibit->getRating();
    }
    return total / exhibits.size();
}

Exhibit* Museum::findMostPopularExhibit() {
    size_t index = -1;
    double maxRating = 0;
    for (size_t i = 0; i < exhibits.size(); i++) {
        if (exhibits[i]->getRating() > maxRating) {
            maxRating = exhibits[i]->getRating();
            index = i;
        }
    }
    return (index == -1) ? nullptr : exhibits[index];
}

void Museum::rateExhibit(Exhibit* ratedExhibit, int rating) {
    if(rating<0 || rating>10) throw std::invalid_argument("Invalid rating!");
    ratedExhibit->updateRating(rating);

}

std::string Museum::viewExhibit(Exhibit* exhibit) {
    exhibit->view();
    return exhibit->getInfo();
}

std::string Museum::interactWithExhibit(const std::string& name) {
    if (!StringValidator::validate(name)) throw std::invalid_argument("Invalid name!");
    Exhibit* exhibit = findExhibit(name);
    std::string viewed = viewExhibit(exhibit);
    try {
        exhibit->touchExhibit();
    } catch (const std::exception& exception) {
        std::string message = exception.what();
        return "Error: " + message;
    }
    return viewed;
}

void Museum::addExhibit(Exhibit* exhibit) {
    exhibits.push_back(exhibit);
}

std::vector<Exhibit*> Museum::getExhibits() {
    return exhibits;
}