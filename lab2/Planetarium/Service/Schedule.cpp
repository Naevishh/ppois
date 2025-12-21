#include "Schedule.h"

Schedule::Schedule(int openingHour, int openingMinutes, int workdayDuration, int lunchStartHour,
                   int lunchStartMinutes, int lunchDuration) :
        openingTime(openingHour, openingMinutes, 0),
        lunchStart(lunchStartHour, lunchStartMinutes, 0) {
    int closingHour = openingHour + workdayDuration;
    if (closingHour >= 24) closingHour -= 24;
    closingTime = MyTime(closingHour, openingMinutes, 0);

    int lunchEndMinutes = lunchStartMinutes + lunchDuration;
    int lunchEndHour = lunchStartHour;
    while (lunchEndMinutes >= 60) {
        lunchEndMinutes -= 60;
        lunchEndHour++;
    }
    if (lunchEndHour >= 24) lunchEndHour -= 24;
    lunchEnd = MyTime(lunchEndHour, lunchEndMinutes, 0);
}

Schedule::Schedule() :
        openingTime(8, 0, 0), closingTime(20, 0, 0),
        lunchStart(12, 0, 0), lunchEnd(13, 0, 0) {}

MyTime Schedule::getOpeningTime() const {
    return openingTime;
}

MyTime Schedule::getClosingTime() const {
    return closingTime;
}

MyTime Schedule::getLunchStart() const {
    return lunchStart;
}

MyTime Schedule::getLunchEnd() const {
    return lunchEnd;
}