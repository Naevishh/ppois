#include "gtest/gtest.h"
#include "Human.h"
#include "Visitor.h"
#include "Employee.h"
#include "Ticket.h"
#include "PlanetariumVenue.h"
#include <vector>

class PeopleTest : public ::testing::Test{
    void SetUp() override{

    }
    void TearDown() override{

    }
};

TEST_F(PeopleTest, DifferentAges) {
    Human child("Child", 5);
    Human adult("Adult", 25);
    Human senior("Senior", 70);
    EXPECT_EQ(child.getAge(), 5);
    EXPECT_EQ(adult.getAge(), 25);
    EXPECT_EQ(senior.getAge(), 70);
}

TEST_F(PeopleTest, EmptyName) {
    Human human("", 20);
    EXPECT_EQ(human.getName(), "");
}

TEST_F(PeopleTest, NameWithSpaces) {
    Human human("First Middle Last", 40);
    EXPECT_EQ(human.getName(), "First Middle Last");
}

TEST_F(PeopleTest, ConstructorAndGetters) {
    Visitor visitor("Alice", 20, Enums::DiscountCategory::STUDENT);
    EXPECT_EQ(visitor.getName(), "Alice");
    EXPECT_EQ(visitor.getAge(), 20);
    EXPECT_EQ(visitor.getCategory(), Enums::DiscountCategory::STUDENT);
}

TEST_F(PeopleTest, AllDiscountCategories) {
    Visitor student("Student", 20, Enums::DiscountCategory::STUDENT);
    Visitor child("Child", 10, Enums::DiscountCategory::NONE);
    Visitor senior("Senior", 65, Enums::DiscountCategory::SENIOR);
    Visitor NONE("NONE", 30, Enums::DiscountCategory::NONE);

    EXPECT_EQ(student.getCategory(), Enums::DiscountCategory::STUDENT);
    EXPECT_EQ(child.getCategory(), Enums::DiscountCategory::NONE);
    EXPECT_EQ(senior.getCategory(), Enums::DiscountCategory::SENIOR);
    EXPECT_EQ(NONE.getCategory(), Enums::DiscountCategory::NONE);
}

TEST_F(PeopleTest, BuyTicketAndCanVisit) {
    Visitor visitor("Bob", 25, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue("Main Hall", 100);
    Ticket ticket(&venue, "Bob", 50.0);

    EXPECT_FALSE(visitor.canVisitVenue(&venue));
    visitor.buyTicket(&ticket);
    EXPECT_TRUE(visitor.canVisitVenue(&venue));
}

TEST_F(PeopleTest, MultipleTicketsDifferentVenues) {
    Visitor visitor("Charlie", 30, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue1("Main Hall", 150);
    PlanetariumVenue venue2("Observatory", 50);
    PlanetariumVenue venue3("Exhibition", 200);

    Ticket ticket1(&venue1, "Charlie", 50.0);
    Ticket ticket2(&venue2, "Charlie", 75.0);

    visitor.buyTicket(&ticket1);
    visitor.buyTicket(&ticket2);

    EXPECT_TRUE(visitor.canVisitVenue(&venue1));
    EXPECT_TRUE(visitor.canVisitVenue(&venue2));
    EXPECT_FALSE(visitor.canVisitVenue(&venue3));
}

TEST_F(PeopleTest, MultipleTicketsSameVenue) {
    Visitor visitor("David", 28, Enums::DiscountCategory::STUDENT);
    PlanetariumVenue venue("Main Hall", 120);

    Ticket ticket1(&venue, "David", 40.0);
    Ticket ticket2(&venue, "David", 40.0);

    visitor.buyTicket(&ticket1);
    visitor.buyTicket(&ticket2);

    EXPECT_TRUE(visitor.canVisitVenue(&venue));
}

TEST_F(PeopleTest, CanVisitEmptyTicketList) {
    Visitor visitor("Henry", 50, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue("Any Venue", 70);

    EXPECT_FALSE(visitor.canVisitVenue(&venue));
}

TEST_F(PeopleTest, VenueNameMatchingExact) {
    Visitor visitor("Ivan", 33, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue1("Main Hall", 100);
    PlanetariumVenue venue2("main hall", 100);
    PlanetariumVenue venue3("Main  Hall", 100);

    Ticket ticket(&venue1, "Ivan", 50.0);
    visitor.buyTicket(&ticket);

    EXPECT_TRUE(visitor.canVisitVenue(&venue1));
    EXPECT_FALSE(visitor.canVisitVenue(&venue2));
    EXPECT_FALSE(visitor.canVisitVenue(&venue3));
}

TEST_F(PeopleTest, AgeBoundariesWithCategories) {
    Visitor child("Kid", 3, Enums::DiscountCategory::NONE);
    Visitor teen("Teen", 17, Enums::DiscountCategory::STUDENT);
    Visitor adult("Adult", 30, Enums::DiscountCategory::NONE);
    Visitor old("Old", 80, Enums::DiscountCategory::SENIOR);

    EXPECT_EQ(child.getAge(), 3);
    EXPECT_EQ(teen.getAge(), 17);
    EXPECT_EQ(adult.getAge(), 30);
    EXPECT_EQ(old.getAge(), 80);
}

TEST_F(PeopleTest, DifferentVenueCapacities) {
    Visitor visitor("Test", 25, Enums::DiscountCategory::NONE);
    PlanetariumVenue smallVenue("Small", 10);
    PlanetariumVenue mediumVenue("Medium", 100);
    PlanetariumVenue largeVenue("Large", 1000);

    Ticket ticket1(&smallVenue, "Test", 30.0);
    Ticket ticket2(&mediumVenue, "Test", 50.0);

    visitor.buyTicket(&ticket1);
    visitor.buyTicket(&ticket2);

    EXPECT_TRUE(visitor.canVisitVenue(&smallVenue));
    EXPECT_TRUE(visitor.canVisitVenue(&mediumVenue));
    EXPECT_FALSE(visitor.canVisitVenue(&largeVenue));
}

TEST_F(PeopleTest, ConstructorAndGettersMale) {
    Employee employee("John", 35, Enums::EmployeePosition::TOUR_GUIDE);
    EXPECT_EQ(employee.getName(), "John");
    EXPECT_EQ(employee.getAge(), 35);
    EXPECT_EQ(employee.getPosition(), Enums::EmployeePosition::TOUR_GUIDE);
}

TEST_F(PeopleTest, AllEmployeePositions) {
    Employee director("Director", 50, Enums::EmployeePosition::DIRECTOR);
    Employee deputy("Deputy", 45, Enums::EmployeePosition::DEPUTY_DIRECTOR);
    Employee astronomer("Astro", 40, Enums::EmployeePosition::ASTRONOMER);
    Employee lecturer("Lecturer", 38, Enums::EmployeePosition::LECTURER);
    Employee presenter("Presenter", 32, Enums::EmployeePosition::PRESENTER);
    Employee guide("Guide", 28, Enums::EmployeePosition::TOUR_GUIDE);
    Employee coordinator("Coord", 35, Enums::EmployeePosition::EDUCATION_COORDINATOR);
    Employee technician("Tech", 30, Enums::EmployeePosition::TECHNICIAN);
    Employee projectionist("Proj", 33, Enums::EmployeePosition::PROJECTIONIST);
    Employee seller("Seller", 25, Enums::EmployeePosition::TICKET_SELLER);
    Employee cashier("Cashier", 26, Enums::EmployeePosition::CASHIER);
    Employee security("Security", 29, Enums::EmployeePosition::SECURITY_GUARD);
    Employee cleaner("Cleaner", 40, Enums::EmployeePosition::CLEANER);
    Employee volunteer("Volunteer", 22, Enums::EmployeePosition::VOLUNTEER);

    EXPECT_EQ(director.getPosition(), Enums::EmployeePosition::DIRECTOR);
    EXPECT_EQ(deputy.getPosition(), Enums::EmployeePosition::DEPUTY_DIRECTOR);
    EXPECT_EQ(astronomer.getPosition(), Enums::EmployeePosition::ASTRONOMER);
    EXPECT_EQ(lecturer.getPosition(), Enums::EmployeePosition::LECTURER);
    EXPECT_EQ(presenter.getPosition(), Enums::EmployeePosition::PRESENTER);
    EXPECT_EQ(guide.getPosition(), Enums::EmployeePosition::TOUR_GUIDE);
    EXPECT_EQ(coordinator.getPosition(), Enums::EmployeePosition::EDUCATION_COORDINATOR);
    EXPECT_EQ(technician.getPosition(), Enums::EmployeePosition::TECHNICIAN);
    EXPECT_EQ(projectionist.getPosition(), Enums::EmployeePosition::PROJECTIONIST);
    EXPECT_EQ(seller.getPosition(), Enums::EmployeePosition::TICKET_SELLER);
    EXPECT_EQ(cashier.getPosition(), Enums::EmployeePosition::CASHIER);
    EXPECT_EQ(security.getPosition(), Enums::EmployeePosition::SECURITY_GUARD);
    EXPECT_EQ(cleaner.getPosition(), Enums::EmployeePosition::CLEANER);
    EXPECT_EQ(volunteer.getPosition(), Enums::EmployeePosition::VOLUNTEER);
}

TEST_F(PeopleTest, EmployeeAgeExtremes) {
    Employee young("Young", 18, Enums::EmployeePosition::VOLUNTEER);
    Employee old("Old", 67, Enums::EmployeePosition::DIRECTOR);

    EXPECT_EQ(young.getAge(), 18);
    EXPECT_EQ(old.getAge(), 67);
}

TEST_F(PeopleTest, EmployeeLongName) {
    std::string longName = "Dr. Alexander Maximilian Rodriguez III";
    Employee employee(longName, 45, Enums::EmployeePosition::ASTRONOMER);

    EXPECT_EQ(employee.getName(), longName);
}

TEST_F(PeopleTest, EmployeeWithZeroCapacityVenue) {
    Employee employee("Test", 30, Enums::EmployeePosition::TICKET_SELLER);
    PlanetariumVenue venue("Closed Venue", 0);

    EXPECT_EQ(employee.getName(), "Test");
    EXPECT_EQ(venue.getName(), "Closed Venue");
}

TEST_F(PeopleTest, VisitorIsHuman) {
    Visitor visitor("Test", 20, Enums::DiscountCategory::NONE);
    Human* humanPtr = &visitor;

    EXPECT_EQ(humanPtr->getName(), "Test");
    EXPECT_EQ(humanPtr->getAge(), 20);
}

TEST_F(PeopleTest, EmployeeIsHuman) {
    Employee employee("Test", 30, Enums::EmployeePosition::TECHNICIAN);
    Human* humanPtr = &employee;

    EXPECT_EQ(humanPtr->getName(), "Test");
    EXPECT_EQ(humanPtr->getAge(), 30);
}

TEST_F(PeopleTest, TicketWithNullVenueInVisitor) {
    Visitor visitor("Test", 25, Enums::DiscountCategory::NONE);

    EXPECT_THROW(Ticket ticket(nullptr, "Test", 50.0), std::invalid_argument);
}

TEST_F(PeopleTest, TicketWithEmptyVenueName) {
    Visitor visitor("Test", 25, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue("", 50);
    Ticket ticket(&venue, "Test", 50.0);
    PlanetariumVenue emptyVenue("", 30);

    visitor.buyTicket(&ticket);
    EXPECT_TRUE(visitor.canVisitVenue(&emptyVenue));
}

TEST_F(PeopleTest, VenueWithDifferentCapacities) {
    Visitor visitor("Test", 30, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue1("Star Theater", 250);
    PlanetariumVenue venue2("Star Theater", 500);

    Ticket ticket(&venue1, "Test", 75.0);
    visitor.buyTicket(&ticket);

    EXPECT_TRUE(visitor.canVisitVenue(&venue1));
    EXPECT_TRUE(visitor.canVisitVenue(&venue2));
}

TEST_F(PeopleTest, MultipleVisitorsSameTicket) {
    Visitor visitor1("Alice", 25, Enums::DiscountCategory::STUDENT);
    Visitor visitor2("Bob", 30, Enums::DiscountCategory::NONE);
    PlanetariumVenue venue("Main Hall", 200);
    Ticket ticket(&venue, "Alice", 40.0);

    visitor1.buyTicket(&ticket);
    visitor2.buyTicket(&ticket);

    EXPECT_TRUE(visitor1.canVisitVenue(&venue));
    EXPECT_TRUE(visitor2.canVisitVenue(&venue));
}