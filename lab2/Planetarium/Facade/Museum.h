/**
 * @file Museum.h
 * @author Aleks
 * @brief Класс музейного зала — помещения для выставки астрономических экспонатов.
 *
 * @details
 * Museum наследуется от PlanetariumVenue и управляет коллекцией Exhibit.
 * Поддерживает поиск, оценку, просмотр и взаимодействие с экспонатами.
 */

#ifndef PLANETARIUMPROJECT_MUSEUM_H
#define PLANETARIUMPROJECT_MUSEUM_H

#include "PlanetariumVenue.h"
#include "../Inventory/Exhibit.h"
#include "../Utils/Enums.h"
#include <vector>

/**
 * @brief Музейный зал планетария.
 *
 * Ориентирован на тематические выставки с возможностью оценки и взаимодействия.
 */
class Museum : public PlanetariumVenue {
private:
    int exhibitsNumber;                     ///< Общее количество экспонатов.
    Enums::Theme theme;                     ///< Тематика выставки (например, SOLAR_SYSTEM).
    std::vector<Exhibit*> exhibits;         ///< Список экспонатов.

public:
    /**
     * @brief Конструктор музея.
     *
     * @param name_ Название зала.
     * @param capacity_ Вместимость посетителей.
     * @param exhibitsNumber_ Объявленное количество экспонатов.
     * @param theme_ Тематика выставки.
     */
    Museum(std::string name_, int capacity_, int exhibitsNumber_, Enums::Theme theme_);

    /**
     * @brief Находит экспонат по названию.
     *
     * @param name Название экспоната.
     * @return Указатель на Exhibit, или nullptr, если не найден.
     */
    Exhibit* findExhibit(const std::string& name);

    /**
     * @brief Рассчитывает средний рейтинг всех экспонатов.
     * @return Среднее арифметическое (0.0, если нет экспонатов).
     */
    double getAverageRating();

    /**
     * @brief Находит самый популярный экспонат (с наивысшим рейтингом).
     * @return Указатель на экспонат, или nullptr, если список пуст.
     */
    Exhibit* findMostPopularExhibit();

    /**
     * @brief Оценивает экспонат.
     *
     * @param ratedExhibit Указатель на экспонат.
     * @param rating Оценка от 0 до 10.
     * @throws std::invalid_argument если оценка вне диапазона.
     * @see Exhibit::updateRating
     */
    static void rateExhibit(Exhibit* ratedExhibit, int rating);

    /**
     * @brief Регистрирует просмотр экспоната и возвращает информацию о нём.
     *
     * @param exhibit Указатель на экспонат.
     * @return Информационный текст об экспонате.
     * @see Exhibit::view, Exhibit::getInfo
     */
    std::string viewExhibit(Exhibit* exhibit);

    /**
     * @brief Взаимодействует с экспонатом: просмотр + попытка касания.
     *
     * @param name Название экспоната (проходит валидацию).
     * @return Результат взаимодействия или сообщение об ошибке.
     * @throws std::invalid_argument если название содержит недопустимые символы.
     * @see StringValidator::validate, Exhibit::touchExhibit
     */
    std::string interactWithExhibit(const std::string& name);

    /**
     * @brief Добавляет экспонат в коллекцию.
     * @param exhibit Указатель на экспонат.
     */
    void addExhibit(Exhibit* exhibit);

    /**
     * @brief Возвращает список всех экспонатов.
     * @return Вектор указателей на Exhibit.
     */
    std::vector<Exhibit*> getExhibits();
};

#endif // PLANETARIUMPROJECT_MUSEUM_H