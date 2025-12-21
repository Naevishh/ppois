#include "Exhibit.h"
#include "../Exceptions/BreakingRules.h"
#include "../Validation/StringValidator.h"
#include <stdexcept>

Exhibit::Exhibit(std::string name_, bool handOn_) :
        name(std::move(name_)), totalViews(0), visitorRating(0), handOn(handOn_) {}

std::string Exhibit::getName() const {
    return name;
}

std::string Exhibit::getInfo() const {
    return info;
}

double Exhibit::getRating() const {
    return visitorRating;
}

int Exhibit::getTotalViews() const {
    return totalViews;
}

void Exhibit::addInfo(std::string info_) {
    if(!StringValidator::validate(info_)) throw std::invalid_argument("Invalid info!");
    info = std::move(info_);
}

void Exhibit::view() {
    totalViews++;
}

void Exhibit::updateRating(int rating) {
    if(rating<0 || rating>10) throw std::invalid_argument("Invalid rating!");
    ratings.push_back(rating);
    totalViews++;
    visitorRating = (visitorRating * (totalViews - 1) + rating) / ratings.size();
}

bool Exhibit::isExhibitPopular() const {
    return visitorRating > 8;
}

void Exhibit::touchExhibit() {
    if (!handOn) throw BreakingRules(name + " cannot be touched!");
}