#include "MyTime.h"
#include "../Validation/TimeValidator.h"
#include <ctime>
#include <stdexcept>

MyTime::MyTime() {
    time_t currentTime = time(nullptr);
    struct tm* now = localtime(&currentTime);
    hours = now->tm_hour;
    minutes = now->tm_min;
    seconds = now->tm_sec;
}

MyTime::MyTime(int hours_, int minutes_, int seconds_) :
        hours(hours_), minutes(minutes_), seconds(seconds_) {
    if (!TimeValidator::isValidTime(hours_, minutes_, seconds_))
        throw std::invalid_argument("Invalid time!");
}

std::string MyTime::getTime() const {
    return (toString(hours) + ":" + toString(minutes) + ":" + toString(seconds));
}

std::string MyTime::toString(int int_) {
    return (int_ < 10 ? "0" : "") + std::to_string(int_);
}

bool MyTime::operator==(const MyTime& other) const {
    return hours == other.hours && minutes == other.minutes && seconds == other.seconds;
}

bool MyTime::operator<(const MyTime& other) const {
    if (hours != other.hours) return hours < other.hours;
    if (minutes != other.minutes) return minutes < other.minutes;
    return seconds < other.seconds;
}

bool MyTime::operator>(const MyTime& other) const {
    return other < *this;
}

bool MyTime::operator<=(const MyTime& other) const {
    return !(*this > other);
}

bool MyTime::operator>=(const MyTime& other) const {
    return !(*this < other);
}

MyTime MyTime::getCurrentTime() {
    return {};
}

int MyTime::getSeconds() const { return seconds; }
int MyTime::getMinutes() const { return minutes; }
int MyTime::getHours() const { return hours; }