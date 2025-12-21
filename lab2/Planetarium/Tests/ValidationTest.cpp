#include <gtest/gtest.h>
#include "TimeValidator.h"
#include "StringValidator.h"

class ValidationTest : public ::testing::Test{
    void SetUp() override{

    }
    void TearDown() override{

    }
};

TEST_F(ValidationTest, getCurrentYear) {
    int year = TimeValidator::getCurrentYear();
    EXPECT_GE(year, 2020);
    EXPECT_LE(year, 2100);
}

TEST_F(ValidationTest, isLeapYear) {
    EXPECT_TRUE(TimeValidator::isLeapYear(2024));
    EXPECT_FALSE(TimeValidator::isLeapYear(2023));
    EXPECT_FALSE(TimeValidator::isLeapYear(1900));
    EXPECT_TRUE(TimeValidator::isLeapYear(2000));
}

TEST_F(ValidationTest, getDaysInMonth) {
    EXPECT_EQ(TimeValidator::getDaysInMonth(1), 31);
    EXPECT_EQ(TimeValidator::getDaysInMonth(2), 28);
    EXPECT_EQ(TimeValidator::getDaysInMonth(2, 2024), 29);
    EXPECT_EQ(TimeValidator::getDaysInMonth(4), 30);
    EXPECT_EQ(TimeValidator::getDaysInMonth(13), 0);
}

TEST_F(ValidationTest, stringToInt) {
    EXPECT_EQ(TimeValidator::stringToInt("123"), 123);
    EXPECT_EQ(TimeValidator::stringToInt("-1"), -1);
    EXPECT_EQ(TimeValidator::stringToInt("abc"), -1);
    EXPECT_EQ(TimeValidator::stringToInt(""), -1);
}

TEST_F(ValidationTest, isValidHourString) {
    EXPECT_TRUE(TimeValidator::isValidHour("0"));
    EXPECT_TRUE(TimeValidator::isValidHour("23"));
    EXPECT_FALSE(TimeValidator::isValidHour("24"));
    EXPECT_FALSE(TimeValidator::isValidHour("-1"));
    EXPECT_FALSE(TimeValidator::isValidHour("abc"));
}

TEST_F(ValidationTest, isValidHourInt) {
    EXPECT_TRUE(TimeValidator::isValidHour(0));
    EXPECT_TRUE(TimeValidator::isValidHour(23));
    EXPECT_FALSE(TimeValidator::isValidHour(24));
    EXPECT_FALSE(TimeValidator::isValidHour(-1));
}

TEST_F(ValidationTest, isValidMinuteString) {
    EXPECT_TRUE(TimeValidator::isValidMinute("0"));
    EXPECT_TRUE(TimeValidator::isValidMinute("59"));
    EXPECT_FALSE(TimeValidator::isValidMinute("60"));
    EXPECT_FALSE(TimeValidator::isValidMinute("-1"));
    EXPECT_FALSE(TimeValidator::isValidMinute("abc"));
}

TEST_F(ValidationTest, isValidMinuteInt) {
    EXPECT_TRUE(TimeValidator::isValidMinute(0));
    EXPECT_TRUE(TimeValidator::isValidMinute(59));
    EXPECT_FALSE(TimeValidator::isValidMinute(60));
    EXPECT_FALSE(TimeValidator::isValidMinute(-1));
}

TEST_F(ValidationTest, isValidSecondString) {
    EXPECT_TRUE(TimeValidator::isValidSecond("0"));
    EXPECT_TRUE(TimeValidator::isValidSecond("59"));
    EXPECT_FALSE(TimeValidator::isValidSecond("60"));
    EXPECT_FALSE(TimeValidator::isValidSecond("-1"));
    EXPECT_FALSE(TimeValidator::isValidSecond("abc"));
}

TEST_F(ValidationTest, isValidSecondInt) {
    EXPECT_TRUE(TimeValidator::isValidSecond(0));
    EXPECT_TRUE(TimeValidator::isValidSecond(59));
    EXPECT_FALSE(TimeValidator::isValidSecond(60));
    EXPECT_FALSE(TimeValidator::isValidSecond(-1));
}

TEST_F(ValidationTest, isValidMonthString) {
    EXPECT_TRUE(TimeValidator::isValidMonth("1"));
    EXPECT_TRUE(TimeValidator::isValidMonth("12"));
    EXPECT_FALSE(TimeValidator::isValidMonth("0"));
    EXPECT_FALSE(TimeValidator::isValidMonth("13"));
    EXPECT_FALSE(TimeValidator::isValidMonth("abc"));
}

TEST_F(ValidationTest, isValidMonthInt) {
    EXPECT_TRUE(TimeValidator::isValidMonth(1));
    EXPECT_TRUE(TimeValidator::isValidMonth(12));
    EXPECT_FALSE(TimeValidator::isValidMonth(0));
    EXPECT_FALSE(TimeValidator::isValidMonth(13));
}

TEST_F(ValidationTest, isValidDayString) {
    EXPECT_TRUE(TimeValidator::isValidDay("15", 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDay("32", 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDay("29", 2, 2023));
    EXPECT_TRUE(TimeValidator::isValidDay("29", 2, 2024));
    EXPECT_FALSE(TimeValidator::isValidDay("abc", 1, 2023));
}

TEST_F(ValidationTest, isValidDayInt) {
    EXPECT_TRUE(TimeValidator::isValidDay(15, 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDay(32, 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDay(29, 2, 2023));
    EXPECT_TRUE(TimeValidator::isValidDay(29, 2, 2024));
    EXPECT_TRUE(TimeValidator::isValidDay(10, -1, 2023));
    EXPECT_FALSE(TimeValidator::isValidDay(0, 1, 2023));
}

TEST_F(ValidationTest, isValidYearString) {
    int currentYear = TimeValidator::getCurrentYear();
    EXPECT_TRUE(TimeValidator::isValidYear(std::to_string(currentYear)));
    EXPECT_TRUE(TimeValidator::isValidYear(std::to_string(currentYear + 50), 1900, 100));
    EXPECT_FALSE(TimeValidator::isValidYear(std::to_string(currentYear + 150)));
    EXPECT_FALSE(TimeValidator::isValidYear("abc"));
}

TEST_F(ValidationTest, isValidYearInt) {
    int currentYear = TimeValidator::getCurrentYear();
    EXPECT_TRUE(TimeValidator::isValidYear(currentYear));
    EXPECT_FALSE(TimeValidator::isValidYear(currentYear + 50));
    EXPECT_FALSE(TimeValidator::isValidYear(currentYear + 150));
    EXPECT_FALSE(TimeValidator::isValidYear(1899));
}

TEST_F(ValidationTest, isValidTimeWithSecond) {
    EXPECT_TRUE(TimeValidator::isValidTime(12, 30, 45));
    EXPECT_FALSE(TimeValidator::isValidTime(25, 30, 45));
    EXPECT_FALSE(TimeValidator::isValidTime(12, 60, 45));
    EXPECT_FALSE(TimeValidator::isValidTime(12, 30, 60));
}

TEST_F(ValidationTest, isValidTimeWithoutSecond) {
    EXPECT_TRUE(TimeValidator::isValidTime(12, 30));
    EXPECT_FALSE(TimeValidator::isValidTime(25, 30));
    EXPECT_FALSE(TimeValidator::isValidTime(12, 60));
}

TEST_F(ValidationTest, isValidDate) {
    EXPECT_TRUE(TimeValidator::isValidDate(15, 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDate(29, 2, 2023));
    EXPECT_TRUE(TimeValidator::isValidDate(29, 2, 2024));
    EXPECT_FALSE(TimeValidator::isValidDate(32, 7, 2023));
    EXPECT_FALSE(TimeValidator::isValidDate(15, 13, 2023));
}

TEST_F(ValidationTest, isValidDateTime) {
    EXPECT_TRUE(TimeValidator::isValidDateTime(15, 7, 2023, 12, 30, 45));
    EXPECT_FALSE(TimeValidator::isValidDateTime(29, 2, 2023, 12, 30, 45));
    EXPECT_FALSE(TimeValidator::isValidDateTime(15, 7, 2023, 25, 30, 45));
}

TEST_F(ValidationTest, isValidCharacter) {
    EXPECT_TRUE(StringValidator::isValidCharacter('A'));
    EXPECT_TRUE(StringValidator::isValidCharacter('z'));
    EXPECT_TRUE(StringValidator::isValidCharacter('5'));
    EXPECT_TRUE(StringValidator::isValidCharacter('-'));
    EXPECT_TRUE(StringValidator::isValidCharacter('\''));
    EXPECT_TRUE(StringValidator::isValidCharacter(' '));
    EXPECT_TRUE(StringValidator::isValidCharacter('.'));
    EXPECT_FALSE(StringValidator::isValidCharacter('!'));
    EXPECT_FALSE(StringValidator::isValidCharacter('@'));
}

TEST_F(ValidationTest, validate) {
    EXPECT_TRUE(StringValidator::validate("Hello World"));
    EXPECT_TRUE(StringValidator::validate("Test-Case"));
    EXPECT_TRUE(StringValidator::validate("O'Neill"));
    EXPECT_TRUE(StringValidator::validate("Dr. Smith"));
    EXPECT_TRUE(StringValidator::validate("123 ABC"));
    EXPECT_FALSE(StringValidator::validate(""));
    EXPECT_FALSE(StringValidator::validate("Hello!"));
    EXPECT_FALSE(StringValidator::validate("Test@Case"));
}