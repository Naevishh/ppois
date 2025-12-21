#include <stdexcept>
#include "InteractiveWhiteboard.h"

InteractiveWhiteboard::Tool::Tool() :
        color(Enums::ToolColor::BLACK), type(Enums::ToolType::PEN), width(5) {}

InteractiveWhiteboard::InteractiveWhiteboard(const std::string& name, double width_, double length_)
        : Screen(name, width_, length_), currentTool(), multiTouch(false) {}

void InteractiveWhiteboard::readyForProjection() {
    if (active()) {
        clearScreen();
        turnOff();
    }
}

void InteractiveWhiteboard::setBasicTool() {
    selectTool(Enums::ToolType::PEN);
    setPenColor(Enums::ToolColor::BLACK);
    setPenWidth(5);
}

void InteractiveWhiteboard::readyForLecture() {
    if (!active()) turnOn();
    else {
        clearScreen();
        setBasicTool();
        multiTouch = false;
    }
}

void InteractiveWhiteboard::enableMultiTouch() {
    multiTouch = true;
}

void InteractiveWhiteboard::clearScreen() {
    content = "";
}

void InteractiveWhiteboard::selectTool(Enums::ToolType type_) {
    currentTool.type = type_;
}

void InteractiveWhiteboard::setPenColor(Enums::ToolColor color_) {
    currentTool.color = color_;
}

void InteractiveWhiteboard::setPenWidth(int width_) {
    if(width_<0 || width_>30) throw std::invalid_argument("Invalid width!");
    currentTool.width = width_;
}

InteractiveWhiteboard::Tool InteractiveWhiteboard::getTool()const{ return currentTool;}