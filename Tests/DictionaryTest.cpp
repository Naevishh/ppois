#include <gtest/gtest.h>
#include <sstream>
#include <fstream>
#include <cstdio>
#include "Dictionary.h"

class DictionaryTest : public ::testing::Test {
protected:
    void SetUp() override {
        dict1 += std::make_pair("apple", "яблоко");
        dict1 += std::make_pair("book", "книга");

        dict2 += std::make_pair("apple", "яблоко");
        dict2 += std::make_pair("book", "книга");

        empty_dict = dictionary();
    }

    void TearDown() override {

    }

    dictionary dict1;
    dictionary dict2;
    dictionary empty_dict;
};

TEST_F(DictionaryTest, ContainsWord_ExistingWord_ReturnsTrue) {
    EXPECT_TRUE(dict1.contains_word("apple"));
    EXPECT_TRUE(dict1.contains_word("book"));
}

TEST_F(DictionaryTest, ContainsWord_NonExistingWord_ReturnsFalse) {
    EXPECT_FALSE(dict1.contains_word("nonexistent"));
    EXPECT_FALSE(empty_dict.contains_word("anything"));
}

TEST_F(DictionaryTest, ContainsWord_EmptyDictionary_ReturnsFalse) {
    EXPECT_FALSE(empty_dict.contains_word("test"));
}

TEST_F(DictionaryTest, OperatorBracketGet_ExistingWord_ReturnsValue) {
    EXPECT_EQ(dict1["apple"], "яблоко");
    EXPECT_EQ(dict1["book"], "книга");
}

TEST_F(DictionaryTest, OperatorBracketGet_NonExistingWord_ThrowsException) {
    EXPECT_THROW(dict1["nonexistent"], std::exception);
    EXPECT_THROW(empty_dict["anything"], std::exception);
}

TEST_F(DictionaryTest, OperatorBracketSet_NewWord_AddsSuccessfully) {
    dict1 += std::make_pair("cat", "кошка");
    dict1["cat"] = "кот";
    EXPECT_TRUE(dict1.contains_word("cat"));
    EXPECT_EQ(dict1["cat"], "кот");
}

TEST_F(DictionaryTest, OperatorBracketSet_ExistingWord_UpdatesValue) {
    dict1["apple"] = "новое яблоко";
    EXPECT_EQ(dict1["apple"], "новое яблоко");
}

TEST_F(DictionaryTest, OperatorPlusEqualsStringPair_NewWord_AddsSuccessfully) {
    dictionary result = dict1 += std::make_pair("cat", "кот");
    EXPECT_TRUE(dict1.contains_word("cat"));
    EXPECT_EQ(dict1["cat"], "кот");
}

TEST_F(DictionaryTest, OperatorPlusEqualsStringPair_ExistingWord_ThrowsException) {
    EXPECT_THROW(dict1 += std::make_pair("apple", "другое яблоко"), std::invalid_argument);
}

TEST_F(DictionaryTest, OperatorPlusEqualsCharPair_NewWord_AddsSuccessfully) {
    dictionary result = dict1 += std::make_pair("dog", "собака");
    EXPECT_TRUE(dict1.contains_word("dog"));
    EXPECT_EQ(dict1["dog"], "собака");
}

TEST_F(DictionaryTest, OperatorPlusEqualsCharPair_ExistingWord_ThrowsException) {
    EXPECT_THROW(dict1 += std::make_pair("book", "другая книга"), std::invalid_argument);
}

TEST_F(DictionaryTest, OperatorMinusEquals_ExistingWord_RemovesSuccessfully) {
    dictionary result = dict1 -= "apple";
    EXPECT_FALSE(dict1.contains_word("apple"));
    EXPECT_TRUE(dict1.contains_word("book"));
}

TEST_F(DictionaryTest, OperatorMinusEquals_NonExistingWord_ThrowsException) {
    EXPECT_THROW(dict1 -= "nonexistent", std::invalid_argument);
}

TEST_F(DictionaryTest, OperatorMinusEquals_EmptyDictionary_ThrowsException) {
    EXPECT_THROW(empty_dict -= "anything", std::invalid_argument);
}

TEST_F(DictionaryTest, OperatorEquals_EqualDictionaries_ReturnsTrue) {
    EXPECT_TRUE(dict1 == dict2);
}

TEST_F(DictionaryTest, OperatorEquals_DifferentDictionaries_ReturnsFalse) {
    dict2 += std::make_pair("cat", "кот");
    EXPECT_FALSE(dict1 == dict2);
}

TEST_F(DictionaryTest, OperatorEquals_EmptyDictionaries_ReturnsTrue) {
    dictionary empty1, empty2;
    EXPECT_TRUE(empty1 == empty2);
}

TEST_F(DictionaryTest, OperatorEquals_OneEmptyOneNonEmpty_ReturnsFalse) {
    EXPECT_FALSE(dict1 == empty_dict);
    EXPECT_FALSE(empty_dict == dict1);
}

TEST_F(DictionaryTest, OperatorNotEquals_DifferentDictionaries_ReturnsTrue) {
    dict2 += std::make_pair("cat", "кот");
    EXPECT_TRUE(dict1 != dict2);
}

TEST_F(DictionaryTest, OperatorNotEquals_EqualDictionaries_ReturnsFalse) {
    EXPECT_FALSE(dict1 != dict2);
}

TEST_F(DictionaryTest, GetSize_NonEmptyDictionary_ReturnsCorrectSize) {
    EXPECT_EQ(dict1.get_size(), 2);

    dict1 += std::make_pair("cat", "кот");
    EXPECT_EQ(dict1.get_size(), 3);
}

TEST_F(DictionaryTest, GetSize_EmptyDictionary_ReturnsZero) {
    EXPECT_EQ(empty_dict.get_size(), 0);
}

TEST_F(DictionaryTest, GetSize_AfterRemoval_ReturnsCorrectSize) {
    dict1 -= "apple";
    EXPECT_EQ(dict1.get_size(), 1);

    dict1 -= "book";
    EXPECT_EQ(dict1.get_size(), 0);
}

TEST_F(DictionaryTest, IsEmpty_EmptyDictionary_ReturnsTrue) {
    EXPECT_TRUE(empty_dict.is_empty());
}

TEST_F(DictionaryTest, IsEmpty_NonEmptyDictionary_ReturnsFalse) {
    EXPECT_FALSE(dict1.is_empty());
}

TEST_F(DictionaryTest, IsEmpty_AfterClearing_ReturnsTrue) {
    dict1 -= "apple";
    dict1 -= "book";
    EXPECT_TRUE(dict1.is_empty());
}

TEST_F(DictionaryTest, OperatorOutputStream_NonEmptyDictionary_OutputsCorrectly) {
    std::stringstream ss;
    ss << dict1;

    std::string output = ss.str();
    EXPECT_FALSE(output.empty());
    EXPECT_NE(output.find("apple"), std::string::npos);
    EXPECT_NE(output.find("яблоко"), std::string::npos);
    EXPECT_NE(output.find("book"), std::string::npos);
    EXPECT_NE(output.find("книга"), std::string::npos);
}

TEST_F(DictionaryTest, OperatorOutputStream_EmptyDictionary_OutputsNothing) {
    std::stringstream ss;
    ss << empty_dict;

    EXPECT_TRUE(ss.str().empty());
}

TEST_F(DictionaryTest, OperatorInputStream_ValidData_ReadsSuccessfully) {
    std::stringstream input("apple яблоко\ncat кот\ndog собака");
    dictionary new_dict;
    input >> new_dict;

    EXPECT_EQ(new_dict.get_size(), 3);
    EXPECT_TRUE(new_dict.contains_word("apple"));
    EXPECT_TRUE(new_dict.contains_word("cat"));
    EXPECT_TRUE(new_dict.contains_word("dog"));
    EXPECT_EQ(new_dict["apple"], "яблоко");
    EXPECT_EQ(new_dict["cat"], "кот");
    EXPECT_EQ(new_dict["dog"], "собака");
}

TEST_F(DictionaryTest, OperatorInputStream_DuplicateWords_IgnoresDuplicates) {
    std::stringstream input("apple яблоко\napple другое_яблоко\ncat кот");
    dictionary new_dict;
    input >> new_dict;

    EXPECT_EQ(new_dict.get_size(), 2);
    EXPECT_EQ(new_dict["apple"], "яблоко");
}

TEST_F(DictionaryTest, OperatorInputStream_InvalidLines_SkipsInvalidData) {
    std::stringstream input("invalid_line\napple яблоко\nanother_invalid\ncat кот");
    dictionary new_dict;
    input >> new_dict;

    EXPECT_EQ(new_dict.get_size(), 2);
    EXPECT_TRUE(new_dict.contains_word("apple"));
    EXPECT_TRUE(new_dict.contains_word("cat"));
}

TEST_F(DictionaryTest, OperatorInputStream_EmptyLines_SkipsEmptyLines) {
    std::stringstream input("\n\napple яблоко\n\ncat кот\n\n");
    dictionary new_dict;
    input >> new_dict;

    EXPECT_EQ(new_dict.get_size(), 2);
    EXPECT_TRUE(new_dict.contains_word("apple"));
    EXPECT_TRUE(new_dict.contains_word("cat"));
}

TEST_F(DictionaryTest, ReadFromFile_ValidFile_ReadsSuccessfully) {
    const std::string test_filename = "test_dictionary.txt";
    std::ofstream test_file(test_filename);
    test_file << "apple яблоко\ncat кот\ndog собака\n";
    test_file.close();

    dictionary file_dict;
    file_dict.read_from_file(test_filename);

    EXPECT_EQ(file_dict.get_size(), 3);
    EXPECT_TRUE(file_dict.contains_word("apple"));
    EXPECT_TRUE(file_dict.contains_word("cat"));
    EXPECT_TRUE(file_dict.contains_word("dog"));

    std::remove(test_filename.c_str());
}

TEST_F(DictionaryTest, ReadFromFile_NonExistentFile_DoesNothing) {
    dictionary original_dict = dict1;
    int original_size = original_dict.get_size();

    original_dict.read_from_file("nonexistent_file.txt");

    EXPECT_EQ(original_dict.get_size(), original_size);
}

TEST_F(DictionaryTest, ReadFromFile_EmptyFile_RemainsEmpty) {
    const std::string test_filename = "empty_test.txt";
    std::ofstream test_file(test_filename);
    test_file.close();

    dictionary empty_dict;
    empty_dict.read_from_file(test_filename);

    EXPECT_TRUE(empty_dict.is_empty());

    std::remove(test_filename.c_str());
}

TEST_F(DictionaryTest, DataIntegrity_AfterMultipleOperations_ConsistentState) {
    dictionary test_dict;

    test_dict += std::make_pair("one", "один");
    test_dict += std::make_pair("two", "два");
    test_dict += std::make_pair("three", "два");
    test_dict["three"] = "три";

    EXPECT_EQ(test_dict.get_size(), 3);
    EXPECT_FALSE(test_dict.is_empty());

    EXPECT_TRUE(test_dict.contains_word("one"));
    EXPECT_TRUE(test_dict.contains_word("two"));
    EXPECT_TRUE(test_dict.contains_word("three"));

    test_dict -= "two";

    EXPECT_EQ(test_dict.get_size(), 2);
    EXPECT_FALSE(test_dict.contains_word("two"));
    EXPECT_TRUE(test_dict.contains_word("one"));
    EXPECT_TRUE(test_dict.contains_word("three"));

    test_dict["one"] = "единица";
    EXPECT_EQ(test_dict["one"], "единица");
}

TEST_F(DictionaryTest, EdgeCases_EmptyStringOperations) {
    dictionary test_dict;

    EXPECT_THROW(test_dict[""], std::exception);
    EXPECT_FALSE(test_dict.contains_word(""));
}

TEST_F(DictionaryTest, OperatorPlusEquals_DuplicateWordThrows) {
    EXPECT_THROW(dict1 += std::make_pair("apple", "яблоко"), std::invalid_argument);
}
