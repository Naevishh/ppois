#include "String_validator.h"
#include <string>
#include <stdexcept>
#include <cctype>

bool string_validator::valid_english_word(const std::string& english_word) {
    for (char symbol: english_word) {
        if (!std::isalpha(static_cast<unsigned char>(symbol))
            && symbol != '\'' && symbol != '-')
            return false;
    }
    return is_correct_length(english_word);
}

bool string_validator::valid_russian_word(const std::string& russian_word) {
    const std::string valid_chars =
            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            "'-";
    for (char character : russian_word) {
        if (valid_chars.find(character) == std::string::npos) {
            return false;
        }
    }
    return is_correct_length_rus(russian_word);
}

bool string_validator::is_correct_length(const std::string& input_word) {
    return (input_word.size() >= 1 && input_word.size() <= 50);
}

bool string_validator::is_correct_length_rus(const std::string& input_word) {
    return (input_word.size()/2 >= 1 && input_word.size()/2 <= 50);
}

std::string string_validator::to_lower(const std::string& input_string) {
    std::string result = input_string;
    for (size_t i = 0; i < result.length(); i++) {
        unsigned char c = result[i];
        if (c >= 'A' && c <= 'Z') {
            result[i] = c + 32;
        }
        else if (c == 0xD0 && i + 1 < result.length()) {
            unsigned char next = result[i + 1];

            if (next >= 0x90 && next <= 0x9F && next != 0x81) {
                result[i + 1] = next + 0x20;
                i++;
            }
            else if (next == 0x81) {
                result[i] = 0xD1;
                result[i + 1] = 0x91;
                i++;
            }
            else if (next >= 0xA0 && next <= 0xAF) {
                result[i] = 0xD1;
                result[i + 1] = next - 0x20;
                i++;
            }
        }
    }
    return result;
}

void string_validator::remove_spaces(std::string& input_string) {
    size_t start_index = input_string.find_first_not_of(" \t\n\r");
    size_t end_index = input_string.find_last_not_of(" \t\n\r");

    if (start_index == std::string::npos) {
        input_string = "";
    } else {
        input_string = input_string.substr(start_index, end_index - start_index + 1);
    }
}

std::string string_validator::extract_word(const std::string& input_line, std::string& word_to_extract){
    size_t start_index=input_line.find_first_not_of("'- \t\n\r");
    size_t end_index;
    if(input_line.find_first_of(' ',start_index)==std::string::npos){
        end_index=input_line.size()-1;
    } else {
        end_index=input_line.find_first_of(' ',start_index)-1;
    }
    word_to_extract=string_validator::to_lower(input_line.substr(start_index,
                                                                 end_index - start_index + 1));
    return input_line.substr(end_index+1);
}

std::pair<std::string, std::string> string_validator::word_pair_input(const std::string& input_line) {
    if (!input_line.empty() && input_line.find_first_not_of("-' \t\n\r")!=std::string::npos) {
        std::string english;
        std::string substrated_line = extract_word(input_line, english);
        if (!string_validator::valid_english_word(english)){
            throw std::invalid_argument("Слово введено неверно");
        }
        if(substrated_line.find_first_not_of("-' \t\n\r")==std::string::npos){
            return {english, ""};
        }
        std::string russian;
        std::string substrated_line_=extract_word(substrated_line,russian);
        if (!string_validator::valid_russian_word(russian)) russian = "";
        return {english, russian};
    } else {
        throw std::invalid_argument("Пустая строка");
    }
}


