#include "AudioDevice.h"

AudioDevice::AudioDevice(const std::string& name_) :
        Device(name_), effect(Enums::AudioEffectType::NONE) {}

void AudioDevice::setEffect(Enums::AudioEffectType effect_) {
    effect = effect_;
}

std::vector<Enums::ConnectionType> AudioDevice::getConnections() const {
    return connections;
}

bool AudioDevice::supportsConnection(Enums::ConnectionType connection_) {
    for (const auto& connection: connections) {
        if (connection == connection_) return true;
    }
    return false;
}