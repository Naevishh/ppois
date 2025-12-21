/**
 * @file Excursion.h
 * @author Aleks
 * @brief Класс экскурсии по музейному залу с поддержкой нескольких языков.
 *
 * @details
 * Excursion наследуется от Activity и представляет тематический маршрут
 * по экспонатам музея с возможностью выбора языка проведения.
 */

#ifndef PLANETARIUMPROJECT_EXCURSION_H
#define PLANETARIUMPROJECT_EXCURSION_H

#include "Activity.h"
#include "../Inventory/Exhibit.h"
#include "../Facade/Museum.h"
#include "../Utils/Enums.h"
#include <vector>
#include <string>

/**
 * @brief Экскурсия по музейному залу.
 *
 * Состоит из маршрута (списка экспонатов), названия и поддерживаемых языков.
 */
class Excursion : public Activity {
private:
    std::vector<Exhibit*> routeExhibits; ///< Список экспонатов маршрута.
    std::vector<std::string> languages;  ///< Поддерживаемые языки проведения.
    std::string routeName;               ///< Название маршрута.
    Museum* museum;                      ///< Музей, в котором проходит экскурсия.

public:
    /**
     * @brief Конструктор экскурсии.
     *
     * @param name Название мероприятия.
     * @param duration Продолжительность в часах.
     * @param theme Тематика (например, EDUCATION, HISTORY).
     * @param museum_ Указатель на музей.
     * @param routeName_ Название маршрута.
     */
    Excursion(const std::string& name, double duration, Enums::ActivityTheme theme, Museum* museum_,
              std::string routeName_);

    /**
     * @brief Проверяет, доступна ли экскурсия на указанном языке.
     *
     * @param language_ Название языка (только допустимые символы).
     * @return true, если язык поддерживается; иначе false.
     * @throws std::invalid_argument если язык содержит недопустимые символы.
     * @see StringValidator::validate
     */
    bool isAvailableInLanguage(const std::string& language_) const;

    /**
     * @brief Проверяет, является ли маршрут популярным.
     * @return true, если средний рейтинг экспонатов маршрута > 8; иначе false.
     */
    bool isRoutePopular();

    /**
     * @brief Проводит экскурсию: регистрирует просмотр всех экспонатов маршрута.
     *
     * @param date Дата проведения.
     * @return Строка с описанием события.
     * @see Museum::viewExhibit
     */
    std::string hold(const Date& date) override;

    /**
     * @brief Добавляет язык в список поддерживаемых.
     *
     * @param language Название языка.
     * @throws std::invalid_argument если язык недопустим.
     * @see StringValidator::validate
     */
    void addLanguage(const std::string& language);

    /**
     * @brief Добавляет экспонат в маршрут.
     *
     * @param exhibit Указатель на экспонат.
     * @throws std::invalid_argument если exhibit == nullptr.
     */
    void addExhibit(Exhibit* exhibit);
};

#endif // PLANETARIUMPROJECT_EXCURSION_H