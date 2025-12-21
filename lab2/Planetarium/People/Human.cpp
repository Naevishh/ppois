#include "Human.h"

Human::Human(std::string name_, int age_) : name(std::move(name_)), age(age_) {}

std::string Human::getName() const {
    return name;
}

int Human::getAge() const {
    return age;
}