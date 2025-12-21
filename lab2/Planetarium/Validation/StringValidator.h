/**
 * @file StringValidator.h
 * @author Ященко Александра
 * @brief Заголовочный файл класса StringValidator для валидации текстовых строк.
 *
 * @details
 * Класс StringValidator предоставляет статические методы для проверки,
 * состоит ли строка только из допустимых символов (латинские буквы,
 * цифры, пробел, дефис, апостроф и точка). Пустая строка считается недопустимой.
 * Предназначен для использования в проекте PlanetariumProject.
 */

#ifndef PLANETARIUMPROJECT_STRINGVALIDATOR_H
#define PLANETARIUMPROJECT_STRINGVALIDATOR_H

#include <string>
#include <cctype>

/**
 * @brief Класс-утилита для валидации строк.
 *
 * Содержит методы для проверки допустимости символов и целых строк.
 */
class StringValidator {
public:
    /**
     * @brief Проверяет, состоит ли строка только из допустимых символов.
     *
     * @details
     * Возвращает false для пустой строки. Иначе проверяет каждый символ
     * с помощью isValidCharacter().
     *
     * @param text Строка для проверки.
     * @return true, если строка допустима; иначе false.
     * @see isValidCharacter
     */
    static bool validate(const std::string& text);

    /**
     * @brief Проверяет, является ли символ допустимым.
     *
     * @details
     * Допустимыми считаются:
     * - латинские буквы (A–Z, a–z),
     * - цифры (0–9),
     * - символы: дефис '-', апостроф '\'', пробел ' ', точка '.'.
     *
     * @param c Проверяемый символ.
     * @return true, если символ допустим; иначе false.
     */
    static bool isValidCharacter(char c);
};

#endif // PLANETARIUMPROJECT_STRINGVALIDATOR_H