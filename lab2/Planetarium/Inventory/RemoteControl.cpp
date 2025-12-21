#include "RemoteControl.h"

RemoteControl::RemoteControl(std::vector<Microphone*> mics_, std::vector<Speaker*> speakers_) :
        mics(std::move(mics_)), speakers(std::move(speakers_)) {}

void RemoteControl::TurnAllOn() {
    for (const auto &mic : mics) {
        if (!mic->active()) mic->turnOn();
    }
    for (const auto &speaker : speakers) {
        if (!speaker->active()) speaker->turnOn();
    }
}

void RemoteControl::changeAllVolume(int difference, bool synchronize) {
    if (speakers.empty()) return;
    double average=getAverageVolume();
    for (const auto& speaker : speakers) {
        double volume = speaker->getVolume();
        if (volume == 0) continue;
        if (synchronize) speaker->setVolume(average + difference);
        else speaker->setVolume(volume + difference);
    }
}

void RemoteControl::setAllVolumes(double newVolume) {
    changeAllVolume(0, true);
}

void RemoteControl::addMicrophone(Microphone* newMic) {
    mics.push_back(newMic);
}

void RemoteControl::addSpeaker(Speaker* newSpeaker) {
    speakers.push_back(newSpeaker);
}

double RemoteControl::getAverageVolume() const {
    if (speakers.empty()) return 0;
    double total = 0;
    int counter = 0;
    for (const auto& speaker : speakers) {
        double volume = speaker->getVolume();
        if (volume == 0) continue;
        counter++;
        total += volume;
    }
    return total / counter;
}

void RemoteControl::allVolumeUp() {
    changeAllVolume(2, false);
}

void RemoteControl::allVolumeDown() {
    changeAllVolume(-2, false);
}