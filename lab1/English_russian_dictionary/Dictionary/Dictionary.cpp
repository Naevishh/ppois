#include <string>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include "Dictionary.h"
#include "string_validator.h"

std::ostream& operator<<(std::ostream& output, const dictionary& dict_to_print) {
    size_t counter = 0;
    dict_to_print.dictionary_tree.inorder_traverse(
            [&output, &counter](const std::string& english_word, const std::string& russian_word) {
                output << ++counter << ". " << english_word << " - " << russian_word << "\n";
            });
    return output;
}

std::istream& operator>>(std::istream& input, dictionary& dictionary){
    std::string current_line;
    while (std::getline(input, current_line)){
        if (!current_line.empty()){
            try {
                std::pair<std::string, std::string> new_pair = string_validator::word_pair_input(current_line);
                if (!dictionary.contains_word(new_pair.first)) dictionary+=new_pair;
            } catch (const std::invalid_argument& exception) {

            }
        }
    }
    return input;
}

bool dictionary::contains_word(const std::string& english_word) const{
    return dictionary_tree.contains_node(english_word);
}

const std::string& dictionary::operator[](const std::string& input_word) const {
    return dictionary_tree.get_value(input_word);
}

std::string& dictionary::operator[](const std::string& input_word) {
    return dictionary_tree.get_value(input_word);
}

dictionary& dictionary::operator+=(const std::pair<std::string, std::string>& english_russian_pair) {
    if (!dictionary_tree.insert_helper(english_russian_pair.first,english_russian_pair.second)) {
        throw std::invalid_argument("Слово уже существует в словаре");
    }
    return *this;
}

dictionary& dictionary::operator+=(const std::pair<const char*, const char*>& english_russian_pair) {
    if (!dictionary_tree.insert_helper(english_russian_pair.first,english_russian_pair.second)) {
        throw std::invalid_argument("Слово уже существует в словаре");
    }
    return *this;
}

dictionary& dictionary::operator-=(const std::string& english_word) {
    if (!dictionary_tree.delete_helper(english_word)) {
        throw std::invalid_argument("Слова не существует в словаре");
    }
    return *this;
}

bool dictionary::operator==(const dictionary& other) const {
    return other.dictionary_tree == this->dictionary_tree;
}

bool dictionary::operator!=(const dictionary& other) const {
    return !(*this == other);
}

int dictionary::get_size() const {
    return dictionary_tree.get_size();
}

bool dictionary::is_empty() const {
    return dictionary_tree.empty_tree();
}

void dictionary::read_from_file(const std::string& file_name) {
    std::ifstream txt_file(file_name);
    if (txt_file.is_open()) {
        txt_file >> *this;
        txt_file.close();
    }
}


