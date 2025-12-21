/**
 * @file Screen.h
 * @author Aleks
 * @brief Класс для представления проекционного экрана.
 *
 * @details
 * Screen наследуется от Device и предоставляет геометрические характеристики:
 * ширину, длину, соотношение сторон и площадь.
 */

#ifndef PLANETARIUMPROJECT_SCREEN_H
#define PLANETARIUMPROJECT_SCREEN_H

#include "Device.h"

/**
 * @brief Класс проекционного экрана.
 *
 * Хранит физические размеры и позволяет вычислять производные параметры.
 */
class Screen : public Device {
private:
    double width;       ///< Ширина экрана в метрах.
    double length;      ///< Длина (высота) экрана в метрах.
    double aspectRatio; ///< Соотношение сторон (ширина / длина).

public:
    /**
     * @brief Конструктор экрана.
     *
     * @param name Название устройства.
     * @param width_ Ширина в метрах (> 0).
     * @param length_ Длина в метрах (> 0).
     */
    Screen(const std::string& name, double width_, double length_);

    /**
     * @brief Возвращает ширину экрана.
     * @return Ширина в метрах.
     */
    double getWidth() const;

    /**
     * @brief Возвращает длину (высоту) экрана.
     * @return Длина в метрах.
     */
    double getLength() const;

    /**
     * @brief Вычисляет и сохраняет соотношение сторон (ширина / длина).
     *
     * @note Результат сохраняется в поле aspectRatio.
     *       Метод не возвращает значение — используйте getWidth()/getLength() для расчётов.
     */
    virtual void calculateAspectRatio();

    /**
     * @brief Вычисляет площадь экрана.
     * @return Площадь = ширина × длина (в кв. метрах).
     */
    virtual double calculateArea() const;
};

#endif // PLANETARIUMPROJECT_SCREEN_H