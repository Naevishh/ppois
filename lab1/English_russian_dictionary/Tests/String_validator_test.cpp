#include <gtest/gtest.h>
#include <string>
#include <stdexcept>
#include "String_validator.h"

using namespace std;

class StringValidatorTest : public ::testing::Test {
protected:
    void SetUp() override {

        validEnglishWord = "hello";
        validEnglishWordWithApostrophe = "don't";
        validEnglishWordWithHyphen = "state-of-the-art";
        invalidEnglishWordWithNumber = "hello123";
        invalidEnglishWordWithSpecialChar = "hello@world";

        validRussianWord = "привет";
        validRussianWordYo = "ёлка";
        validRussianWordWithApostrophe = "кто-то";
        validRussianWordWithHyphen = "северо-запад";
        invalidRussianWordWithLatin = "приветhello";
        invalidRussianWordWithNumber = "привет123";

        shortWord = "a";
        longWord = "supercalifragilisticexpialidocioussuperlongword";
        normalWord = "normal";

        stringWithSpaces = "   hello world  ";
        stringWithTabs = "\t\ttest\t\t";
        stringWithNewlines = "\n\nstring\n\n";
        stringOnlySpaces = "     ";
        emptyString = "";
    }

    void TearDown() override {
        // Очистка при необходимости
    }

    string validEnglishWord;
    string validEnglishWordWithApostrophe;
    string validEnglishWordWithHyphen;
    string invalidEnglishWordWithNumber;
    string invalidEnglishWordWithSpecialChar;

    string validRussianWord;
    string validRussianWordYo;
    string validRussianWordWithApostrophe;
    string validRussianWordWithHyphen;
    string invalidRussianWordWithLatin;
    string invalidRussianWordWithNumber;

    string shortWord;
    string longWord;
    string normalWord;

    string stringWithSpaces;
    string stringWithTabs;
    string stringWithNewlines;
    string stringOnlySpaces;
    string emptyString;
};

TEST_F(StringValidatorTest, ValidEnglishWord_ValidWords) {
    EXPECT_TRUE(string_validator::valid_english_word(validEnglishWord));
    EXPECT_TRUE(string_validator::valid_english_word(validEnglishWordWithApostrophe));
    EXPECT_TRUE(string_validator::valid_english_word(validEnglishWordWithHyphen));
    EXPECT_TRUE(string_validator::valid_english_word("TEST"));
    EXPECT_TRUE(string_validator::valid_english_word("McDonald's"));
}

TEST_F(StringValidatorTest, ValidEnglishWord_InvalidCharacters) {
    EXPECT_FALSE(string_validator::valid_english_word(invalidEnglishWordWithNumber));
    EXPECT_FALSE(string_validator::valid_english_word(invalidEnglishWordWithSpecialChar));
    EXPECT_FALSE(string_validator::valid_english_word("hello!"));
    EXPECT_FALSE(string_validator::valid_english_word("hello.world"));
    EXPECT_FALSE(string_validator::valid_english_word("hello world"));
}

TEST_F(StringValidatorTest, ValidEnglishWord_BoundaryLength) {
    EXPECT_TRUE(string_validator::valid_english_word(shortWord));
    EXPECT_TRUE(string_validator::valid_english_word(normalWord));

    string maxLengthWord(50, 'a');
    EXPECT_TRUE(string_validator::valid_english_word(maxLengthWord));

    string tooLongWord(51, 'a');
    EXPECT_FALSE(string_validator::valid_english_word(tooLongWord));
}

TEST_F(StringValidatorTest, ValidEnglishWord_EmptyString) {
    EXPECT_FALSE(string_validator::valid_english_word(emptyString));
}

TEST_F(StringValidatorTest, ValidRussianWord_ValidWords) {
    EXPECT_TRUE(string_validator::valid_russian_word(validRussianWord));
    EXPECT_TRUE(string_validator::valid_russian_word(validRussianWordYo));
    EXPECT_TRUE(string_validator::valid_russian_word(validRussianWordWithApostrophe));
    EXPECT_TRUE(string_validator::valid_russian_word(validRussianWordWithHyphen));
    EXPECT_TRUE(string_validator::valid_russian_word("ПРИВЕТ"));
    EXPECT_TRUE(string_validator::valid_russian_word("привет"));
    EXPECT_TRUE(string_validator::valid_russian_word("Привет"));
}

TEST_F(StringValidatorTest, ValidRussianWord_InvalidCharacters) {
    EXPECT_FALSE(string_validator::valid_russian_word(invalidRussianWordWithLatin));
    EXPECT_FALSE(string_validator::valid_russian_word(invalidRussianWordWithNumber));
    EXPECT_FALSE(string_validator::valid_russian_word("привет!"));
    EXPECT_FALSE(string_validator::valid_russian_word("привет.мир"));
    EXPECT_FALSE(string_validator::valid_russian_word("привет мир"));
}

TEST_F(StringValidatorTest, ValidRussianWord_BoundaryLength) {
    EXPECT_TRUE(string_validator::valid_russian_word("я"));
    EXPECT_TRUE(string_validator::valid_russian_word(validRussianWord));

    string maxLengthWord;
    for (int i = 0; i < 50; ++i) {
        maxLengthWord += "а";
    }
    EXPECT_TRUE(string_validator::valid_russian_word(maxLengthWord));

    string tooLongWord;
    for (int i = 0; i < 51; ++i) {
        tooLongWord += "а";
    }
    EXPECT_FALSE(string_validator::valid_russian_word(tooLongWord));
}

TEST_F(StringValidatorTest, ValidRussianWord_EmptyString) {
    EXPECT_FALSE(string_validator::valid_russian_word(emptyString));
}

TEST_F(StringValidatorTest, IsCorrectLength_ValidLengths) {
    EXPECT_TRUE(string_validator::is_correct_length(shortWord));
    EXPECT_TRUE(string_validator::is_correct_length(normalWord));

    string boundaryWord(50, 'a');
    EXPECT_TRUE(string_validator::is_correct_length(boundaryWord));
}

TEST_F(StringValidatorTest, IsCorrectLength_InvalidLengths) {
    EXPECT_FALSE(string_validator::is_correct_length(emptyString));
    EXPECT_TRUE(string_validator::is_correct_length(longWord));

    string tooLongWord(51, 'a');
    EXPECT_FALSE(string_validator::is_correct_length(tooLongWord));
}


TEST_F(StringValidatorTest, ToLower_BasicFunctionality) {
    EXPECT_EQ(string_validator::to_lower("HELLO"), "hello");
    EXPECT_EQ(string_validator::to_lower("Hello"), "hello");
    EXPECT_EQ(string_validator::to_lower("hElLo"), "hello");
    EXPECT_EQ(string_validator::to_lower("hello"), "hello");
}

TEST_F(StringValidatorTest, ToLower_WithMixedCharacters) {
    EXPECT_EQ(string_validator::to_lower("Hello World!"), "hello world!");
    EXPECT_EQ(string_validator::to_lower("Test123"), "test123");
    EXPECT_EQ(string_validator::to_lower("ABCdef"), "abcdef");
}

TEST_F(StringValidatorTest, ToLower_EmptyString) {
    EXPECT_EQ(string_validator::to_lower(emptyString), emptyString);
}

TEST_F(StringValidatorTest, ToLower_RussianLetters) {
    EXPECT_EQ(string_validator::to_lower("ПРИВЕТ"), "привет");
    EXPECT_EQ(string_validator::to_lower("Привет"), "привет");
    EXPECT_EQ(string_validator::to_lower("приВЕт"), "привет");
}

TEST_F(StringValidatorTest, ToLower_SpecialCharacters) {
    EXPECT_EQ(string_validator::to_lower("DON'T"), "don't");
    EXPECT_EQ(string_validator::to_lower("STATE-OF-THE-ART"), "state-of-the-art");
    EXPECT_EQ(string_validator::to_lower("TEST@EMAIL.COM"), "test@email.com");
}

TEST_F(StringValidatorTest, RemoveSpaces_BasicFunctionality) {
    string test1 = stringWithSpaces;
    string_validator::remove_spaces(test1);
    EXPECT_EQ(test1, "hello world");

    string test2 = stringWithTabs;
    string_validator::remove_spaces(test2);
    EXPECT_EQ(test2, "test");

    string test3 = stringWithNewlines;
    string_validator::remove_spaces(test3);
    EXPECT_EQ(test3, "string");
}

TEST_F(StringValidatorTest, RemoveSpaces_NoSpaces) {
    string test1 = validEnglishWord;
    string_validator::remove_spaces(test1);
    EXPECT_EQ(test1, validEnglishWord);

    string test2 = "hello";
    string_validator::remove_spaces(test2);
    EXPECT_EQ(test2, "hello");
}

TEST_F(StringValidatorTest, RemoveSpaces_OnlySpaces) {
    string test1 = stringOnlySpaces;
    string_validator::remove_spaces(test1);
    EXPECT_EQ(test1, "");

    string test2 = "\t\n\r ";
    string_validator::remove_spaces(test2);
    EXPECT_EQ(test2, "");
}

TEST_F(StringValidatorTest, RemoveSpaces_EmptyString) {
    string test = emptyString;
    string_validator::remove_spaces(test);
    EXPECT_EQ(test, "");
}

TEST_F(StringValidatorTest, RemoveSpaces_MixedWhitespace) {
    string test1 = "  \t\nhello \t\nworld  \t\n";
    string_validator::remove_spaces(test1);
    EXPECT_EQ(test1, "hello \t\nworld");

    string test2 = "  test  case  ";
    string_validator::remove_spaces(test2);
    EXPECT_EQ(test2, "test  case");
}

TEST_F(StringValidatorTest, WordPairInput_ValidInput) {
    auto result = string_validator::word_pair_input("hello привет");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "привет");

    result = string_validator::word_pair_input("  test   тест  ");
    EXPECT_EQ(result.first, "test");
    EXPECT_EQ(result.second, "тест");

    result = string_validator::word_pair_input("don't нельзя");
    EXPECT_EQ(result.first, "don't");
    EXPECT_EQ(result.second, "нельзя");
}

TEST_F(StringValidatorTest, WordPairInput_WithMultipleSpaces) {
    auto result = string_validator::word_pair_input("   hello    привет   ");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "привет");

    result = string_validator::word_pair_input("word \t\tслово");
    EXPECT_EQ(result.first, "word");
    EXPECT_EQ(result.second, "слово");
}

TEST_F(StringValidatorTest, WordPairInput_InvalidEnglishWord) {
    EXPECT_THROW(string_validator::word_pair_input("hello123 привет"), invalid_argument);
    EXPECT_THROW(string_validator::word_pair_input("hel!lo привет"), invalid_argument);
}

TEST_F(StringValidatorTest, WordPairInput_InvalidRussianWord) {
    auto result = string_validator::word_pair_input("hello привет123");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "");

    result = string_validator::word_pair_input("test тест!");
    EXPECT_EQ(result.first, "test");
    EXPECT_EQ(result.second, "");
}

TEST_F(StringValidatorTest, WordPairInput_EmptyString) {
    EXPECT_THROW(string_validator::word_pair_input(emptyString), invalid_argument);
    EXPECT_THROW(string_validator::word_pair_input("   "), invalid_argument);
}

TEST_F(StringValidatorTest, WordPairInput_OnlyOneWord) {
    auto result = string_validator::word_pair_input("hello");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "");

    result = string_validator::word_pair_input("  hello  ");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "");
}

TEST_F(StringValidatorTest, WordPairInput_CaseConversion) {
    auto result = string_validator::word_pair_input("HELLO ПРИВЕТ");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "привет");

    result = string_validator::word_pair_input("Hello Привет");
    EXPECT_EQ(result.first, "hello");
    EXPECT_EQ(result.second, "привет");
}

TEST_F(StringValidatorTest, WordPairInput_SpecialCharactersAllowed) {
    auto result = string_validator::word_pair_input("state-of-the-art состояние-дел-искусства");
    EXPECT_EQ(result.first, "state-of-the-art");
}

TEST_F(StringValidatorTest, EdgeCases_MinimumLengthWords) {
    auto result = string_validator::word_pair_input("a б");
    EXPECT_EQ(result.first, "a");
    EXPECT_EQ(result.second, "б");
}

TEST_F(StringValidatorTest, EdgeCases_MaximumLengthWords) {
    string english(50, 'a');
    string russian;
    for (int i = 0; i < 50; ++i) {
        russian += "б";
    }
    string input = english + " " + russian;

    auto result = string_validator::word_pair_input(input);
    EXPECT_EQ(result.first, english);
    EXPECT_EQ(result.second, russian);
}

TEST_F(StringValidatorTest, EdgeCases_JustOverMaximumLength) {
    string english(51, 'a');
    string russian;
    for (int i = 0; i < 50; ++i) {
        russian += "б";
    }
    string input = english + " " + russian;

    EXPECT_THROW(string_validator::word_pair_input(input), invalid_argument);
}

TEST_F(StringValidatorTest, IntegrationTest_CompleteWorkflow) {

    string input = "  HeLLo-WorlD   ПрИвЕт-Мир  ";

    auto wordPair = string_validator::word_pair_input(input);

    EXPECT_EQ(wordPair.first, "hello-world");

    EXPECT_TRUE(string_validator::valid_english_word(wordPair.first));
}

TEST_F(StringValidatorTest, Performance_LargeInput) {
    string largeEnglish(1000, 'a');
    string largeRussian;
    for (int i = 0; i < 1000; ++i) {
        largeRussian += "б";
    }
    string input = largeEnglish + " " + largeRussian;

    EXPECT_THROW(string_validator::word_pair_input(input), invalid_argument);
}

TEST_F(StringValidatorTest, ToLower_RussianEdgeCases) {
    EXPECT_EQ(string_validator::to_lower("Ё"), "ё");
    EXPECT_EQ(string_validator::to_lower("Й"), "й");
    EXPECT_EQ(string_validator::to_lower("Ъ"), "ъ");

    EXPECT_EQ(string_validator::to_lower("HelloПРИВЕТ"), "helloпривет");
    EXPECT_EQ(string_validator::to_lower("TestТест"), "testтест");
}

TEST_F(StringValidatorTest, ToLower_InvalidUTF8Sequences) {
    std::string incomplete = "при";
    incomplete.pop_back();
    std::string result = string_validator::to_lower(incomplete);
    EXPECT_FALSE(result.empty());
}

