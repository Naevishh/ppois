#include "PriceCalculator.h"
#include "../Utils/Enums.h"

PriceCalculator::PriceCalculator(int maxAge, int discountAge) :
        maxFreeAge(maxAge), maxDiscountAge(discountAge) {}

int PriceCalculator::getMaxFreeAge() const {
    return maxFreeAge;
}

int PriceCalculator::getMaxDiscountAge() const {
    return maxDiscountAge;
}

double PriceCalculator::calculatePrice(double basePrice, const Visitor& visitor) const {
    if(basePrice<0) throw std::invalid_argument("Invalid price!");
    Enums::DiscountCategory category_ = visitor.getCategory();
    using discount = Enums::DiscountCategory;
    if (category_ == discount::PUPIL || category_ == discount::SENIOR) {
        return basePrice * 0.5;
    } else if (category_ == discount::STUDENT) {
        return basePrice * 0.6;
    } else if (category_ == discount::DISABLED || category_ == discount::VETERAN) {
        return 0;
    } else if (category_ == discount::EMPLOYEE) {
        return basePrice * 0.7;
    } else {
        if (visitor.getAge() <= maxFreeAge) return 0;
        else if (visitor.getAge() <= maxDiscountAge) return basePrice * 0.4;
        else return basePrice;
    }
}