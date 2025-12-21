/**
 * @file PriceCalculator.h
 * @author Aleks
 * @brief Класс для расчёта стоимости билета с учётом льгот.
 *
 * @details
 * Применяет скидки на основе категории посетителя (студент, ветеран и т.д.)
 * и возраста (дети до определённого возраста).
 */

#ifndef PLANETARIUMPROJECT_PRICECALCULATOR_H
#define PLANETARIUMPROJECT_PRICECALCULATOR_H

#include "../People/Visitor.h"

/**
 * @brief Калькулятор цен с поддержкой льгот.
 *
 * Применяет фиксированные правила скидок в зависимости от категории посетителя
 * и возраста (если категория не установлена явно).
 */
class PriceCalculator {
private:
    int maxFreeAge;       ///< Максимальный возраст для бесплатного входа (включительно).
    int maxDiscountAge;   ///< Максимальный возраст для детской скидки (включительно).

public:
    /**
     * @brief Конструктор с настройкой возрастных порогов.
     *
     * @param maxAge Максимальный возраст для бесплатного входа.
     * @param discountAge Максимальный возраст для скидки.
     */
    PriceCalculator(int maxAge, int discountAge);

    /**
     * @brief Возвращает максимальный возраст для бесплатного входа.
     * @return Возраст (в годах).
     */
    int getMaxFreeAge() const;

    /**
     * @brief Возвращает максимальный возраст для детской скидки.
     * @return Возраст (в годах).
     */
    int getMaxDiscountAge() const;

    /**
     * @brief Рассчитывает итоговую цену билета.
     *
     * @param basePrice Базовая цена билета (должна быть >= 0).
     * @param visitor Посетитель с возрастом и категорией льгот.
     * @return Итоговая цена:
     * - 0 для льготников (ветераны, инвалиды) и детей до maxFreeAge,
     * - 40% / 50% / 60% / 70% от базовой цены — в зависимости от категории,
     * - полная цена — для взрослых без льгот.
     * @throws std::invalid_argument если basePrice < 0.
     */
    double calculatePrice(double basePrice, const Visitor& visitor) const;
};

#endif // PLANETARIUMPROJECT_PRICECALCULATOR_H