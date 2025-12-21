#include <iostream>
#include "Device.h"

Device::Device(std::string name_) :
        name(std::move(name_)), isActive(false),
        warrantyExpiryDate(Date::currentDate()+3),
        lastMaintenance(Date::currentDate()),
        maintenanceInterval(1) {}

void Device::turnOn() {
    isActive = true;
}

void Device::turnOff() {
    isActive = false;
}

void Device::setMaintenanceInterval(int interval) {
    maintenanceInterval = interval;
}

void Device::setlastMaintenance(int year_, int month_, int day_) {
    lastMaintenance.setYear(year_);
    lastMaintenance.setMonth(month_);
    lastMaintenance.setDay(day_);
}

bool Device::active() const {
    return isActive;
}

bool Device::isUnderWarranty(const Date& currentDate) const {
    return currentDate < warrantyExpiryDate;
}

bool Device::needsMaintenance(const Date& currentDate) {
    Date nextMaintenance = lastMaintenance + maintenanceInterval;
    return currentDate > nextMaintenance;
}

bool Device::canBeUsed(const Date& currentDate) {
    return isUnderWarranty(currentDate) && !needsMaintenance(currentDate);
}

std::string Device::getName() const {
    return name;
}

Date Device::getWarrantyExpiryDate() const {
    return warrantyExpiryDate;
}

Date Device::getLastMaintenance() const {
    return lastMaintenance;
}

int Device::getMaintenanceInterval() const {
    return maintenanceInterval;
}