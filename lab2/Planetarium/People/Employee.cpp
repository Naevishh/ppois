#include "Employee.h"

#include <utility>

Employee::Employee(std::string name, int age, Enums::EmployeePosition position_) : Human(std::move(name), age),
                                                                                   position(position_) {}

Enums::EmployeePosition Employee::getPosition() const {
    return position;
}