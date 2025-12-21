/**
 * @file DomeShapedScreen.h
 * @author Aleks
 * @brief Класс купольного экрана для планетария.
 *
 * @details
 * DomeShapedScreen наследуется от Screen и переопределяет расчёт площади.
 * Поддерживает проверку совместимости с проекторами на основе throw-коэффициента.
 */

#ifndef PLANETARIUMPROJECT_DOMESHAPEDSCREEN_H
#define PLANETARIUMPROJECT_DOMESHAPEDSCREEN_H

#include "Screen.h"
#include "Projector.h"

/**
 * @brief Купольный экран для проекции звёздного неба.
 *
 * Представляет собой полусферу заданного диаметра и высоты.
 */
class DomeShapedScreen : public Screen {
private:
    double diameter; ///< Диаметр купола (в метрах).
    double height;   ///< Высота купола (в метрах).

public:
    /**
     * @brief Конструктор купольного экрана.
     *
     * @param name Название устройства.
     * @param diameter_ Диаметр купола (в метрах).
     * @param height_ Высота купола (в метрах).
     * @note Ширина и длина для базового Screen инициализируются как π·diameter.
     */
    explicit DomeShapedScreen(const std::string& name, double diameter_, double height_);

    /**
     * @brief Возвращает диаметр купола.
     * @return Диаметр в метрах.
     */
    double getDiameter() const;

    /**
     * @brief Возвращает высоту купола.
     * @return Высота в метрах.
     */
    double getHeight() const;

    /**
     * @brief Переопределяет расчёт площади для купола.
     *
     * @return Площадь = π · diameter² (приближение для полусферы).
     */
    double calculateArea() const override;

    /**
     * @brief Проверяет совместимость с проектором.
     *
     * @param projector Проектор для проверки.
     * @return true, если throw-коэффициент проектора > 2 (подходит для купола); иначе false.
     * @see Projector::getThrowRatio
     */
    bool isProjectorCompatible(const Projector& projector) const;
};

#endif // PLANETARIUMPROJECT_DOMESHAPEDSCREEN_H