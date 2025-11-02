/**
 * @file String_validator.h
 * @brief Заголовочный файл класса для валидации и обработки строк
 * @author Ященко Александра
 * @details
 * Данный файл содержит объявление класса string_validator, который предоставляет
 * статические методы для проверки корректности английских и русских слов,
 * обработки строк и извлечения слов из входных данных.
 */

#ifndef SEM3_L1_PPOIS_STRING_VALIDATOR_H
#define SEM3_L1_PPOIS_STRING_VALIDATOR_H


#include <string>
#include <string>
#include <cctype>

/**
 * @class string_validator
 * @brief Класс для валидации и обработки строковых данных
 * @details
 * Класс предоставляет статические методы для проверки корректности слов,
 * обработки регистра, удаления пробелов и извлечения слов из строк.
 */
class string_validator {
public:

    /**
     * @brief Проверяет корректность английского слова
     * @param english_word Строка для проверки
     * @return true если слово содержит только буквы, апострофы и дефисы, и имеет корректную длину
     * @see valid_russian_word
     */
    static bool valid_english_word(const std::string&);

    /**
     * @brief Проверяет корректность русского слова
     * @param russian_word Строка для проверки
     * @return true если слово содержит только русские буквы, апострофы и дефисы, и имеет корректную длину
     * @see valid_english_word
     */
    static bool valid_russian_word(const std::string&);

    /**
     * @brief Проверяет длину английского слова
     * @param input_word Строка для проверки длины
     * @return true если длина слова от 1 до 50 символов включительно
     */
    static bool is_correct_length(const std::string&);

    /**
     * @brief Проверяет длину русского слова
     * @param input_word Строка для проверки длины
     * @return true если длина слова от 1 до 50 символов включительно (с учетом UTF-8)
     */
    static bool is_correct_length_rus(const std::string&);

    /**
     * @brief Преобразует строку к нижнему регистру
     * @param input_string Исходная строка
     * @return Строка в нижнем регистре
     * @details Поддерживает как английские, так и русские символы
     * @see https://ru.stackoverflow.com/questions/1390641
     */
    static std::string to_lower(const std::string&);

    /**
     * @brief Удаляет пробельные символы с начала и конца строки
     * @param input_string Ссылка на строку для обработки
     */
    static void remove_spaces(std::string&);

    /**
     * @brief Извлекает первое слово из строки
     * @param input_line Исходная строка
     * @param word_to_extract Ссылка на переменную для сохранения извлеченного слова
     * @return Оставшаяся часть строки после извлечения слова
     * @details Извлеченное слово автоматически преобразуется к нижнему регистру
     */
    static std::string extract_word(const std::string& input_line, std::string&);

    /**
     * @brief Извлекает пару слов (английское и русское) из строки
     * @param input_line Исходная строка, содержащая слова
     * @return Пара строк: английское слово и русское слово
     * @details Русское слово может быть пустым, если оно отсутствует или невалидно
     */
    static std::pair<std::string, std::string> word_pair_input(const std::string&);
};

#endif //SEM3_L1_PPOIS_STRING_VALIDATOR_H




