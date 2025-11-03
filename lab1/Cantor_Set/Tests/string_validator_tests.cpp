#include <gtest/gtest.h>
#include "string_validator.h"

class StringValidatorTest : public ::testing::Test {
protected:
    void SetUp() override {
        validator = string_validator();
    }

    string_validator validator;

    char test_get_next_char(const std::string& str, size_t index) {
        return validator.get_next_char(str, index);
    }

    bool test_process_character(char current, char next) {
        return validator.process_character(current, next);
    }

    bool test_is_allowed_character(char ch) {
        return validator.is_allowed_character(ch);
    }

    bool test_check_sequence_rules(char current, char next) {
        return validator.check_sequence_rules(current, next);
    }

    void test_update_brace_counters(char ch) {
        validator.update_brace_counters(ch);
    }

    int get_curly_braces() const { return validator.curly_braces_; }
    int get_angle_braces() const { return validator.angle_braces_; }
};

TEST_F(StringValidatorTest, Validate_EmptyString_ReturnsFalse) {
EXPECT_FALSE(validator.validate("", false));
EXPECT_FALSE(validator.validate("", true));
}

TEST_F(StringValidatorTest, Validate_InvalidFirstCharacter_ReturnsFalse) {
EXPECT_FALSE(validator.validate("invalid", false));
EXPECT_FALSE(validator.validate("atest", false));
EXPECT_FALSE(validator.validate("123", false));
EXPECT_FALSE(validator.validate(")test", false));
}

TEST_F(StringValidatorTest, Validate_ValidSimpleCurlyBraces_ReturnsTrue) {
EXPECT_TRUE(validator.validate("{a}", false));
EXPECT_TRUE(validator.validate("{a,b,c}", false));
}

TEST_F(StringValidatorTest, Validate_ValidSimpleAngleBraces_ReturnsTrue) {
EXPECT_TRUE(validator.validate("<a>", true));
EXPECT_TRUE(validator.validate("<a,b,c>", true));
}

TEST_F(StringValidatorTest, Validate_ValidNestedStructures_ReturnsTrue) {
EXPECT_TRUE(validator.validate("{<a>}", true));
EXPECT_TRUE(validator.validate("<{a}>", true));
EXPECT_TRUE(validator.validate("{a<b>c}", true));
}

TEST_F(StringValidatorTest, Validate_UnbalancedBraces_ReturnsFalse) {
EXPECT_FALSE(validator.validate("{a", false));
EXPECT_FALSE(validator.validate("<a", true));
EXPECT_FALSE(validator.validate("{a}}", false));
EXPECT_FALSE(validator.validate("<<a>", true));
}

TEST_F(StringValidatorTest, Validate_UnclosedBraces_ReturnsFalse) {
EXPECT_FALSE(validator.validate("{<a>", true));
EXPECT_FALSE(validator.validate("<{a}", true));
}

TEST_F(StringValidatorTest, Validate_SpacesAreIgnored_ReturnsTrue) {
EXPECT_TRUE(validator.validate("{ a }", false));
EXPECT_TRUE(validator.validate("< a >", true));
EXPECT_TRUE(validator.validate("{ a , b }", false));
}

TEST_F(StringValidatorTest, Validate_InvalidSequences_ReturnsFalse) {
EXPECT_FALSE(validator.validate("{{}", false));
EXPECT_FALSE(validator.validate("{,}", false));
EXPECT_FALSE(validator.validate("{>}", false));
EXPECT_FALSE(validator.validate("{}a", false));
EXPECT_FALSE(validator.validate("{}<", false));
EXPECT_FALSE(validator.validate("{}{", false));
EXPECT_FALSE(validator.validate("<,>", true));
EXPECT_FALSE(validator.validate("<>}", true));
EXPECT_FALSE(validator.validate("<>a", true));
EXPECT_FALSE(validator.validate("<><", true));
EXPECT_FALSE(validator.validate(",a", false));
}

TEST_F(StringValidatorTest, Validate_ConsecutiveLetters_ReturnsFalse) {
EXPECT_FALSE(validator.validate("{ab}", false));
EXPECT_FALSE(validator.validate("<xy>", true));
}

TEST_F(StringValidatorTest, Validate_InvalidCharacters_ReturnsFalse) {
EXPECT_FALSE(validator.validate("{A}", false));
EXPECT_FALSE(validator.validate("{1}", false));
EXPECT_FALSE(validator.validate("{!}", false));
EXPECT_FALSE(validator.validate("{@}", false));
}

TEST_F(StringValidatorTest, Validate_ComplexValidCases_ReturnsTrue) {
EXPECT_TRUE(validator.validate("{a,b,c}", false));
EXPECT_TRUE(validator.validate("{a<b>,c<d>}", true));
EXPECT_TRUE(validator.validate("<a{b,c}>", true));
}

TEST_F(StringValidatorTest, Validate_IsElementFlagBehavior) {
EXPECT_TRUE(validator.validate("{a}", false));
EXPECT_TRUE(validator.validate("{a}", true));

EXPECT_TRUE(validator.validate("<a>", true));

string_validator validator2;
EXPECT_TRUE(validator2.validate("{<a>}", true));
}

TEST_F(StringValidatorTest, SetRead_ValidString_ReturnsTrueAndModifiesString) {
std::string test1 = "{ a , b }";
std::string test2 = "< x , y >";

EXPECT_TRUE(string_validator::set_read(test1, false));
EXPECT_EQ(test1, "{ab}");

EXPECT_TRUE(string_validator::set_read(test2, true));
EXPECT_EQ(test2, "<xy>");
}

TEST_F(StringValidatorTest, SetRead_InvalidString_ReturnsFalseAndNoModification) {
std::string test1 = "invalid";
std::string original1 = test1;

std::string test2 = "{unclosed";
std::string original2 = test2;

EXPECT_FALSE(string_validator::set_read(test1, false));
EXPECT_EQ(test1, original1);

EXPECT_FALSE(string_validator::set_read(test2, false));
EXPECT_EQ(test2, original2);
}

TEST_F(StringValidatorTest, SetRead_RemovesSpacesAndCommas) {
std::string test1 = "{ a , b , c }";
std::string test2 = "< x , y , z >";

string_validator::set_read(test1, false);
string_validator::set_read(test2, true);

EXPECT_EQ(test1, "{abc}");
EXPECT_EQ(test2, "<xyz>");
}

TEST_F(StringValidatorTest, ProcessCharacter_Space_ReturnsTrue) {
EXPECT_TRUE(test_process_character(' ', 'a'));
}

TEST_F(StringValidatorTest, ProcessCharacter_InvalidChar_ReturnsFalse) {
EXPECT_FALSE(test_process_character('A', 'a'));
EXPECT_FALSE(test_process_character('1', '}'));
EXPECT_FALSE(test_process_character('!', ' '));
}

TEST_F(StringValidatorTest, ProcessCharacter_ValidChars_ReturnsTrue) {
EXPECT_TRUE(test_process_character('a', '}'));
EXPECT_TRUE(test_process_character('{', 'a'));
EXPECT_TRUE(test_process_character('}', ' '));
EXPECT_TRUE(test_process_character('<', 'a'));
EXPECT_TRUE(test_process_character('>', ' '));
EXPECT_TRUE(test_process_character(',', 'a'));
}

TEST_F(StringValidatorTest, IsAllowedCharacter_ValidChars_ReturnsTrue) {
EXPECT_TRUE(test_is_allowed_character('a'));
EXPECT_TRUE(test_is_allowed_character('z'));
EXPECT_TRUE(test_is_allowed_character('{'));
EXPECT_TRUE(test_is_allowed_character('}'));
EXPECT_TRUE(test_is_allowed_character('<'));
EXPECT_TRUE(test_is_allowed_character('>'));
EXPECT_TRUE(test_is_allowed_character(','));
}

TEST_F(StringValidatorTest, IsAllowedCharacter_InvalidChars_ReturnsFalse) {
EXPECT_FALSE(test_is_allowed_character('A'));
EXPECT_FALSE(test_is_allowed_character('Z'));
EXPECT_FALSE(test_is_allowed_character('1'));
EXPECT_FALSE(test_is_allowed_character('!'));
EXPECT_FALSE(test_is_allowed_character('@'));
EXPECT_FALSE(test_is_allowed_character('['));
EXPECT_FALSE(test_is_allowed_character(']'));
}

TEST_F(StringValidatorTest, CheckSequenceRules_InvalidSequences_ReturnsFalse) {
EXPECT_FALSE(test_check_sequence_rules('{', ','));
EXPECT_FALSE(test_check_sequence_rules('{', '>'));
EXPECT_FALSE(test_check_sequence_rules('}', 'a'));
EXPECT_FALSE(test_check_sequence_rules('}', '<'));
EXPECT_FALSE(test_check_sequence_rules('}', '{'));
EXPECT_FALSE(test_check_sequence_rules('<', ','));
EXPECT_FALSE(test_check_sequence_rules('<', '}'));
EXPECT_FALSE(test_check_sequence_rules('>', 'a'));
EXPECT_FALSE(test_check_sequence_rules('>', '<'));
EXPECT_FALSE(test_check_sequence_rules('>', '{'));
EXPECT_FALSE(test_check_sequence_rules(',', ','));
EXPECT_FALSE(test_check_sequence_rules(',', '}'));
EXPECT_FALSE(test_check_sequence_rules(',', '>'));
EXPECT_FALSE(test_check_sequence_rules('a', 'a'));
EXPECT_FALSE(test_check_sequence_rules('b', 'c'));
}

TEST_F(StringValidatorTest, CheckSequenceRules_ValidSequences_ReturnsTrue) {
EXPECT_TRUE(test_check_sequence_rules('{', 'a'));
EXPECT_TRUE(test_check_sequence_rules('{', '<'));
EXPECT_TRUE(test_check_sequence_rules('}', '}'));
EXPECT_TRUE(test_check_sequence_rules('}', '>'));
EXPECT_TRUE(test_check_sequence_rules('<', 'a'));
EXPECT_TRUE(test_check_sequence_rules('<', '{'));
EXPECT_TRUE(test_check_sequence_rules('>', '}'));
EXPECT_TRUE(test_check_sequence_rules('>', '>'));
EXPECT_TRUE(test_check_sequence_rules(',', 'a'));
EXPECT_TRUE(test_check_sequence_rules(',', '<'));
EXPECT_TRUE(test_check_sequence_rules('a', '}'));
EXPECT_TRUE(test_check_sequence_rules('a', '>'));
EXPECT_TRUE(test_check_sequence_rules('a', ','));
}

TEST_F(StringValidatorTest, UpdateBraceCounters) {
    test_update_brace_counters('{');
    EXPECT_EQ(get_curly_braces(), 1);
    EXPECT_EQ(get_angle_braces(), 0);

    test_update_brace_counters('<');
    EXPECT_EQ(get_curly_braces(), 1);
    EXPECT_EQ(get_angle_braces(), 1);

    test_update_brace_counters('}');
    EXPECT_EQ(get_curly_braces(), 0);
    EXPECT_EQ(get_angle_braces(), 1);

    test_update_brace_counters('>');
    EXPECT_EQ(get_curly_braces(), 0);
    EXPECT_EQ(get_angle_braces(), 0);

    test_update_brace_counters('a');
    EXPECT_EQ(get_curly_braces(), 0);
    EXPECT_EQ(get_angle_braces(), 0);

    test_update_brace_counters(',');
    EXPECT_EQ(get_curly_braces(), 0);
    EXPECT_EQ(get_angle_braces(), 0);
}

TEST_F(StringValidatorTest, GetNextChar_ValidIndex_ReturnsChar) {
std::string test = "abc";
EXPECT_EQ(test_get_next_char(test, 0), 'b');
EXPECT_EQ(test_get_next_char(test, 1), 'c');
}

TEST_F(StringValidatorTest, GetNextChar_LastIndex_ReturnsNull) {
std::string test = "abc";
EXPECT_EQ(test_get_next_char(test, 2), '\0');
EXPECT_EQ(test_get_next_char(test, 5), '\0');
}
