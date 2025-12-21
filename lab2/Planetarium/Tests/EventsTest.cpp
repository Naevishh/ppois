#include <gtest/gtest.h>
#include <vector>
#include "StarHall.h"
#include "Observatory.h"
#include "Auditorium.h"
#include "Museum.h"
#include "Stargazing.h"
#include "Event.h"
#include "Excursion.h"
#include "Observation.h"

class EventsTest : public ::testing::Test{
    void SetUp() override{

    }
    void TearDown() override{

    }
};

TEST_F(EventsTest, ConstructorInitializesBasicFields) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Intro", 1.5, Enums::ActivityTheme::SCIENCE, &hall);
    EXPECT_EQ(act.getName(), "Intro");
    EXPECT_DOUBLE_EQ(act.getDuration(), 1.5);
    EXPECT_EQ(act.getTheme(), Enums::ActivityTheme::SCIENCE);
    EXPECT_EQ(act.getActivityPlace(), &hall);
    EXPECT_EQ(act.getHost(), nullptr);
}

TEST_F(EventsTest, AddQualifiedPositionStoresPosition) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    Activity act("Test", 1.0, Enums::ActivityTheme::EDUCATION, &obs);
    act.addQualifiedPosition(Enums::EmployeePosition::TOUR_GUIDE);
    auto positions = act.getAbleToHold();
    ASSERT_EQ(positions.size(), 1);
    EXPECT_EQ(positions[0], Enums::EmployeePosition::TOUR_GUIDE);
}

TEST_F(EventsTest, CanBeHeldByReturnsTrueForMatchingEmployee) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Activity act("Lecture", 1.0, Enums::ActivityTheme::EDUCATION, &auditorium);
    act.addQualifiedPosition(Enums::EmployeePosition::LECTURER);
    Employee emp("Dr. Smith",40, Enums::EmployeePosition::LECTURER);
    EXPECT_TRUE(act.canBeHeldBy(emp));
}

TEST_F(EventsTest, CanBeHeldByReturnsFalseForNonMatchingEmployee) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Activity act("Tour", 1.0, Enums::ActivityTheme::HISTORY, &museum);
    act.addQualifiedPosition(Enums::EmployeePosition::ASTRONOMER);
    Employee emp("Janitor", 45,Enums::EmployeePosition::CLEANER);
    EXPECT_FALSE(act.canBeHeldBy(emp));
}

TEST_F(EventsTest, SetRulesAcceptsValidString) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Quiet Time", 2.0, Enums::ActivityTheme::SCIENCE, &hall);
    EXPECT_NO_THROW(act.setRules("Please be silent"));
}

TEST_F(EventsTest, SetRulesThrowsOnEmptyString) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Test", 1.0, Enums::ActivityTheme::NONE, &hall);
    EXPECT_THROW(act.setRules(""), std::invalid_argument);
}

TEST_F(EventsTest, HoldReturnsCorrectStringActivity) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Event", 1.0, Enums::ActivityTheme::NONE, &hall);
    Date date(2025, 12,3);
    std::string result = act.hold(date);
    EXPECT_EQ(result, "Event is being held on 03.12.2025.");
}

TEST_F(EventsTest, ConstructorWorksStargazing) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Stargazing sg("Night Sky", 2.0, Enums::ActivityTheme::SCIENCE, &hall);
    EXPECT_EQ(sg.getName(), "Night Sky");
}

TEST_F(EventsTest, HoldReturnsCorrectStringStargazing) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Stargazing sg("Stars", 1.5, Enums::ActivityTheme::SCIENCE, &hall);
    Date date(2025,12,21);
    std::string result = sg.hold(date);
    EXPECT_EQ(result, "Stargazing 'Stars' is held on 21.12.2025.");
}

TEST_F(EventsTest, ConstructorWorksObservation) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    MyTime time(20, 30,0);
    Observation obsv("Moon Watch", 1.0, Enums::ActivityTheme::SCIENCE, &obs, time);
    EXPECT_EQ(obsv.getName(), "Moon Watch");
}

TEST_F(EventsTest, HoldReturnsCorrectString) {
    Telescope telescope("Tel", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    Observatory obs("Obs", 50, &telescope);
    MyTime time(21,0,0);
    Observation obsv("Planets", 1.5, Enums::ActivityTheme::SCIENCE, &obs, time);
    Date date(2025,12,21);
    std::string result = obsv.hold(date);
    EXPECT_EQ(result, "Observation 'Planets' is held on 21.12.2025.");
}

TEST_F(EventsTest, ConstructorInitializesFields) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Lecture lecture("Galaxies", 1.2, Enums::ActivityTheme::EDUCATION, &auditorium, Enums::Theme::GALAXIES_COSMOLOGY);
    EXPECT_EQ(lecture.getName(), "Galaxies");
    EXPECT_EQ(lecture.getLectureTheme(), "Galaxies and Cosmology");
}

TEST_F(EventsTest, IsProjectorNeededReturnsFalseByDefault) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Lecture lecture("Basics", 1.0, Enums::ActivityTheme::EDUCATION, &auditorium, Enums::Theme::SPACE_TELESCOPES);
    EXPECT_FALSE(lecture.isProjectorNeeded());
}

TEST_F(EventsTest, HoldReturnsStringEndingWithDate) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Lecture lecture("Universe", 1.0, Enums::ActivityTheme::EDUCATION, &auditorium, Enums::Theme::GALAXIES_COSMOLOGY);
    Date date(2025,12,21);
    std::string result = lecture.hold(date);
    EXPECT_NE(result.find("21.12.2025"), std::string::npos);
    EXPECT_NE(result.find("Galaxies and Cosmology"), std::string::npos);
}

TEST_F(EventsTest, ConstructorWorks) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Ancient Sky", 2.0, Enums::ActivityTheme::HISTORY, &museum, "Myth Route");
    EXPECT_EQ(exc.getName(), "Ancient Sky");
}

TEST_F(EventsTest, HoldReturnsStringWithRouteName) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Solar Tour", 1.5, Enums::ActivityTheme::EDUCATION, &museum, "Planet Path");
    Date date(2025,12,21);
    std::string result = exc.hold(date);
    EXPECT_NE(result.find("Planet Path"), std::string::npos);
}

TEST_F(EventsTest, IsAvailableInLanguageThrowsOnInvalidInput) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Tour", 1.0, Enums::ActivityTheme::NONE, &museum, "Main");
    EXPECT_THROW(exc.isAvailableInLanguage(""), std::invalid_argument);
}

TEST_F(EventsTest, ConstructorInitializesFieldsEvent) {
    Employee organizer("Alice", 23, Enums::EmployeePosition::TOUR_GUIDE);
    Date date(2025,12,25);
    Event event("Space Day", date, 10, &organizer);
    EXPECT_EQ(event.getName(), "Space Day");
    EXPECT_EQ(event.getVisitorsNumber(), 10);
    EXPECT_EQ(event.getOrganizerName(), "Alice");
}

TEST_F(EventsTest, EventDurationWithNoActivitiesIsZero) {
    Employee organizer("Bob", 32, Enums::EmployeePosition::PRESENTER);
    Date date(2025,12,25);
    Event event("Empty", date, 0, &organizer);
    EXPECT_DOUBLE_EQ(event.eventDuration(0), 0.0);
}

TEST_F(EventsTest, EventDurationWithOneActivityEqualsItsDuration) {
    Employee organizer("Carol", 24, Enums::EmployeePosition::MANAGER);
    Date date(2025,12,25);
    Event event("Single", date, 0, &organizer);
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Show", 1.5, Enums::ActivityTheme::SCIENCE, &hall);
    event.includeActivity(act);
    EXPECT_DOUBLE_EQ(event.eventDuration(10), 1.5);
}

TEST_F(EventsTest, EventDurationWithTwoActivitiesIncludesOneBreak) {
    Employee organizer("Dave",34, Enums::EmployeePosition::PRESENTER);
    Date date(2025,12,25);
    Event event("Double", date, 0, &organizer);
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    event.includeActivity(Activity("A", 1.0, Enums::ActivityTheme::NONE, &hall));
    event.includeActivity(Activity("B", 2.0, Enums::ActivityTheme::NONE, &hall));
    EXPECT_DOUBLE_EQ(event.eventDuration(5), 1.0 + 2.0 + 5.0);
}

TEST_F(EventsTest, EventDurationThrowsOnNegativeBreak) {
    Employee organizer("Eve", 33, Enums::EmployeePosition::MANAGER);
    Date date(2025,12,25);
    Event event("BreakTest", date, 0, &organizer);
    EXPECT_THROW(event.eventDuration(-1), std::invalid_argument);
}

TEST_F(EventsTest, EventDurationThrowsOnBreakOver60) {
    Employee organizer("Frank", 30, Enums::EmployeePosition::MANAGER);
    Date date(2025,12,25);
    Event event("BreakTest", date, 0, &organizer);
    EXPECT_THROW(event.eventDuration(61), std::invalid_argument);
}

TEST_F(EventsTest, SetOrganizerUpdatesName) {
    Employee org1("Old", 55, Enums::EmployeePosition::MANAGER);
    Employee org2("New", 45, Enums::EmployeePosition::PRESENTER);
    Date date(2025,12,25);
    Event event("Test", date, 0, &org1);
    event.setOrganizer(&org2);
    EXPECT_EQ(event.getOrganizerName(), "New");
}

TEST_F(EventsTest, EnableShowAllowsAddingShows) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Stargazing sg("Cosmos", 2.0, Enums::ActivityTheme::SCIENCE, &hall);
    sg.enableShow();
    sg.addShow(Enums::BuiltInPlanetariumShow::CONSTELLATION_DEMO);
    sg.addShow(Enums::BuiltInPlanetariumShow::STARFIELD_DEMO);
    Date date(2025,12,21);
    EXPECT_NO_THROW(sg.hold(date));
}

TEST_F(EventsTest, AddShowDoesNothingWhenShowNotEnabled) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Stargazing sg("Stars", 1.5, Enums::ActivityTheme::SCIENCE, &hall);
    // do NOT call enableShow()
    sg.addShow(Enums::BuiltInPlanetariumShow::MILKY_WAY_PREVIEW);
    Date date(2025,12,21);
    EXPECT_NO_THROW(sg.hold(date));
}

TEST_F(EventsTest, AddMaterialStoresMaterial) {
    Seating seats(200);
    Projector projector("Proj", 3000, 2.1, 1.047);
    InteractiveWhiteboard board("Board", 2.0, 1.5);
    Auditorium auditorium("Aud", 200, &seats, &projector, &board);
    Lecture lecture("Test", 1.0, Enums::ActivityTheme::EDUCATION, &auditorium, Enums::Theme::ANCIENT_ASTRONOMY);
    lecture.addMaterial(Enums::LectureMaterial::PRESENTATION_SLIDES);
    lecture.addMaterial(Enums::LectureMaterial::HANDOUTS);
    EXPECT_TRUE(lecture.isProjectorNeeded());
}

TEST_F(EventsTest, AddLanguageStoresLanguage) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Tour", 1.0, Enums::ActivityTheme::NONE, &museum, "Route");
    exc.addLanguage("en");
    exc.addLanguage("ru");
    EXPECT_TRUE(exc.isAvailableInLanguage("en"));
    EXPECT_TRUE(exc.isAvailableInLanguage("ru"));
    EXPECT_FALSE(exc.isAvailableInLanguage("de"));
}

TEST_F(EventsTest, IsAvailableInLanguageThrowsOnInvalidLanguage) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Tour", 1.0, Enums::ActivityTheme::NONE, &museum, "Route");
    EXPECT_THROW(exc.isAvailableInLanguage(""), std::invalid_argument);
    EXPECT_THROW(exc.isAvailableInLanguage("123!"), std::invalid_argument);
    EXPECT_NO_THROW(exc.isAvailableInLanguage("en-US"));
    EXPECT_NO_THROW(exc.isAvailableInLanguage("fr"));
}

TEST_F(EventsTest, AddExhibitStoresExhibit) {
    Museum museum("Museum", 100, 10, Enums::Theme::SPACE_EXPLORATION);
    Excursion exc("Expo", 1.0, Enums::ActivityTheme::HISTORY, &museum, "Path");
    Exhibit* ex1 = new Exhibit("Ex1",false);
    Exhibit* ex2 = new Exhibit("Ex2",false);
    ex1->updateRating(9);
    ex2->updateRating(8);
    exc.addExhibit(ex1);
    exc.addExhibit(ex2);
    EXPECT_TRUE(exc.isRoutePopular()); // (9.5 + 8.7) / 2 = 9.1 > 8
}

TEST_F(EventsTest, AppointHostDoesNotSetHostIfEmployeeNotQualified) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Test", 1.0, Enums::ActivityTheme::SCIENCE, &hall);
    act.addQualifiedPosition(Enums::EmployeePosition::LECTURER);
    Employee emp("Guide", 36, Enums::EmployeePosition::TOUR_GUIDE);
    act.appointHost(&emp);
    EXPECT_EQ(act.getHost(), nullptr);
}

TEST_F(EventsTest, AppointHostSetsHostAndTriggersChooseCurator) {
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    Activity act("Test", 1.0, Enums::ActivityTheme::SCIENCE, &hall);
    act.addQualifiedPosition(Enums::EmployeePosition::ASTRONOMER);
    Employee emp("Dr. A", 40, Enums::EmployeePosition::ASTRONOMER);
    act.appointHost(&emp);
    EXPECT_NO_THROW(act.appointHost(&emp));
}

TEST_F(EventsTest, CalculateWholePriceReturnsZeroAsPlaceholder) {
    Employee org("Org", 31,  Enums::EmployeePosition::MANAGER);
    Date date(2025,12,21);
    Event event("Event", date, 0, &org);
    PlanetariumProjector projector("Proj", 3000, 2.1, 1.047);
    AudioSystem audio;
    Seating seats(100);
    DomeShapedScreen screen("Screen", 4, 4);
    StarHall hall("Hall", 50, &projector, &audio, &seats, &screen);
    event.includeActivity(Activity("A", 1.0, Enums::ActivityTheme::NONE, &hall));
    EXPECT_EQ(event.calculateWholePrice(), 0.0);
}

