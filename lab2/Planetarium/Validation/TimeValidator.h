/**
 * @file TimeValidator.h
 * @author Ященко Александра
 * @brief Заголовочный файл класса TimeValidator для валидации даты и времени.
 *
 * @details
 * Класс TimeValidator предоставляет статические методы для проверки
 * корректности компонентов даты и времени: года, месяца, дня, часа,
 * минуты и секунды. Поддерживает валидацию с учётом високосных лет
 * и текущего системного времени. Используется в проекте PlanetariumProject.
 */

#ifndef PLANETARIUMPROJECT_TIMEVALIDATOR_H
#define PLANETARIUMPROJECT_TIMEVALIDATOR_H

#include <string>

/**
 * @brief Утилитный класс для валидации временных значений и дат.
 *
 * Все методы статические. Поддерживает валидацию отдельных компонентов времени,
 * а также комплексную проверку даты и даты со временем.
 */
class TimeValidator {
public:
    /**
     * @brief Конструктор по умолчанию (не используется — все методы статические).
     */
    TimeValidator() = default;

    /**
     * @brief Возвращает текущий год по системному времени.
     * @return Текущий год (например, 2025).
     */
    static int getCurrentYear();

    /**
     * @brief Проверяет, является ли год високосным.
     * @param year Год для проверки.
     * @return true, если год високосный; иначе false.
     */
    static bool isLeapYear(int year);

    /**
     * @brief Возвращает количество дней в указанном месяце.
     * @param month Номер месяца (1–12).
     * @param year Год (опционально); если задан и месяц — февраль, учитывается високосность.
     * @return Количество дней в месяце, или 0 при некорректном номере месяца.
     */
    static int getDaysInMonth(int month, int year = -1);

    /**
     * @brief Преобразует строку в целое число.
     * @param str Строка для преобразования.
     * @return Целое число, или -1 при ошибке (некорректный формат, переполнение и т.д.).
     */
    static int stringToInt(const std::string& str);

    /**
     * @brief Проверяет корректность часа, заданного строкой.
     * @param hourStr Строка с числом (ожидается 0–23).
     * @return true, если строка корректна и представляет допустимый час; иначе false.
     * @see isValidHour(int)
     */
    static bool isValidHour(const std::string& hourStr);

    /**
     * @brief Проверяет корректность часа.
     * @param hour Час (ожидается 0–23).
     * @return true, если час корректен; иначе false.
     */
    static bool isValidHour(int hour);

    /**
     * @brief Проверяет корректность минут, заданных строкой.
     * @param minuteStr Строка с числом (ожидается 0–59).
     * @return true, если строка корректна и представляет допустимые минуты; иначе false.
     * @see isValidMinute(int)
     */
    static bool isValidMinute(const std::string& minuteStr);

    /**
     * @brief Проверяет корректность минут.
     * @param minute Минуты (ожидается 0–59).
     * @return true, если минуты корректны; иначе false.
     */
    static bool isValidMinute(int minute);

    /**
     * @brief Проверяет корректность секунд, заданных строкой.
     * @param secondStr Строка с числом (ожидается 0–59).
     * @return true, если строка корректна и представляет допустимые секунды; иначе false.
     * @see isValidSecond(int)
     */
    static bool isValidSecond(const std::string& secondStr);

    /**
     * @brief Проверяет корректность секунд.
     * @param second Секунды (ожидается 0–59).
     * @return true, если секунды корректны; иначе false.
     */
    static bool isValidSecond(int second);

    /**
     * @brief Проверяет корректность дня, заданного строкой.
     * @param dayStr Строка с числом (ожидается 1–31).
     * @param month Номер месяца (опционально, 1–12); если задан — проверяется максимальное число дней.
     * @param year Год (опционально); используется при проверке февраля.
     * @return true, если день допустим; иначе false.
     * @see isValidDay(int, int, int)
     */
    static bool isValidDay(const std::string& dayStr, int month = -1, int year = -1);

    /**
     * @brief Проверяет корректность дня.
     * @param day День месяца.
     * @param month Номер месяца (опционально, 1–12).
     * @param year Год (опционально).
     * @return true, если день допустим с учётом месяца и года (если указаны); иначе false.
     * @see getDaysInMonth
     */
    static bool isValidDay(int day, int month = -1, int year = -1);

    /**
     * @brief Проверяет корректность месяца, заданного строкой.
     * @param monthStr Строка с числом (ожидается 1–12).
     * @return true, если строка корректна и представляет допустимый месяц; иначе false.
     * @see isValidMonth(int)
     */
    static bool isValidMonth(const std::string& monthStr);

    /**
     * @brief Проверяет корректность месяца.
     * @param month Номер месяца (ожидается 1–12).
     * @return true, если месяц корректен; иначе false.
     */
    static bool isValidMonth(int month);

    /**
     * @brief Проверяет корректность года, заданного строкой.
     * @param yearStr Строка с числом.
     * @param minYear Минимально допустимый год (по умолчанию 1900).
     * @param maxYearsFuture Максимальное количество лет в будущем относительно текущего (по умолчанию 10).
     * @return true, если год допустим; иначе false.
     * @see isValidYear(int, int, int)
     */
    static bool isValidYear(const std::string& yearStr, int minYear = 1900, int maxYearsFuture = 10);

    /**
     * @brief Проверяет корректность года.
     * @param year Год для проверки.
     * @param minYear Минимально допустимый год (по умолчанию 1900).
     * @param maxYearsFuture Максимальное количество лет в будущем относительно текущего (по умолчанию 10).
     * @return true, если minYear ≤ year ≤ текущий_год + maxYearsFuture; иначе false.
     * @see getCurrentYear
     */
    static bool isValidYear(int year, int minYear = 1900, int maxYearsFuture = 10);

    /**
     * @brief Проверяет корректность времени (часы и минуты, опционально секунды).
     * @param hour Часы (0–23).
     * @param minute Минуты (0–59).
     * @param second Секунды (0–59); если передано -1 — не проверяются.
     * @return true, если все указанные компоненты времени корректны; иначе false.
     * @see isValidHour, isValidMinute, isValidSecond
     */
    static bool isValidTime(int hour, int minute, int second = -1);

    /**
     * @brief Проверяет корректность даты.
     * @param day День месяца.
     * @param month Месяц (1–12).
     * @param year Год.
     * @return true, если дата корректна (включая проверку дней в месяце); иначе false.
     * @see isValidDay, isValidMonth, isValidYear
     */
    static bool isValidDate(int day, int month, int year);

    /**
     * @brief Проверяет корректность даты и времени.
     * @param day День месяца.
     * @param month Месяц (1–12).
     * @param year Год.
     * @param hour Часы (0–23).
     * @param minute Минуты (0–59).
     * @param second Секунды (0–59); если -1 — не проверяются.
     * @return true, если и дата, и время корректны; иначе false.
     * @see isValidDate, isValidTime
     */
    static bool isValidDateTime(int day, int month, int year, int hour, int minute, int second = -1);
};

#endif // PLANETARIUMPROJECT_TIMEVALIDATOR_H