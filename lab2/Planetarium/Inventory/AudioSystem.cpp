#include "AudioSystem.h"
#include <algorithm>

AudioSystem::AudioSystem() : remoteControl(mics, speakers) {}

int AudioSystem::devicesCount() {
    return mics.size() + speakers.size();
}

double AudioSystem::totalPowerConsumption() {
    double totalPower = 0;
    for (const auto& speaker: speakers) {
        totalPower += speaker->getPower();
    }
    return totalPower;
}

void AudioSystem::addMicrophone(Microphone* mic) {
    mics.push_back(mic);
    remoteControl.addMicrophone(mic);
}

void AudioSystem::addSpeaker(Speaker* speaker) {
    speakers.push_back(speaker);
    remoteControl.addSpeaker(speaker);
}

bool AudioSystem::removeMicrophone(Microphone* mic) {
    auto it = std::find(mics.begin(), mics.end(), mic);
    if (it != mics.end()) {
        mics.erase(it);
        return true;
    }
    return false;
}

bool AudioSystem::removeSpeaker(Speaker* speaker) {
    auto it = std::find(speakers.begin(), speakers.end(), speaker);
    if (it != speakers.end()) {
        speakers.erase(it);
        return true;
    }
    return false;
}

bool AudioSystem::canBeUsed(const Date& date) {
    for (const auto &mic: mics) {
        if (!mic->canBeUsed(date)) return false;
    }
    for (const auto &speaker: speakers) {
        if (!speaker->canBeUsed(date)) return false;
    }
    return true;
}

void AudioSystem::setUpSystem() {
    remoteControl.TurnAllOn();
    remoteControl.changeAllVolume(+10, true);
}