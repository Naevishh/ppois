#include <stdexcept>
#include "Seating.h"

Seating::Seating(int seatsNumber_) : seatsNumber(seatsNumber_) {}

int Seating::getSeatsNumber() const {
    return seatsNumber;
}

void Seating::setRowsNumber(int rows_) {
    if(rows_<0) throw std::invalid_argument("Invalid row number!");
    rows = rows_;
}

int Seating::calculateSeatsPerRow() {
    return seatsNumber / rows;
}