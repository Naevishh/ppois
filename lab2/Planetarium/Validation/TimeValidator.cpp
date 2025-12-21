#include "TimeValidator.h"
#include <ctime>

int TimeValidator::getCurrentYear() {
    time_t current = time(nullptr);
    struct tm* now = localtime(&current);
    return now->tm_year + 1900;
}

bool TimeValidator::isLeapYear(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int TimeValidator::getDaysInMonth(int month, int year) {
    switch (month) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            return 31;
        case 4: case 6: case 9: case 11:
            return 30;
        case 2:
            if (year != -1 && isLeapYear(year)) return 29;
            return 28;
        default:
            return 0;
    }
}

int TimeValidator::stringToInt(const std::string& str) {
    try {
        return std::stoi(str);
    } catch (...) {
        return -1;
    }
}

bool TimeValidator::isValidHour(const std::string& hourStr) {
    int hour = stringToInt(hourStr);
    return hour >= 0 && hour <= 23;
}

bool TimeValidator::isValidHour(int hour) {
    return hour >= 0 && hour <= 23;
}

bool TimeValidator::isValidMinute(const std::string& minuteStr) {
    int minute = stringToInt(minuteStr);
    return minute >= 0 && minute <= 59;
}

bool TimeValidator::isValidMinute(int minute) {
    return minute >= 0 && minute <= 59;
}

bool TimeValidator::isValidSecond(const std::string& secondStr) {
    int second = stringToInt(secondStr);
    return second >= 0 && second <= 59;
}

bool TimeValidator::isValidSecond(int second) {
    return second >= 0 && second <= 59;
}

bool TimeValidator::isValidDay(const std::string& dayStr, int month, int year) {
    int day = stringToInt(dayStr);
    return isValidDay(day, month, year);
}

bool TimeValidator::isValidDay(int day, int month, int year) {
    if (day < 1 || day > 31) return false;
    if (month != -1) {
        int maxDays = getDaysInMonth(month, year);
        return day <= maxDays;
    }
    return true;
}

bool TimeValidator::isValidMonth(const std::string& monthStr) {
    int month = stringToInt(monthStr);
    return month >= 1 && month <= 12;
}

bool TimeValidator::isValidMonth(int month) {
    return month >= 1 && month <= 12;
}

bool TimeValidator::isValidYear(const std::string& yearStr, int minYear, int maxYearsFuture) {
    int year = stringToInt(yearStr);
    return isValidYear(year, minYear, maxYearsFuture);
}

bool TimeValidator::isValidYear(int year, int minYear, int maxYearsFuture) {
    int currentYear = getCurrentYear();
    return year >= minYear && year <= (currentYear + maxYearsFuture);
}

bool TimeValidator::isValidTime(int hour, int minute, int second) {
    if (!isValidHour(hour) || !isValidMinute(minute)) return false;
    if (second != -1 && !isValidSecond(second)) return false;
    return true;
}

bool TimeValidator::isValidDate(int day, int month, int year) {
    if (!isValidMonth(month)) return false;
    if (!isValidYear(year)) return false;
    return isValidDay(day, month, year);
}

bool TimeValidator::isValidDateTime(int day, int month, int year, int hour, int minute, int second) {
    return isValidDate(day, month, year) && isValidTime(hour, minute, second);
}