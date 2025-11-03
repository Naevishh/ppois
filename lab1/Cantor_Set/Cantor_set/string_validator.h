/**
 * @file string_validator.h
 * @brief Заголовочный файл класса для валидации вводимых строк, содержащих множество
 * @author Ященко Александра
 */

#ifndef SEM3_L1_PPOIS_P2_STRING_VALIDATOR_H
#define SEM3_L1_PPOIS_P2_STRING_VALIDATOR_H

#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cctype>
#include <algorithm>

/**
 * @class string_validator
 * @brief Класс для проверки корректности ввода множеств
 * @details Данный класс предоставляет функциональность для проверки синтаксической
 * корректности множеств, содержащих фигурные {} и угловые <> скобки, а также буквы
 * латинского алфавита и запятые. Класс отслеживает баланс скобок и проверяет
 * допустимые последовательности символов.
 */
class string_validator {
private:
    int curly_braces_ = 0;  ///< Счетчик фигурных скобок для отслеживания баланса
    int angle_braces_ = 0;  ///< Счетчик угловых скобок для отслеживания баланса

    /**
     * @brief Получает следующий символ в строке
     * @param input_string Входная строка для анализа
     * @param index Текущий индекс в строке
     * @return Следующий символ или '\0', если достигнут конец строки
     */
    char get_next_char(const std::string& input_string, size_t index);

    /**
     * @brief Обрабатывает текущий символ с учетом следующего
     * @param current_char Текущий обрабатываемый символ
     * @param next_char Следующий символ в строке
     * @return true, если символ обработан успешно, false в противном случае
     */
    bool process_character(char current_char, char next_char);

    /**
     * @brief Проверяет, является ли символ допустимым
     * @param character Проверяемый символ
     * @return true, если символ разрешен, false в противном случае
     */
    bool is_allowed_character(char character);

    /**
     * @brief Проверяет правила последовательности символов
     * @param current_char Текущий символ
     * @param next_char Следующий символ
     * @return true, если последовательность допустима, false в противном случае
     */
    bool check_sequence_rules(char current_char, char next_char);

    /**
     * @brief Обновляет счетчики скобок
     * @param character Текущий символ для обработки
     */
    void update_brace_counters(char character);

public:
    /**
     * @brief Валидирует входную строку
     * @param input_string Строка для валидации
     * @param is_element Флаг, указывающий является ли строка элементом
     * @return true, если строка валидна, false в противном случае
     * @see set_read
     */
    bool validate(const std::string& input_string, bool is_element);

    /**
     * @brief Статический метод для чтения и подготовки строки
     * @param input_string Строка для обработки
     * @param is_element Флаг, указывающий является ли строка элементом
     * @return true, если строка валидна и подготовлена, false в противном случае
     * @see validate
     * @details Метод выполняет валидацию строки и при успехе удаляет из нее
     * все пробелы и запятые для дальнейшей обработки
     */
    static bool set_read(std::string& input_string, bool is_element);

    friend class StringValidatorTest;  ///< Дружественный класс для тестирования
};

#endif //SEM3_L1_PPOIS_P2_STRING_VALIDATOR_H
