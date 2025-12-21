/**
 * @file Exhibit.h
 * @author Aleks
 * @brief Класс для представления выставочного экспоната в планетарии.
 *
 * @details
 * Exhibit хранит название, информацию, рейтинг, количество просмотров
 * и признак возможности физического взаимодействия ("hands-on").
 */

#ifndef PLANETARIUMPROJECT_EXHIBIT_H
#define PLANETARIUMPROJECT_EXHIBIT_H

#include <string>
#include <vector>

/**
 * @brief Выставочный экспонат.
 *
 * Поддерживает сбор статистики, оценок и ограничение на взаимодействие.
 */
class Exhibit {
private:
    std::string name;           ///< Название экспоната.
    int totalViews;             ///< Общее количество просмотров.
    std::vector<int> ratings;   ///< Список оценок (от 0 до 10).
    double visitorRating;       ///< Средний рейтинг (обновляется после каждой оценки).
    std::string info;           ///< Информационный текст об экспонате.
    bool handOn;                ///< Можно ли трогать экспонат.

public:
    /**
     * @brief Конструктор экспоната.
     *
     * @param name_ Название.
     * @param handOn_ Признак возможности физического взаимодействия.
     */
    Exhibit(std::string name_, bool handOn_);

    /**
     * @brief Возвращает название экспоната.
     * @return Строка с названием.
     */
    std::string getName() const;

    /**
     * @brief Возвращает информационный текст.
     * @return Строка с описанием.
     */
    std::string getInfo() const;

    /**
     * @brief Возвращает средний рейтинг.
     * @return Среднее значение (от 0.0 до 10.0).
     */
    double getRating() const;

    /**
     * @brief Возвращает общее количество просмотров.
     * @return Число посещений.
     */
    int getTotalViews() const;

    /**
     * @brief Устанавливает информационный текст.
     *
     * @param info_ Новый текст (должен пройти валидацию через StringValidator).
     * @throws std::invalid_argument если текст содержит недопустимые символы.
     * @see StringValidator::validate
     */
    void addInfo(std::string info_);

    /**
     * @brief Регистрирует просмотр экспоната.
     *
     * Увеличивает счётчик totalViews на 1.
     */
    void view();

    /**
     * @brief Обновляет рейтинг на основе новой оценки.
     *
     * @param rating Новая оценка (целое число от 0 до 10 включительно).
     * @throws std::invalid_argument если оценка вне диапазона.
     * @note Средний рейтинг пересчитывается как скользящее среднее.
     */
    void updateRating(int rating);

    /**
     * @brief Проверяет, является ли экспонат популярным.
     * @return true, если средний рейтинг > 8; иначе false.
     */
    bool isExhibitPopular() const;

    /**
     * @brief Позволяет пользователю потрогать экспонат.
     *
     * @throws BreakingRules если handOn == false.
     */
    void touchExhibit();
};

#endif // PLANETARIUMPROJECT_EXHIBIT_H