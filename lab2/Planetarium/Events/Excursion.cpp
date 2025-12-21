#include <stdexcept>
#include "Excursion.h"
#include "../Validation/StringValidator.h"

Excursion::Excursion(const std::string& name, double duration, Enums::ActivityTheme theme, Museum* museum_,
                     std::string routeName_) :
        Activity(name, duration, theme, museum_),
        routeName(std::move(routeName_)), museum(museum_) {}

bool Excursion::isAvailableInLanguage(const std::string& language_) const {
    if(!StringValidator::validate(language_)) throw std::invalid_argument("Invalid language!");
    for (const auto &language : languages) {
        if (language == language_) return true;
    }
    return false;
}

bool Excursion::isRoutePopular() {
    double total = 0;
    for (const auto &exhibit : routeExhibits) {
        total += exhibit->getRating();
    }
    return total / routeExhibits.size() > 8;
}

std::string Excursion::hold(const Date& date) {
    for (const auto &exhibit: routeExhibits) {
        museum->viewExhibit(exhibit);
    }
    return "Excursion '" + getName() + "' is held on " + date.getDate() + ". Route is called '" + routeName + "'.";
}

void Excursion::addLanguage(const std::string& language) {
    if (!StringValidator::validate(language)) {
        throw std::invalid_argument("Invalid language!");
    }
    languages.push_back(language);
}

void Excursion::addExhibit(Exhibit* exhibit) {
    if (exhibit == nullptr) {
        throw std::invalid_argument("Exhibit cannot be null!");
    }
    routeExhibits.push_back(exhibit);
}