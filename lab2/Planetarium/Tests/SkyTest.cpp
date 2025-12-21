#include <gtest/gtest.h>
#include "SkyPosition.h"
#include "DegreeRangeError.h"
#include "Enums.h"
#include "MyTime.h"
#include "AstronomicalObject.h"
#include "Star.h"
#include "Planet.h"

class SkyTest : public ::testing::Test{
    void SetUp() override{

    }
    void TearDown() override{

    }
};

TEST_F(SkyTest, ConstructorAndGetters) {
    SkyPosition pos(45.0, 30.0);
    EXPECT_DOUBLE_EQ(pos.getAzimuth(), 45.0);
    EXPECT_DOUBLE_EQ(pos.getAltitude(), 30.0);
}

TEST_F(SkyTest, SettersValid) {
    SkyPosition pos(0, 0);
    pos.setAzimuth(180.0);
    pos.setAltitude(45.0);
    EXPECT_DOUBLE_EQ(pos.getAzimuth(), 180.0);
    EXPECT_DOUBLE_EQ(pos.getAltitude(), 45.0);
}

TEST_F(SkyTest, SettersInvalid) {
    SkyPosition pos(0, 0);
    EXPECT_THROW(pos.setAzimuth(400.0), DegreeRangeError);
    EXPECT_THROW(pos.setAltitude(100.0), DegreeRangeError);
}

TEST_F(SkyTest, IsAboveHorizon) {
    SkyPosition pos1(0, 10.0);
    SkyPosition pos2(0, -10.0);
    EXPECT_TRUE(pos1.isAboveHorizon());
    EXPECT_FALSE(pos2.isAboveHorizon());
}

TEST_F(SkyTest, ToString) {
    SkyPosition pos(123.456, -45.678);
    std::string result = pos.toString();
    EXPECT_TRUE(result.find("123.456") != std::string::npos);
    EXPECT_TRUE(result.find("-45.678") != std::string::npos);
}

TEST_F(SkyTest, ConstructorAndGettersObject) {
    AstronomicalObject obj("Test", 5.0, 2.0, 90.0, 45.0, Enums::ObjectType::STAR);
    EXPECT_EQ(obj.getName(), "Test");
    EXPECT_DOUBLE_EQ(obj.getMagnitude(), 5.0);
    EXPECT_DOUBLE_EQ(obj.getAbsoluteMagnitude(), 2.0);
    EXPECT_EQ(obj.getType(), Enums::ObjectType::STAR);
}

TEST_F(SkyTest, Visibility) {
    AstronomicalObject visible("Visible", 4.0, 1.0, 0, 0, Enums::ObjectType::STAR);
    AstronomicalObject invisible("Invisible", 7.0, 1.0, 0, 0, Enums::ObjectType::STAR);
    EXPECT_TRUE(visible.isVisibleToNakedEye());
    EXPECT_FALSE(invisible.isVisibleToNakedEye());
}

TEST_F(SkyTest, CalculateDistance) {
    AstronomicalObject obj("Test", 10.0, 5.0, 0, 0, Enums::ObjectType::STAR);
    double distance = obj.calculateDistance();
    EXPECT_DOUBLE_EQ(distance, 1);
}

TEST_F(SkyTest, TimeVisibility) {
    AstronomicalObject obj("Test", 5.0, 2.0, 0, 0, Enums::ObjectType::STAR);
    obj.setRiseTime(6, 0, 0);
    obj.setSetTime(18, 0, 0);

    EXPECT_TRUE(obj.isVisibleAtTime(MyTime(12, 0, 0)));
    EXPECT_FALSE(obj.isVisibleAtTime(MyTime(3, 0, 0)));
    EXPECT_TRUE(obj.isVisibleAtTime(MyTime(6, 0, 0)));
    EXPECT_TRUE(obj.isVisibleAtTime(MyTime(18, 0, 0)));
}

TEST_F(SkyTest, TimeValidation) {
    AstronomicalObject obj("Test", 5.0, 2.0, 0, 0, Enums::ObjectType::STAR);
    EXPECT_THROW(obj.setRiseTime(25, 0, 0), std::invalid_argument);
    EXPECT_THROW(obj.setSetTime(12, 70, 0), std::invalid_argument);
}

TEST_F(SkyTest, ConstructorAndGettersStar) {
    Star star("Sun", -26.74, 4.83, 180.0, 45.0, Enums::SpectralClass::G, false, 1.0);
    EXPECT_EQ(star.getName(), "Sun");
    EXPECT_EQ(star.getSpectralClass(), Enums::SpectralClass::G);
    EXPECT_FALSE(star.getIsMultiple());
    EXPECT_DOUBLE_EQ(star.getMass(), 1.0);
}

TEST_F(SkyTest, Constellation) {
    Star star("Vega", 0.03, 0.58, 0, 0, Enums::SpectralClass::A, false, 2.1);
    star.addConstellation("Lyra");
    EXPECT_EQ(star.getConstellation(), "Lyra");
}

TEST_F(SkyTest, InvalidConstellation) {
    Star star("Test", 0.0, 0.0, 0, 0, Enums::SpectralClass::A, false, 1.0);
    EXPECT_THROW(star.addConstellation(""), std::invalid_argument);
}

TEST_F(SkyTest, ConstructorAndEccentricity) {
    Planet planet("Earth", -3.86, -3.99, 0, 0, Enums::PlanetType::TERRESTRIAL,
                  365.25, 1.0, 0.99, 5.97e24);
    EXPECT_EQ(planet.getName(), "Earth");
    EXPECT_EQ(planet.getPlanetType(), Enums::PlanetType::TERRESTRIAL);
    double e = planet.getEccentricity();
    EXPECT_GT(e, 0.0);
    EXPECT_LT(e, 1.0);
}

TEST_F(SkyTest, DistanceToStar) {
    Planet planet("Test", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL,
                  365.25, 1.0, 0.995, 1.0);
    double dist = planet.getDistanceToHostStar(0.0);
    EXPECT_GT(dist, 0.0);
}

TEST_F(SkyTest, InvalidTrueAnomaly) {
    Planet planet("Test", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL,
                  365.25, 1.0, 1.0, 1.0);
    EXPECT_THROW(planet.getDistanceToHostStar(400.0), DegreeRangeError);
    EXPECT_THROW(planet.getDistanceToHostStar(-10.0), DegreeRangeError);
}

TEST_F(SkyTest, Moons) {
    Planet planet("Jupiter", -2.94, -9.4, 0, 0, Enums::PlanetType::GAS_GIANT,
                  4332.59, 5.20, 5.20, 1.898e27);
    EXPECT_EQ(planet.getMoonCount(), 0);

    Moon moon("Io", 5.0, 5.0, 0, 0, &planet, 1.77, 8.93e22);
    planet.addMoon(moon);
    EXPECT_EQ(planet.getMoonCount(), 1);
}

TEST_F(SkyTest, HostStar) {
    auto star = std::make_shared<Star>("Sun", -26.74, 4.83, 0, 0, Enums::SpectralClass::G, false, 1.0);
    Planet planet("Earth", -3.86, -3.99, 0, 0, Enums::PlanetType::TERRESTRIAL,
                  365.25, 1.0, 0.99, 5.97e24);
    planet.setHostStar(star);
}

TEST_F(SkyTest, OrbitLength) {
    Planet planet("Test", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL,
                  365.25, 1.0, 0.99, 1.0);
    double length = planet.calculateOrbitLength();
    EXPECT_GT(length, 0.0);
}

TEST_F(SkyTest, ConstructorAndGettersMoon) {
    Planet host("Earth", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL, 365.25, 1.0, 1.0, 1.0);
    Moon moon("Luna", -12.74, 0.21, 0, 0, &host, 27.32, 7.34e22);
    moon.setDiameter(3474.0);
    EXPECT_EQ(moon.getName(), "Luna");
    EXPECT_EQ(moon.getHostPlanetName(), "Earth");
    EXPECT_DOUBLE_EQ(moon.getOrbitalPeriod(), 27.32);
    EXPECT_DOUBLE_EQ(moon.getMass(), 7.34e22);
    EXPECT_DOUBLE_EQ(moon.getDistanceToPlanet(0.5),398088.5496895971);
}

TEST_F(SkyTest, AngularVelocity) {
    Planet host("Earth", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL, 365.25, 1.0, 1.0, 1.0);
    Moon moon("Test", 0.0, 0.0, 0, 0, &host, 27.32, 1.0);
    double velocity = moon.getAngularVelocity();
    EXPECT_GT(velocity, 0.0);
}

TEST_F(SkyTest, SurfaceGravity) {
    Planet host("Earth", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL, 365.25, 1.0, 1.0, 1.0);
    Moon moon("Test", 0.0, 0.0, 0, 0, &host, 27.32, 1.0);
    double gravity = moon.calculateSurfaceGravity();
    EXPECT_GT(gravity, 0.0);
}

TEST_F(SkyTest, InvalidDistanceToPlanet) {
    Planet host("Earth", 0.0, 0.0, 0, 0, Enums::PlanetType::TERRESTRIAL, 365.25, 1.0, 1.0, 1.0);
    Moon moon("Test", 0.0, 0.0, 0, 0, &host, 27.32, 1.0);
    EXPECT_THROW(moon.getDistanceToPlanet(-10.0), std::invalid_argument);
}

TEST_F(SkyTest, StarPlanetMoon) {
    auto sun = std::make_shared<Star>("Sun", -26.74, 4.83, 0, 0, Enums::SpectralClass::G, false, 1.0);
    sun->addConstellation("None");

    Planet earth("Earth", -3.86, -3.99, 0, 0, Enums::PlanetType::TERRESTRIAL,
                 365.25, 1.0, 0.99, 5.97e24);
    earth.setHostStar(sun);

    Moon moon("Moon", -12.74, 0.21, 0, 0, &earth, 27.32, 7.34e22);
    earth.addMoon(moon);

    EXPECT_EQ(earth.getMoonCount(), 1);
    EXPECT_EQ(moon.getHostPlanetName(), "Earth");
}

TEST_F(SkyTest, BoundaryValues) {
    SkyPosition pos(360.0, 90.0);
    EXPECT_DOUBLE_EQ(pos.getAzimuth(), 360.0);
    EXPECT_DOUBLE_EQ(pos.getAltitude(), 90.0);

    pos.setAzimuth(0.0);
    pos.setAltitude(-90.0);
    EXPECT_DOUBLE_EQ(pos.getAzimuth(), 0.0);
    EXPECT_DOUBLE_EQ(pos.getAltitude(), -90.0);

    EXPECT_THROW(pos.setAzimuth(360.1), DegreeRangeError);
    EXPECT_THROW(pos.setAltitude(90.1), DegreeRangeError);
}

TEST_F(SkyTest, TimeEdgeCases) {
    AstronomicalObject obj("Test", 5.0, 2.0, 0, 0, Enums::ObjectType::STAR);
    obj.setRiseTime(20, 0, 0);
    obj.setSetTime(4, 0, 0);

    EXPECT_TRUE(obj.isVisibleAtTime(MyTime(22, 0, 0)));
    EXPECT_TRUE(obj.isVisibleAtTime(MyTime(2, 0, 0)));
    EXPECT_FALSE(obj.isVisibleAtTime(MyTime(12, 0, 0)));
}
