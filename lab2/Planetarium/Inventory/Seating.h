/**
 * @file Seating.h
 * @author Aleks
 * @brief Класс для управления посадочными местами в зале планетария.
 *
 * @details
 * Seating хранит общее количество мест и число рядов,
 * позволяет рассчитать количество мест в ряду.
 */

#ifndef PLANETARIUMPROJECT_SEATING_H
#define PLANETARIUMPROJECT_SEATING_H

/**
 * @brief Класс распределения мест в зрительном зале.
 */
class Seating {
private:
    int seatsNumber; ///< Общее количество мест (≥ 0).
    int rows;        ///< Количество рядов (устанавливается отдельно).

public:
    /**
     * @brief Конструктор с указанием общего числа мест.
     * @param seatsNumber_ Количество мест (не проверяется на отрицательность).
     */
    Seating(int seatsNumber_);

    /**
     * @brief Возвращает общее количество мест.
     * @return Число мест.
     */
    int getSeatsNumber() const;

    /**
     * @brief Устанавливает количество рядов.
     *
     * @param rows_ Новое значение (должно быть ≥ 0).
     * @throws std::invalid_argument если rows_ < 0.
     */
    void setRowsNumber(int rows_);

    /**
     * @brief Рассчитывает количество мест в одном ряду.
     * @return Целочисленное деление seatsNumber / rows.
     * @note Не проверяет деление на ноль — вызов после setRowsNumber(0) приведёт к неопределённому поведению.
     */
    int calculateSeatsPerRow();
};

#endif // PLANETARIUMPROJECT_SEATING_H