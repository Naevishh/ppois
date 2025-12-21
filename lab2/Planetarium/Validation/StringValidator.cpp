#include "StringValidator.h"

bool StringValidator::validate(const std::string& text) {
    if (text.empty()) {
        return false;
    }

    for (char c : text) {
        if (!isValidCharacter(c)) {
            return false;
        }
    }

    return true;
}

bool StringValidator::isValidCharacter(char c) {
    if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z')) {
        return true;
    }

    if (c >= '0' && c <= '9') {
        return true;
    }

    if (c == '-' || c == '\'' || c == ' '|| c == '.') {
        return true;
    }

    return false;
}