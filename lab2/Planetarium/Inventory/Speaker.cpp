#include "Speaker.h"

Speaker::Speaker(const std::string& name) :
        AudioDevice(name), volumeLevel(0), powerConsumption(600){}

void Speaker::setVolume(double volume) {
    if (volume < 0) volumeLevel = 0;
    else if (volume > 30) volumeLevel = 30;
    else volumeLevel = volume;
}

void Speaker::startPlayback(double volumeLevel_) {
    if (!active()) turnOn();
    volumeLevel = volumeLevel_;
}

void Speaker::stopPlayback() {
    volumeLevel = 0;
}

double Speaker::getVolume() const {
    return volumeLevel;
}

double Speaker::getPower() const {
    return powerConsumption;
}