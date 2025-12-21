#include "Microphone.h"
#include <stdexcept>
#include "../Exceptions/DeviceSwitchedOff.h"

Microphone::Microphone(const std::string& name, bool isWireless_) :
        AudioDevice(name), isMovable(true), connectedSpeaker(nullptr) {}

void Microphone::mountOnStand() {
    isMovable = false;
}

void Microphone::connectToSpeaker(std::unique_ptr<Speaker> speaker) {
    if (!speaker->active()) throw DeviceSwitchedOff("Device is off.");
    for (const auto& connection : getConnections()) {
        if (speaker->supportsConnection(connection)) {
            connectedSpeaker = std::move(speaker);
            return;
        }
    }
}