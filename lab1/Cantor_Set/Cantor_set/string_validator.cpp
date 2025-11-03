#include "string_validator.h"
#include <vector>
#include <string>
#include <algorithm>


bool string_validator::validate(const std::string& input_string, bool is_element) {
    if (!is_element && input_string[0] == '<') return false;
    if (input_string[0] != '{' && input_string[0] != '<') return false;
    for (size_t i = 0; i < input_string.size(); i++) {
        if (!process_character(input_string[i], get_next_char(input_string, i))) {
            return false;
        }
        if (is_element) {
            if (curly_braces_ == 0 && angle_braces_ == 0) break;
        } else {
            if (curly_braces_ == 0) break;
        }
    }
    return curly_braces_ == 0 && angle_braces_ == 0;
}

bool string_validator::set_read(std::string& input_string, bool is_element) {
    if (string_validator().validate(input_string, is_element)) {
        input_string.erase(std::remove(input_string.begin(),input_string.end(), ' '),
                           input_string.end());
        input_string.erase(std::remove(input_string.begin(),input_string.end(), ','),
                           input_string.end());
        return true;
    } else return false;
}

char string_validator::get_next_char(const std::string& input_string, size_t index) {
    return (index + 1 < input_string.size()) ? input_string[index + 1] : '\0';
}

bool string_validator::process_character(char current_char, char next_char) {
    if (current_char == ' ') return true;
    if (!is_allowed_character(current_char)) return false;
    if (!check_sequence_rules(current_char, next_char)) return false;

    update_brace_counters(current_char);
    return true;
}

bool string_validator::is_allowed_character(char character) {
    static const std::string allowed = "{}<>,abcdefghijklmnopqrstuvwxyz";
    return allowed.find(character) != std::string::npos;
}

bool string_validator::check_sequence_rules(char current_char, char next_char) {
    const auto is_alpha = [](char character) { return character >= 'a' && character <= 'z'; };
    const std::vector<std::pair<char, std::string>> invalid_sequences = {
            {'{', ",>"},
            {'}', "a<{"},
            {'<', ",}"},
            {'>', "a<{"},
            {',', ",}>"}
    };

    for (const auto& [rule_char, invalid_next] : invalid_sequences) {
        if (current_char == rule_char && invalid_next.find(next_char) != std::string::npos) {
            return false;
        }
    }

    return !(is_alpha(current_char) && is_alpha(next_char));
}

void string_validator::update_brace_counters(char character) {
    switch (character) {
        case '{': curly_braces_++; break;
        case '}': curly_braces_--; break;
        case '<': angle_braces_++; break;
        case '>': angle_braces_--; break;
        default: break;
    }
}