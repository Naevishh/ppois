#include "DomeShapedScreen.h"

DomeShapedScreen::DomeShapedScreen(const std::string& name, double diameter_, double height_) :
        Screen(name, 3.14 * diameter_, 3.14 * diameter_),
        diameter(diameter_), height(height_) {}

double DomeShapedScreen::getDiameter() const {
    return diameter;
}

double DomeShapedScreen::getHeight() const {
    return height;
}

double DomeShapedScreen::calculateArea() const {
return 3.14 * diameter * diameter;
}

bool DomeShapedScreen::isProjectorCompatible(const Projector& projector) const {
    return projector.getThrowRatio() > 2;
}