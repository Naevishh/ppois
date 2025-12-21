#include <gtest/gtest.h>
#include <string>
#include <stdexcept>
#include <ctime>
#include "Weather.h"
#include "MyTime.h"
#include "Date.h"

class UtilsTest : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(UtilsTest, ParameterizedConstructorValidWeather) {
    Weather w1(Enums::WeatherCondition::SUNNY);
    Weather w2(Enums::WeatherCondition::CLOUDY);
    Weather w3(Enums::WeatherCondition::HAZY);
    EXPECT_EQ(w1.getWeatherCondition(), Enums::WeatherCondition::SUNNY);
    EXPECT_EQ(w2.getWeatherCondition(), Enums::WeatherCondition::CLOUDY);
    EXPECT_EQ(w3.getWeatherCondition(), Enums::WeatherCondition::HAZY);
}

TEST_F(UtilsTest, GetWeatherByIndexValidIndex) {
    EXPECT_EQ(Weather::getWeatherByIndex(0), Enums::WeatherCondition::SUNNY);
    EXPECT_EQ(Weather::getWeatherByIndex(1), Enums::WeatherCondition::CLOUDY);
    EXPECT_EQ(Weather::getWeatherByIndex(8), Enums::WeatherCondition::HAZY);
}

TEST_F(UtilsTest, GetWeatherByIndexInvalidIndex) {
    EXPECT_EQ(Weather::getWeatherByIndex(100), Enums::WeatherCondition::SUNNY);
    EXPECT_EQ(Weather::getWeatherByIndex(9), Enums::WeatherCondition::SUNNY);
}

TEST_F(UtilsTest, GetWeatherCondition) {
    Weather w;
    auto cond = w.getWeatherCondition();
    std::vector<Enums::WeatherCondition> all = {
            Enums::WeatherCondition::SUNNY,
            Enums::WeatherCondition::CLOUDY,
            Enums::WeatherCondition::PARTLY_CLOUDY,
            Enums::WeatherCondition::RAINY,
            Enums::WeatherCondition::STORMY,
            Enums::WeatherCondition::SNOWY,
            Enums::WeatherCondition::FOGGY,
            Enums::WeatherCondition::WINDY,
            Enums::WeatherCondition::HAZY
    };
    bool found = false;
    for (auto c : all) {
        if (cond == c) {
            found = true;
            break;
        }
    }
    EXPECT_TRUE(found);
}

TEST_F(UtilsTest, DefaultConstructor) {
    MyTime t;
    EXPECT_GE(t.getHours(), 0);
    EXPECT_LE(t.getHours(), 23);
    EXPECT_GE(t.getMinutes(), 0);
    EXPECT_LE(t.getMinutes(), 59);
    EXPECT_GE(t.getSeconds(), 0);
    EXPECT_LE(t.getSeconds(), 59);
}

TEST_F(UtilsTest, ParameterizedConstructorValid) {
    MyTime t(12, 30, 45);
    EXPECT_EQ(t.getHours(), 12);
    EXPECT_EQ(t.getMinutes(), 30);
    EXPECT_EQ(t.getSeconds(), 45);
}

TEST_F(UtilsTest, ParameterizedConstructorInvalid) {
    EXPECT_THROW(MyTime(25, 0, 0), std::invalid_argument);
    EXPECT_THROW(MyTime(0, 60, 0), std::invalid_argument);
    EXPECT_THROW(MyTime(0, 0, 60), std::invalid_argument);
}

TEST_F(UtilsTest, GetTime) {
    MyTime t(5, 9, 3);
    EXPECT_EQ(t.getTime(), "05:09:03");
    MyTime t2(12, 30, 45);
    EXPECT_EQ(t2.getTime(), "12:30:45");
}

TEST_F(UtilsTest, EqualityOperatorsTime) {
    MyTime t1(10, 20, 30);
    MyTime t2(10, 20, 30);
    MyTime t3(11, 0, 0);
    EXPECT_TRUE(t1 == t2);
    EXPECT_FALSE(t1 == t3);
    EXPECT_TRUE(t1 < t3);
    EXPECT_TRUE(t3 > t1);
    EXPECT_TRUE(t1 <= t2);
    EXPECT_TRUE(t1 <= t3);
    EXPECT_TRUE(t3 >= t1);
    EXPECT_TRUE(t2 >= t1);
}

TEST_F(UtilsTest, GetCurrentTime) {
    MyTime t = MyTime::getCurrentTime();
    EXPECT_GE(t.getHours(), 0);
    EXPECT_LE(t.getHours(), 23);
}

TEST_F(UtilsTest, ConstructorValid) {
    Date d(2023, 12, 25);
    EXPECT_EQ(d.getDate(), "25.12.2023");
}

TEST_F(UtilsTest, ConstructorInvalid) {
    EXPECT_THROW(Date(2023, 13, 1), std::invalid_argument);
    EXPECT_THROW(Date(2023, 2, 30), std::invalid_argument);
    EXPECT_THROW(Date(2023, 0, 1), std::invalid_argument);
}

TEST_F(UtilsTest, GetDate) {
    Date d(2022, 5, 7);
    EXPECT_EQ(d.getDate(), "07.05.2022");
    Date d2(2022, 12, 15);
    EXPECT_EQ(d2.getDate(), "15.12.2022");
}

TEST_F(UtilsTest, GetWeather) {
    Date d(2023, 1, 1);
    auto w = d.getWeather();
    std::vector<Enums::WeatherCondition> all = {
            Enums::WeatherCondition::SUNNY,
            Enums::WeatherCondition::CLOUDY,
            Enums::WeatherCondition::PARTLY_CLOUDY,
            Enums::WeatherCondition::RAINY,
            Enums::WeatherCondition::STORMY,
            Enums::WeatherCondition::SNOWY,
            Enums::WeatherCondition::FOGGY,
            Enums::WeatherCondition::WINDY,
            Enums::WeatherCondition::HAZY
    };
    bool found = false;
    for (auto c : all) {
        if (w == c) {
            found = true;
            break;
        }
    }
    EXPECT_TRUE(found);
}

TEST_F(UtilsTest, EqualityOperatorsDate) {
    Date d1(2023, 5, 10);
    Date d2(2023, 5, 10);
    Date d3(2023, 6, 1);
    EXPECT_TRUE(d1 == d2);
    EXPECT_FALSE(d1 == d3);
    EXPECT_TRUE(d1 < d3);
    EXPECT_TRUE(d3 > d1);
    EXPECT_FALSE(d1 > d3);
    EXPECT_FALSE(d3 < d1);
}

TEST_F(UtilsTest, OperatorPlus) {
    Date d(2020, 6, 15);
    Date d2 = d + 5;
    EXPECT_EQ(d2.getDate(), "15.06.2025");
}

TEST_F(UtilsTest, Setters) {
    Date d(2020, 1, 1);
    d.setYear(2025);
    d.setMonth(12);
    d.setDay(31);
    EXPECT_EQ(d.getDate(), "31.12.2025");
}

TEST_F(UtilsTest, CurrentDate) {
    Date d = Date::currentDate();
    time_t now = time(nullptr);
    tm* local = localtime(&now);
    int expectedYear = local->tm_year + 1900;
    int expectedMonth = local->tm_mon + 1;
    int expectedDay = local->tm_mday;
    std::string expected = (expectedDay < 10 ? "0" : "") + std::to_string(expectedDay) + "." +
                           (expectedMonth < 10 ? "0" : "") + std::to_string(expectedMonth) + "." +
                           std::to_string(expectedYear);
    EXPECT_EQ(d.getDate().substr(6), expected.substr(6));
}
