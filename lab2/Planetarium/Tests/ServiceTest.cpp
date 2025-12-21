#include <gtest/gtest.h>
#include "Ticket.h"
#include "TicketOffice.h"
#include "PriceCalculator.h"
#include "Schedule.h"
#include "BreakingRules.h"
#include "VenueClosedException.h"
#include "CapacityExceededException.h"
#include "NonWorkingHoursException.h"
#include "Activity.h"
#include "Event.h"

class ServiceTest : public testing::Test{
    void SetUp() override{

    }
    void TearDown() override {

    }

};

TEST_F(ServiceTest, ConstructorAndGetInfo) {
    PlanetariumVenue venue("Cosmos Dome", 100);
    Ticket ticket(&venue, "John Doe", 50.0);

    EXPECT_EQ(ticket.getVenueName(), "Cosmos Dome");
    std::string expected = "Ticket to Cosmos Dome for John Doe";
    EXPECT_EQ(ticket.getInfo(), expected);
}

TEST_F(ServiceTest, GetPurchaseTime) {
    PlanetariumVenue venue("Star Theater", 150);
    Ticket ticket(&venue, "Alice Smith", 40.0);

    MyTime purchaseTime = ticket.getPurchaseTime();
    EXPECT_NO_THROW(purchaseTime.getHours());
    EXPECT_NO_THROW(purchaseTime.getMinutes());
    EXPECT_NO_THROW(purchaseTime.getSeconds());
}

// ==================== TEST_F для класса PriceCalculator ====================
TEST_F(ServiceTest, ConstructorAndGetters) {
    PriceCalculator calculator(5, 18);
    EXPECT_EQ(calculator.getMaxFreeAge(), 5);
    EXPECT_EQ(calculator.getMaxDiscountAge(), 18);
}

TEST_F(ServiceTest, CalculatePriceVariousDiscounts) {
    PriceCalculator calculator(5, 18);

    Visitor pupil("Pupil", 15, Enums::DiscountCategory::PUPIL);
    Visitor student("Student", 20, Enums::DiscountCategory::STUDENT);
    Visitor senior("Senior", 70, Enums::DiscountCategory::SENIOR);
    Visitor disabled("Disabled", 40, Enums::DiscountCategory::DISABLED);
    Visitor veteran("Veteran", 50, Enums::DiscountCategory::VETERAN);
    Visitor employee("Employee", 30, Enums::DiscountCategory::EMPLOYEE);
    Visitor child("Child", 3, Enums::DiscountCategory::NONE);
    Visitor teen("Teen", 12, Enums::DiscountCategory::NONE);
    Visitor adult("Adult", 25, Enums::DiscountCategory::NONE);

    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, pupil), 50.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, student), 60.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, senior), 50.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, disabled), 0.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, veteran), 0.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, employee), 70.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, child), 0.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, teen), 40.0);
    EXPECT_DOUBLE_EQ(calculator.calculatePrice(100.0, adult), 100.0);
}

// ==================== TEST_F для класса Schedule ====================
TEST_F(ServiceTest, DefaultConstructor) {
    Schedule schedule;

    EXPECT_EQ(schedule.getOpeningTime().getHours(), 8);
    EXPECT_EQ(schedule.getOpeningTime().getMinutes(), 0);
    EXPECT_EQ(schedule.getClosingTime().getHours(), 20);
    EXPECT_EQ(schedule.getClosingTime().getMinutes(), 0);
    EXPECT_EQ(schedule.getLunchStart().getHours(), 12);
    EXPECT_EQ(schedule.getLunchStart().getMinutes(), 0);
    EXPECT_EQ(schedule.getLunchEnd().getHours(), 13);
    EXPECT_EQ(schedule.getLunchEnd().getMinutes(), 0);
}

TEST_F(ServiceTest, ParameterizedConstructor) {
    Schedule schedule(10, 30, 8, 13, 0, 60);

    EXPECT_EQ(schedule.getOpeningTime().getHours(), 10);
    EXPECT_EQ(schedule.getOpeningTime().getMinutes(), 30);
    EXPECT_EQ(schedule.getClosingTime().getHours(), 18);
    EXPECT_EQ(schedule.getClosingTime().getMinutes(), 30);
    EXPECT_EQ(schedule.getLunchStart().getHours(), 13);
    EXPECT_EQ(schedule.getLunchStart().getMinutes(), 0);
    EXPECT_EQ(schedule.getLunchEnd().getHours(), 14);
    EXPECT_EQ(schedule.getLunchEnd().getMinutes(), 0);
}

TEST_F(ServiceTest, ConstructorWithTimeOverflow) {
    Schedule schedule(22, 0, 5, 23, 30, 90);

    EXPECT_EQ(schedule.getOpeningTime().getHours(), 22);
    EXPECT_EQ(schedule.getOpeningTime().getMinutes(), 0);
    EXPECT_EQ(schedule.getClosingTime().getHours(), 3);
    EXPECT_EQ(schedule.getClosingTime().getMinutes(), 0);
    EXPECT_EQ(schedule.getLunchStart().getHours(), 23);
    EXPECT_EQ(schedule.getLunchStart().getMinutes(), 30);
    EXPECT_EQ(schedule.getLunchEnd().getHours(), 1);
    EXPECT_EQ(schedule.getLunchEnd().getMinutes(), 0);
}

// ==================== TEST_F для класса TicketOffice ====================
TEST_F(ServiceTest, ConstructorAndBasicFunctions) {
    TicketOffice office(5, 18);

    PlanetariumVenue venue("Test Venue", 100);
    venue.setTicketPrice(100);
    Visitor visitor("Test Visitor", 25, Enums::DiscountCategory::NONE);

    office.addVenue(&venue);

    double price = office.getPrice(&venue, visitor);
    EXPECT_DOUBLE_EQ(price, 100.0);
}

TEST_F(ServiceTest, SellTicketSuccess) {
    TicketOffice office(5, 18);

    PlanetariumVenue venue("Test Venue", 100);
    venue.openVenue();
    venue.setSchedule(9,0,8,
                      13,0,60);
    Visitor visitor("Test Visitor", 25, Enums::DiscountCategory::NONE);

    office.addVenue(&venue);
    MyTime curTime(10,0,0);
    Ticket* ticket = office.sellTicket(&venue, visitor, curTime);
    ASSERT_NE(ticket, nullptr);
    EXPECT_EQ(ticket->getVenueName(), "Test Venue");

    delete ticket;
}

TEST_F(ServiceTest, SellTicketWithDiscount) {
    TicketOffice office(5, 18);

    PlanetariumVenue venue("Test Venue", 100);
    venue.openVenue();
    MyTime current=MyTime::getCurrentTime();
    venue.setSchedule(9,0,8,
                      13,0,60);
    Visitor student("Student", 20, Enums::DiscountCategory::STUDENT);

    office.addVenue(&venue);
    MyTime curTime(10,0,0);
    Ticket* ticket = office.sellTicket(&venue, student,curTime);
    ASSERT_NE(ticket, nullptr);

    delete ticket;
}

TEST_F(ServiceTest, SellTicketVenueClosedException) {
    TicketOffice office(5, 18);

    PlanetariumVenue venue("Closed Venue", 100);
    Visitor visitor("Test Visitor", 25, Enums::DiscountCategory::NONE);
    MyTime curTime(10,0,0);
    EXPECT_THROW(office.sellTicket(&venue, visitor,curTime), VenueClosedException);
}

TEST_F(ServiceTest, CheckVenueCapacityExceeded) {
    TicketOffice office(5, 18);

    PlanetariumVenue venue("Full Venue",100);
    venue.openVenue();
    MyTime current=MyTime::getCurrentTime();
    venue.setSchedule(9,0,8,
                      13,0,60);
    MyTime curTime(10,0,0);
    venue.addVisitors(100);
    Visitor visitor("Test Visitor", 25, Enums::DiscountCategory::NONE);

    EXPECT_THROW(office.checkVenue(&venue,curTime), CapacityExceededException);
}