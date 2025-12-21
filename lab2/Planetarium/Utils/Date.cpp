#include "Date.h"
#include "../Validation/TimeValidator.h"
#include <ctime>
#include <stdexcept>

Date::Date(int year_, int month_, int day_) : weather_() {
    if (!TimeValidator::isValidDate(day_, month_, year_))
        throw std::invalid_argument("Invalid time!");
    year=year_;
    month=month_;
    day=day_;
}

std::string Date::getDate() const {
    return (toString(day) + "." + toString(month) + "." + toString(year));
}

std::string Date::toString(int int_) {
    if (int_ < 10) return ('0' + std::to_string(int_));
    else return std::to_string(int_);
}

Enums::WeatherCondition Date::getWeather() const {
    return weather_.getWeatherCondition();
}

bool Date::operator==(const Date& date) const {
    return year == date.year && month == date.month && day == date.day;
}

bool Date::operator<(const Date& date) const {
    if (year < date.year) return true;
    else if (year == date.year) {
        if (month < date.month) return true;
        else if (month == date.month) return day < date.day;
        else return false;
    }
    else return false;
}

bool Date::operator>(const Date& date) const {
    return date < *this;
}

Date Date::operator+(int years) const {
    Date result = *this;
    result.year += years;
    return result;
}

Date Date::currentDate() {
    time_t currentDate_ = time(nullptr);
    struct tm *now = localtime(&currentDate_);
    return {now->tm_year + 1900, now->tm_mon + 1, now->tm_mday};
}

void Date::setYear(int year_) {
    year = year_;
}

void Date::setMonth(int month_) {
    month = month_;
}

void Date::setDay(int day_) {
    day = day_;
}

void Date::setWeather(const Weather& weather) {weather_=weather;}