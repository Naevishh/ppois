#include "Screen.h"

Screen::Screen(const std::string& name, double width_, double length_) :
        Device(name), width(width_), length(length_) {}

double Screen::getWidth() const {
    return width;
}

double Screen::getLength() const {
    return length;
}

void Screen::calculateAspectRatio() {
    aspectRatio = width / length;
}

double Screen::calculateArea() const {
    return width * length;
}