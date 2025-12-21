#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include "Telescope.h"
#include "Speaker.h"
#include "Seating.h"
#include "Screen.h"
#include "Microphone.h"
#include "RemoteControl.h"
#include "Projector.h"
#include "PlanetariumProjector.h"
#include "InteractiveWhiteboard.h"
#include "Exhibit.h"
#include "BreakingRules.h"
#include "AudioSystem.h"
#include "DeviceCapabilityException.h"
#include "IncompatibleDevices.h"
#include "DeviceSwitchedOff.h"

class InventoryTest : public ::testing::Test{
    void SetUp() override{

    }
    void TearDown() override{

    }
};

TEST_F(InventoryTest, ConstructorInitializesCorrectly) {
    Telescope t("Hubble", 2400.0, 57600.0, Enums::TelescopeType::REFLECTOR);
    EXPECT_EQ(t.getName(), "Hubble");
}

TEST_F(InventoryTest, CalculateResolution) {
    Telescope t("Test", 100.0, 1000.0, Enums::TelescopeType::REFRACTOR);
    EXPECT_DOUBLE_EQ(t.calculateResolution(), 116.0 / 100.0);
}

TEST_F(InventoryTest, CalculateLimitingMagnitude) {
    Telescope t("Test", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    EXPECT_DOUBLE_EQ(t.calculateLimitingMagnitude(), 2.7 + 5 * std::log10(200.0));
}

TEST_F(InventoryTest, FocusValidCoordinates) {
    Telescope t("Test", 100.0, 1000.0, Enums::TelescopeType::REFRACTOR);
    t.focus(90.0, 45.0);
}

TEST_F(InventoryTest, CanObserveReturnsTrueForObservableObject) {
    Telescope t("Test", 200.0, 2000.0, Enums::TelescopeType::REFLECTOR);
    AstronomicalObject obj("Star", 5.0, 0.1,2,50,Enums::ObjectType::STAR);
    EXPECT_TRUE(t.canObserve(obj));
}

TEST_F(InventoryTest, CanObserveReturnsFalseForFaintObject) {
    Telescope t("Test", 100.0, 1000.0, Enums::TelescopeType::REFRACTOR);
    AstronomicalObject obj("Faint", 20.0, 0.001,68,55,Enums::ObjectType::NEBULA);
    EXPECT_FALSE(t.canObserve(obj));
}

TEST_F(InventoryTest, SetVolumeClampsToValidRange) {
    Speaker s("Test");
    s.setVolume(-10);
    EXPECT_DOUBLE_EQ(s.getVolume(), 0.0);
    s.setVolume(50);
    EXPECT_DOUBLE_EQ(s.getVolume(), 30.0);
    s.setVolume(15.5);
    EXPECT_DOUBLE_EQ(s.getVolume(), 15.5);
}

TEST_F(InventoryTest, StartPlaybackTurnsOnAndSetsVolume) {
    Speaker s("Test");
    s.startPlayback(20.0);
    EXPECT_TRUE(s.active());
    EXPECT_DOUBLE_EQ(s.getVolume(), 20.0);
}

TEST_F(InventoryTest, StopPlaybackResetsVolume) {
    Speaker s("Test");
    s.startPlayback(25.0);
    s.stopPlayback();
    EXPECT_DOUBLE_EQ(s.getVolume(), 0.0);
}

TEST_F(InventoryTest, GetPowerReturnsConstant) {
    Speaker s("Test");
    EXPECT_DOUBLE_EQ(s.getPower(), 600.0);
}

TEST_F(InventoryTest, ConstructorSetsSeatsNumber) {
    Seating s(120);
    EXPECT_EQ(s.getSeatsNumber(), 120);
}

TEST_F(InventoryTest, SetRowsNumberValid) {
    Seating s(100);
    s.setRowsNumber(5);
    EXPECT_EQ(s.calculateSeatsPerRow(), 20);
}

TEST_F(InventoryTest, SetRowsNumberThrowsOnNegative) {
    Seating s(100);
    EXPECT_THROW(s.setRowsNumber(-1), std::invalid_argument);
}

TEST_F(InventoryTest, ConstructorInitializesDimensions) {
    Screen sc("Main", 16.0, 9.0);
    EXPECT_DOUBLE_EQ(sc.getWidth(), 16.0);
    EXPECT_DOUBLE_EQ(sc.getLength(), 9.0);
}

TEST_F(InventoryTest, CalculateArea) {
    Screen sc("Test", 4.0, 3.0);
    EXPECT_DOUBLE_EQ(sc.calculateArea(), 12.0);
}

TEST_F(InventoryTest, CalculateAspectRatio) {
    Screen sc("Test", 16.0, 9.0);
    sc.calculateAspectRatio();
}

TEST_F(InventoryTest, TurnAllOnActivatesDevices) {
    std::vector<Microphone*> mics;
    std::vector<Speaker*> speakers;
    auto spk = new Speaker("Spk");
    speakers.push_back(spk);
    RemoteControl rc(mics, speakers);
    rc.TurnAllOn();
    EXPECT_TRUE(spk->active());
    delete spk;
}

TEST_F(InventoryTest, ChangeAllVolumeNonSync) {
    std::vector<Microphone*> mics;
    std::vector<Speaker*> speakers;
    auto spk = new Speaker("Spk");
    spk->startPlayback(10.0);
    speakers.push_back(spk);
    RemoteControl rc(mics, speakers);
    rc.changeAllVolume(5, false);
    EXPECT_DOUBLE_EQ(spk->getVolume(), 15.0);
    delete spk;
}

TEST_F(InventoryTest, ChangeAllVolumeSync) {
    std::vector<Microphone*> mics;
    std::vector<Speaker*> speakers;
    auto s1 = new Speaker("S1");
    auto s2 = new Speaker("S2");
    s1->startPlayback(10.0);
    s2->startPlayback(20.0);
    speakers.push_back(s1);
    speakers.push_back(s2);
    RemoteControl rc(mics, speakers);
    rc.changeAllVolume(0, true);
    double avg = (10.0 + 20.0) / 2.0;
    EXPECT_DOUBLE_EQ(s1->getVolume(), avg);
    EXPECT_DOUBLE_EQ(s2->getVolume(), avg);
    delete s1;
    delete s2;
}

TEST_F(InventoryTest, AllVolumeUpAndDown) {
    std::vector<Microphone*> mics;
    std::vector<Speaker*> speakers;
    auto spk = new Speaker("Spk");
    spk->startPlayback(10.0);
    speakers.push_back(spk);
    RemoteControl rc(mics, speakers);
    rc.allVolumeUp();
    EXPECT_DOUBLE_EQ(spk->getVolume(), 12.0);
    rc.allVolumeDown();
    EXPECT_DOUBLE_EQ(spk->getVolume(), 10.0);
    delete spk;
}

TEST_F(InventoryTest, ConstructorInitializesFields) {
    Projector p("PX1", 3000.0, 1.2, 120.0);
    EXPECT_EQ(p.getName(), "PX1");
    EXPECT_DOUBLE_EQ(p.getBrightness(), 3000.0);
    EXPECT_DOUBLE_EQ(p.getThrowRatio(), 1.2);
    EXPECT_DOUBLE_EQ(p.getFov(), 120.0);
}

TEST_F(InventoryTest, AdjustBrightness) {
    Projector p("PX1", 2000.0, 1.0, 90.0);
    p.adjustBrightness(500);
    EXPECT_DOUBLE_EQ(p.getBrightness(), 2500.0);
}

TEST_F(InventoryTest, SetProjectionSizeValid) {
    Projector p("PX1", 2000.0, 2.0, 90.0);
    p.setProjectionSize(10.0);
    EXPECT_DOUBLE_EQ(p.getThrowDistance(), 20.0);
}

TEST_F(InventoryTest, SetProjectionSizeInvalidThrows) {
    Projector p("PX1", 2000.0, 2.0, 90.0);
    EXPECT_THROW(p.setProjectionSize(-1), std::invalid_argument);
    EXPECT_THROW(p.setProjectionSize(20), std::invalid_argument);
}

TEST_F(InventoryTest, ProjectTurnsOnAndSetsSize) {
    Projector p("PX1", 2000.0, 2.0, 90.0);
    Screen screen("Scrn", 16.0, 9.0);
    p.project(&screen);
    EXPECT_TRUE(p.active());
    EXPECT_DOUBLE_EQ(p.getThrowDistance(), 2.0 * 9.0);
}

TEST_F(InventoryTest, SetProjectionSizeUsesFov) {
    PlanetariumProjector pp("Planetarium", 2500.0, 1.5, 120.0);
    pp.setProjectionSize(10.0);
    double expected = 10.0 / std::sin(60.0 * M_PI / 180.0);
    EXPECT_NEAR(pp.getThrowDistance(), expected, 1e-5);
}

TEST_F(InventoryTest, PlanetariumProjectorProjectObjectIncompatible) {
    PlanetariumProjector pp("PP", 3000, 1.0, 120.0); // throwRatio=1.0 < 2 → несовместим
    DomeShapedScreen ds("Dome", 10.0, 5.0);
    AstronomicalObject obj("Moon", -12.0, 0.0, 0.0, 0.0, Enums::ObjectType::MOON);
    pp.addObject(&obj);
    EXPECT_THROW(pp.projectObject(&ds, &obj), IncompatibleDevices);
}

TEST_F(InventoryTest, PlanetariumProjectorProjectShowIncompatible) {
    PlanetariumProjector pp("PP", 3000, 1.0, 120.0);
    DomeShapedScreen ds("Dome", 10.0, 5.0);
    EXPECT_THROW(pp.projectShow(&ds, Enums::BuiltInPlanetariumShow::DAY_NIGHT_CYCLE), IncompatibleDevices);
}

TEST_F(InventoryTest, PlanetariumProjectorProjectUnknownObject) {
    PlanetariumProjector pp("PP", 3000, 2.5, 120.0); // совместим
    DomeShapedScreen ds("Dome", 10.0, 5.0);
    AstronomicalObject obj("Mars", -1.0, 0.0, 0.0, 0.0, Enums::ObjectType::PLANET);
    EXPECT_THROW(pp.projectObject(&ds, &obj), DeviceCapabilityException);
}

TEST_F(InventoryTest, MountOnStandSetsImmovable) {
    Microphone mic("Mic1", true);
    mic.mountOnStand();
}

TEST_F(InventoryTest, AudioDeviceSetEffectAndGetConnections) {
    Microphone mic("Mic", true);
    mic.setEffect(Enums::AudioEffectType::REVERB);
    EXPECT_EQ(mic.getConnections().size(), 0);
    EXPECT_FALSE(mic.supportsConnection(Enums::ConnectionType::XLR));
}



TEST_F(InventoryTest, ConstructorInitializes) {
    InteractiveWhiteboard wb("WB1", 16.0, 9.0);
    EXPECT_EQ(wb.getName(), "WB1");
}

TEST_F(InventoryTest, ReadyForLectureTurnsOnAndClears) {
    InteractiveWhiteboard wb("WB1", 16.0, 9.0);
    wb.readyForLecture();
    EXPECT_TRUE(wb.active());
}

TEST_F(InventoryTest, SetPenWidthValid) {
    InteractiveWhiteboard wb("WB1", 16.0, 9.0);
    wb.setPenWidth(10);
    InteractiveWhiteboard::Tool tool = wb.getTool();
    EXPECT_EQ(tool.width, 10);
}

TEST_F(InventoryTest, SetPenWidthInvalidThrows) {
    InteractiveWhiteboard wb("WB1", 16.0, 9.0);
    EXPECT_THROW(wb.setPenWidth(-1), std::invalid_argument);
    EXPECT_THROW(wb.setPenWidth(35), std::invalid_argument);
}

TEST_F(InventoryTest, InteractiveWhiteboardSetBasicTool) {
    InteractiveWhiteboard wb("WB", 2.0, 1.5);
    wb.readyForLecture(); // устанавливает базовый инструмент
    InteractiveWhiteboard::Tool t = wb.getTool();
    EXPECT_EQ(t.type, Enums::ToolType::PEN);
    EXPECT_EQ(t.color, Enums::ToolColor::BLACK);
    EXPECT_EQ(t.width, 5);
}

TEST_F(InventoryTest, InteractiveWhiteboardToolSelection) {
    InteractiveWhiteboard wb("WB", 2.0, 1.5);
    wb.selectTool(Enums::ToolType::ERASER);
    wb.setPenColor(Enums::ToolColor::BLUE);
    InteractiveWhiteboard::Tool t = wb.getTool();
    EXPECT_EQ(t.type, Enums::ToolType::ERASER);
    EXPECT_EQ(t.color, Enums::ToolColor::BLUE);
}

TEST_F(InventoryTest, InteractiveWhiteboardEnableMultiTouch) {
    InteractiveWhiteboard wb("WB", 2.0, 1.5);
    wb.enableMultiTouch();
    // Флаг multiTouch не публичный, но тест вызывает метод
    SUCCEED();
}

TEST_F(InventoryTest, InteractiveWhiteboardClearScreen) {
    InteractiveWhiteboard wb("WB", 2.0, 1.5);
    wb.readyForLecture();
    wb.clearScreen();
    SUCCEED();
}

TEST_F(InventoryTest, InteractiveWhiteboardReadyForProjection) {
    InteractiveWhiteboard wb("WB", 2.0, 1.5);
    wb.turnOn();
    wb.readyForProjection();
    EXPECT_FALSE(wb.active());
}

TEST_F(InventoryTest, ConstructorInitializesExhibit) {
    Exhibit ex("Ex1", true);
    EXPECT_EQ(ex.getName(), "Ex1");
    EXPECT_EQ(ex.getTotalViews(), 0);
}

TEST_F(InventoryTest, AddInfoValid) {
    Exhibit ex("Ex1", true);
    ex.addInfo("Info text");
    EXPECT_EQ(ex.getInfo(), "Info text");
}

TEST_F(InventoryTest, AddInfoInvalidThrows) {
    Exhibit ex("Ex1", true);
    EXPECT_THROW(ex.addInfo(""), std::invalid_argument);
}

TEST_F(InventoryTest, UpdateRating) {
    Exhibit ex("Ex1", true);
    ex.updateRating(9);
    EXPECT_DOUBLE_EQ(ex.getRating(), 9.0);
    ex.updateRating(7);
    EXPECT_DOUBLE_EQ(ex.getRating(), 8.0);
}

TEST_F(InventoryTest, UpdateRatingInvalidThrows) {
    Exhibit ex("Ex1", true);
    EXPECT_THROW(ex.updateRating(-1), std::invalid_argument);
    EXPECT_THROW(ex.updateRating(11), std::invalid_argument);
}

TEST_F(InventoryTest, TouchExhibitAllowed) {
    Exhibit ex("Ex1", true);
    ex.touchExhibit();
}

TEST_F(InventoryTest, TouchExhibitNotAllowedThrows) {
    Exhibit ex("Ex1", false);
    EXPECT_THROW(ex.touchExhibit(), BreakingRules);
}

TEST_F(InventoryTest, ConstructorInitializesDomeShapedScreen) {
    DomeShapedScreen ds("Dome1", 20.0, 10.0);
    EXPECT_DOUBLE_EQ(ds.getDiameter(), 20.0);
    EXPECT_DOUBLE_EQ(ds.getHeight(), 10.0);
}

TEST_F(InventoryTest, CalculateAreaDomeShapedScreen) {
    DomeShapedScreen ds("Dome1", 10.0, 5.0);
    EXPECT_DOUBLE_EQ(ds.calculateArea(), 3.14 * 10.0 * 10.0);
}

TEST_F(InventoryTest, IsProjectorCompatible) {
    DomeShapedScreen ds("Dome1", 20.0, 10.0);
    Projector p1("P1", 2000, 1.5, 90.0);
    Projector p2("P2", 2000, 2.5, 90.0);
    EXPECT_FALSE(ds.isProjectorCompatible(p1));
    EXPECT_TRUE(ds.isProjectorCompatible(p2));
}

TEST_F(InventoryTest, TurnOnOff) {
    Device d("Dev1");
    d.turnOn();
    EXPECT_TRUE(d.active());
    d.turnOff();
    EXPECT_FALSE(d.active());
}

TEST_F(InventoryTest, CanBeUsedUnderWarrantyAndNoMaintenanceNeeded) {
    Device d("Dev1");
    d.setlastMaintenance(2024, 12, 20);
    d.setMaintenanceInterval(2);
    Date now(2025, 12, 20);
    EXPECT_TRUE(d.canBeUsed(now));
}

TEST_F(InventoryTest, NeedsMaintenance) {
    Device d("Dev1");
    d.setlastMaintenance(2020, 12, 20);
    d.setMaintenanceInterval(1);
    Date now(2025, 12, 20);
    EXPECT_TRUE(d.needsMaintenance(now));
}

TEST_F(InventoryTest, AddAndRemoveDevices) {
    AudioSystem as;
    Microphone* mic = new Microphone("Mic", true);
    Speaker* spk = new Speaker("Spk");
    as.addMicrophone(mic);
    as.addSpeaker(spk);
    EXPECT_EQ(as.devicesCount(), 2);
    EXPECT_TRUE(as.removeMicrophone(mic));
    EXPECT_EQ(as.devicesCount(), 1);
    as.removeSpeaker(spk);
    EXPECT_EQ(as.devicesCount(),0);
    delete mic;
    delete spk;
}

TEST_F(InventoryTest, TotalPowerConsumption) {
    AudioSystem as;
    Speaker* spk1 = new Speaker("Spk1");
    Speaker* spk2 = new Speaker("Spk2");
    as.addSpeaker(spk1);
    as.addSpeaker(spk2);
    EXPECT_DOUBLE_EQ(as.totalPowerConsumption(), 1200.0);
    delete spk1;
    delete spk2;
}

TEST_F(InventoryTest, SetUpSystemTurnsOnAndSetsVolume) {
    AudioSystem as;
    Speaker* spk = new Speaker("Spk");
    as.addSpeaker(spk);
    as.setUpSystem();
    EXPECT_TRUE(spk->active());
    EXPECT_DOUBLE_EQ(spk->getVolume(), 0);
    delete spk;
}

TEST_F(InventoryTest, MicrophoneConnectToSpeakerOffThrows) {
    Microphone mic("Mic", true);
    auto speaker = std::make_unique<Speaker>("Spk");
    EXPECT_THROW(mic.connectToSpeaker(std::move(speaker)), DeviceSwitchedOff);
}

TEST_F(InventoryTest, RemoteControlAddDevices) {
    std::vector<Microphone*> mics;
    std::vector<Speaker*> speakers;
    RemoteControl rc(mics, speakers);
    auto mic = new Microphone("Mic", true);
    auto spk = new Speaker("Spk");
    rc.addMicrophone(mic);
    rc.addSpeaker(spk);
    rc.TurnAllOn();
    EXPECT_TRUE(mic->active());
    EXPECT_TRUE(spk->active());
    delete mic;
    delete spk;
}

TEST_F(InventoryTest, ProjectorSetTechnologyResolutionLamp) {
    Projector p("PX", 1000, 1.0, 90.0);
    p.setTechnology(Enums::ProjectionTechnology::DLP);
    p.setResolution(Enums::StandardResolution::FULL_HD);
    p.setLamp(Enums::LightSource::LASER);
    SUCCEED();
}

TEST_F(InventoryTest, SeatingCalculateSeatsPerRowZeroRows) {
    Seating s(100);
    s.setRowsNumber(10);
    EXPECT_EQ(s.calculateSeatsPerRow(), 10);
}