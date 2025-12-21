#include <gtest/gtest.h>
#include "StarHall.h"
#include "Observatory.h"
#include "Museum.h"
#include "Auditorium.h"
#include "PlanetariumFacade.h"
#include "PlanetariumProjector.h"
#include "AudioSystem.h"
#include "Seating.h"
#include "DomeShapedScreen.h"
#include "Telescope.h"
#include "Projector.h"
#include "InteractiveWhiteboard.h"
#include "AstronomicalObject.h"
#include "Lecture.h"
#include "Exhibit.h"
#include "TicketOffice.h"
#include "Visitor.h"
#include "CantUseDevice.h"
#include "VenueClosedException.h"
#include "CapacityExceededException.h"
#include "VenueIsEmpty.h"
#include "BadWeather.h"
#include "DeviceCapabilityException.h"
#include "ObjectIsNotVisible.h"
#include "Event.h"
#include "BreakingRules.h"

class FacadeTest : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(FacadeTest, ConstructorAndBasicGetters) {
    PlanetariumVenue venue("TestVenue", 100);
    EXPECT_EQ(venue.getName(), "TestVenue");
    EXPECT_EQ(venue.getCapacity(), 100);
    EXPECT_FALSE(venue.IsOpen());
    EXPECT_EQ(venue.getCurrentVisitors(), 0);
    EXPECT_EQ(venue.getTicketPrice(), 30);
}

TEST_F(FacadeTest, OpenCloseVenue) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    EXPECT_TRUE(venue.IsOpen());
    venue.closeVenue();
    EXPECT_FALSE(venue.IsOpen());
    EXPECT_EQ(venue.getCurrentVisitors(), 0);
}

TEST_F(FacadeTest, AddVisitorsSuccess) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    EXPECT_NO_THROW(venue.addVisitors(50));
    EXPECT_EQ(venue.getCurrentVisitors(), 50);
}

TEST_F(FacadeTest, AddVisitorsThrowsCapacityExceeded) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    venue.addVisitors(90);
    EXPECT_THROW(venue.addVisitors(20), CapacityExceededException);
}

TEST_F(FacadeTest, AddVisitorsThrowsInvalidArgument) {
    PlanetariumVenue venue("TestVenue", 100);
    EXPECT_THROW(venue.addVisitors(-5), std::invalid_argument);
}

TEST_F(FacadeTest, RemoveVisitorsSuccess) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    venue.addVisitors(50);
    EXPECT_NO_THROW(venue.removeVisitors(30));
    EXPECT_EQ(venue.getCurrentVisitors(), 20);
}

TEST_F(FacadeTest, RemoveVisitorsThrowsWhenEmpty) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    EXPECT_THROW(venue.removeVisitors(10), VenueIsEmpty);
}

TEST_F(FacadeTest, RemoveVisitorsThrowsOutOfRange) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    venue.addVisitors(5);
    EXPECT_THROW(venue.removeVisitors(10), std::out_of_range);
}

TEST_F(FacadeTest, HostEventSuccess) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.openVenue();
    venue.setSchedule(9, 0, 8, 22, 0, 60);
    Employee organizer("John", 30, Enums::EmployeePosition::EDUCATION_COORDINATOR);
    Date date(2025, 12, 1);
    Event event("Test Event", date, 30, &organizer);
    std::string result = venue.hostEvent(event);
    EXPECT_NE(result.find("Test Event"), std::string::npos);
    EXPECT_NE(result.find("John"), std::string::npos);
    EXPECT_EQ(venue.getCurrentVisitors(), 30);
}

TEST_F(FacadeTest, HostEventThrowsWhenClosed) {
    PlanetariumVenue venue("TestVenue", 100);
    Employee organizer("John", 30, Enums::EmployeePosition::EDUCATION_COORDINATOR);
    Date date(2025, 12, 1);
    Event event("Test Event", date, 30, &organizer);
    EXPECT_THROW(venue.hostEvent(event), VenueClosedException);
}

TEST_F(FacadeTest, SetTicketPrice) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.setTicketPrice(50.5);
    EXPECT_EQ(venue.getTicketPrice(), 50.5);
    EXPECT_THROW(venue.setTicketPrice(-10), std::invalid_argument);
}

TEST_F(FacadeTest, ScheduleOperations) {
    PlanetariumVenue venue("TestVenue", 100);
    venue.setSchedule(9, 0, 8, 13, 0, 60);
    EXPECT_EQ(venue.getOpeningTime().getHours(), 9);
    EXPECT_EQ(venue.getClosingTime().getHours(), 17);
    EXPECT_EQ(venue.getLunchStart().getHours(), 13);
    EXPECT_EQ(venue.getLunchEnd().getHours(), 14);
}

TEST_F(FacadeTest, StarHallConstructor) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 10.0, 10.0);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    EXPECT_EQ(hall.getName(), "Hall");
    EXPECT_EQ(hall.getCapacity(), 50);
}

TEST_F(FacadeTest, StarHallSetupForProjectionSuccess) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);

    EXPECT_NO_THROW(hall.setupForProjection(Date::currentDate()));
}

TEST_F(FacadeTest, StarHallWatchObjectSuccess) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Date validDate(2025, 12, 20);
    SkyPosition pos(45.0, 30.0);
    AstronomicalObject obj("Mars", -12.74, 0.21, 45.0, 30.0, Enums::ObjectType::PLANET);
    EXPECT_NE(hall.watchObject(validDate, &obj).find("Mars"), std::string::npos);
}

TEST_F(FacadeTest, StarHallWatchShowSuccess) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Date validDate(2025, 12, 20);
    EXPECT_EQ(hall.watchShow(validDate, Enums::BuiltInPlanetariumShow::SOLAR_SYSTEM_DEMO), "The show is going on.");
}

TEST_F(FacadeTest, AuditoriumConstructor) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    EXPECT_EQ(auditorium.getName(), "Aud");
    EXPECT_EQ(auditorium.getCapacity(), 200);
}

TEST_F(FacadeTest, AuditoriumSetupForPresentationSuccess) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date validDate(2025, 12, 20);
    EXPECT_NO_THROW(auditorium.setupForPresentation(validDate));
}

TEST_F(FacadeTest, AuditoriumSetupForPresentationThrows) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    projector.setlastMaintenance(2020,7,8);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date date(2024, 1, 1);
    EXPECT_THROW(auditorium.setupForPresentation(date), CantUseDevice);
}

TEST_F(FacadeTest, AuditoriumSetupForLectureWithProjector) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date validDate(2025, 12, 20);
    EXPECT_NO_THROW(auditorium.setupForLecture(validDate, true));
}

TEST_F(FacadeTest, AuditoriumSetupForLectureWithoutProjector) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date validDate(2025, 12, 20);
    EXPECT_NO_THROW(auditorium.setupForLecture(validDate, false));
}

TEST_F(FacadeTest, AuditoriumHoldLectureSuccess) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date validDate(2025, 12, 20);
    Lecture lecture("Space", 70, Enums::ActivityTheme::EDUCATION,&auditorium,Enums::Theme::SPACE_EXPLORATION_HISTORY);
    std::string result = auditorium.holdLecture(validDate, &lecture);
    EXPECT_NE(result.find("Space"), std::string::npos);
}

TEST_F(FacadeTest, AuditoriumHoldLectureFailure) {
    Seating seats(200);
    Projector projector("Proj", 3000, 1.2, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Date date(2024, 1, 1);
    board.setlastMaintenance(2022,2,2);
    Lecture lecture("Space",  70, Enums::ActivityTheme::EDUCATION,&auditorium,Enums::Theme::SPACE_EXPLORATION);
    std::string result = auditorium.holdLecture(date, &lecture);
    EXPECT_NE(result.find("Error:"), std::string::npos);
}

TEST_F(FacadeTest, ObservatoryConstructor) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    EXPECT_EQ(obs.getName(), "Obs");
    EXPECT_EQ(obs.getCapacity(), 50);
}

TEST_F(FacadeTest, ObservatoryDomeOperations) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    EXPECT_NO_THROW(obs.openDome());
    SkyPosition pos(45.0, 30.0);
    EXPECT_NO_THROW(obs.setDomeToPosition(pos));
    EXPECT_NO_THROW(obs.rotateDome(15.0));
}

TEST_F(FacadeTest, ObservatoryObserveObjectSuccess) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    Date date(2025, 6, 15);
    Weather weather(Enums::WeatherCondition::SUNNY);
    date.setWeather(weather);
    MyTime time(20, 0, 0);
    AstronomicalObject moon("Moon", -12.74, 0.21, 45.0, 30.0, Enums::ObjectType::MOON);
    moon.setDiameter(3474);
    moon.setRiseTime(18, 0, 0);
    moon.setSetTime(6, 0, 0);
    std::string result = obs.observeObject(moon, date, time);
    EXPECT_NE(result.find("Moon"), std::string::npos);
}

TEST_F(FacadeTest, ObservatoryObserveObjectBadWeather) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    Date date(2025, 1, 1);
    Weather weather(Enums::WeatherCondition::SNOWY);
    date.setWeather(weather);
    MyTime time(20, 0, 0);
    AstronomicalObject moon("Moon", -12.74, 0.21, 45.0, 30.0, Enums::ObjectType::PLANET);
    moon.setDiameter(3474);
    moon.setRiseTime(18, 0, 0);
    moon.setSetTime(6, 0, 0);
    EXPECT_THROW(obs.observeObject(moon, date, time), BadWeather);
}

TEST_F(FacadeTest, MuseumConstructor) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    EXPECT_EQ(museum.getName(), "Museum");
    EXPECT_EQ(museum.getCapacity(), 100);
}

TEST_F(FacadeTest, ExhibitOperations) {
    Exhibit exhibit("Rock", false);
    exhibit.addInfo("Lunar sample.");
    EXPECT_EQ(exhibit.getName(), "Rock");
    EXPECT_FALSE(exhibit.getInfo().empty());
}

TEST_F(FacadeTest, ExhibitViewAndTouch) {
    Exhibit touchable("Touchable", true);
    touchable.addInfo("Info");
    EXPECT_EQ(touchable.getTotalViews(), 0);
    touchable.view();
    EXPECT_EQ(touchable.getTotalViews(), 1);
    EXPECT_NO_THROW(touchable.touchExhibit());

    Exhibit nonTouchable("NonTouchable", false);
    EXPECT_THROW(nonTouchable.touchExhibit(), BreakingRules);
}

TEST_F(FacadeTest, MuseumRateExhibit) {
    Exhibit exhibit("Exhibit", true);
    EXPECT_NO_THROW(Museum::rateExhibit(&exhibit, 8));
    EXPECT_THROW(Museum::rateExhibit(&exhibit, -1), std::invalid_argument);
    EXPECT_THROW(Museum::rateExhibit(&exhibit, 11), std::invalid_argument);
}

TEST_F(FacadeTest, MuseumViewExhibit) {
    Exhibit exhibit("Exhibit", true);
    exhibit.addInfo("Info");
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    std::string result = museum.viewExhibit(&exhibit);
    EXPECT_EQ(result, "Info");
}

TEST_F(FacadeTest, MuseumInteractWithExhibit) {
    Exhibit* exhibit = new Exhibit("Exhibit", true);
    exhibit->addInfo("Info");
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    museum.addExhibit(exhibit);
    std::string result = museum.interactWithExhibit("Exhibit");
    EXPECT_EQ(result, "Info");
}

TEST_F(FacadeTest, MuseumInteractWithExhibitInvalidName) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    EXPECT_THROW(museum.interactWithExhibit(""), std::invalid_argument);
}

TEST_F(FacadeTest, MuseumGetAverageRating) {
    Exhibit* e1 = new Exhibit("E1", true);
    Exhibit* e2 = new Exhibit("E2", true);
    e1->updateRating(8);
    e2->updateRating(6);
    Museum museum("Museum", 100, 2, Enums::Theme::SPACE_EXPLORATION);
    museum.addExhibit(e1);
    museum.addExhibit(e2);
    EXPECT_DOUBLE_EQ(museum.getAverageRating(), 7.0);
}

TEST_F(FacadeTest, MuseumFindMostPopularExhibit) {
    Exhibit* e1 = new Exhibit("E1", true);
    Exhibit* e2 = new Exhibit("E2", true);
    e1->updateRating(5);
    e2->updateRating(9);
    Museum museum("Museum", 100, 2, Enums::Theme::SPACE_EXPLORATION);
    museum.addExhibit(e1);
    museum.addExhibit(e2);
    Exhibit* best = museum.findMostPopularExhibit();
    ASSERT_NE(best, nullptr);
    EXPECT_EQ(best->getName(), "E2");
}

TEST_F(FacadeTest, PlanetariumFacadeConstructor) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 10.0, 10.0);
    PlanetariumFacade facade(&projector, &audio, &seats, &screen);
    PlanetariumVenue* hall = facade.findVenueByName("StarHall");
    ASSERT_NE(hall, nullptr);
    EXPECT_EQ(hall->getName(), "StarHall");
}

TEST_F(FacadeTest, PlanetariumFacadeAddVenue) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 10.0, 10.0);
    PlanetariumFacade facade(&projector, &audio, &seats, &screen);
    PlanetariumVenue venue("NewHall", 50);
    facade.addVenue(&venue);
    PlanetariumVenue* found = facade.findVenueByName("NewHall");
    ASSERT_NE(found, nullptr);
    EXPECT_EQ(found->getName(), "NewHall");
}

TEST_F(FacadeTest, PlanetariumFacadeSellTicketSuccess) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 10.0, 10.0);
    PlanetariumFacade facade(&projector, &audio, &seats, &screen);
    facade.openFacadeVenue("StarHall");
    Visitor visitor("Alice", 25, Enums::DiscountCategory::NONE);
    MyTime curTime(10,0,0);
    Ticket* ticket = facade.sellTicketToVisitor("StarHall", visitor, curTime);
    ASSERT_NE(ticket, nullptr);
    EXPECT_EQ(ticket->getVisitorName(), "Alice");
}

TEST_F(FacadeTest, PlanetariumFacadeSellTicketInvalidName) {
    PlanetariumProjector projector("Proj", 3000, 1.2, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 10.0, 10.0);
    PlanetariumFacade facade(&projector, &audio, &seats, &screen);
    Visitor visitor("Alice", 25, Enums::DiscountCategory::NONE);
    MyTime curTime(10,0,0);
    EXPECT_THROW(facade.sellTicketToVisitor("", visitor,curTime), std::invalid_argument);
}