/**
 * @file Telescope.h
 * @author Aleks
 * @brief Класс для представления телескопа как астрономического устройства.
 *
 * @details
 * Telescope наследуется от Device и предоставляет функционал для наведения,
 * расчёта разрешающей способности, предельной звёздной величины
 * и проверки возможности наблюдения объекта.
 */

#ifndef PLANETARIUMPROJECT_TELESCOPE_H
#define PLANETARIUMPROJECT_TELESCOPE_H

#include "Device.h"
#include "../Utils/Enums.h"
#include "../Sky/SkyPosition.h"
#include "../Sky/AstronomicalObject.h"

/**
 * @brief Класс телескопа.
 *
 * Моделирует оптические характеристики и управление наведением.
 */
class Telescope : public Device {
private:
    double objectiveDiameter; ///< Диаметр объектива в миллиметрах.
    double focalLength;       ///< Фокусное расстояние в миллиметрах.
    Enums::TelescopeType type;///< Тип телескопа (рефрактор, рефлектор и т.д.).
    SkyPosition position;     ///< Текущее направление наведения (азимут и высота).

public:
    /**
     * @brief Конструктор телескопа.
     *
     * @param name_ Название устройства.
     * @param diameter_ Диаметр объектива (в мм, > 0).
     * @param focalLength_ Фокусное расстояние (в мм, > 0).
     * @param type_ Тип телескопа.
     */
    Telescope(const std::string& name_, double diameter_, double focalLength_, Enums::TelescopeType type_);

    /**
     * @brief Наводит телескоп на заданные координаты.
     *
     * @param azimuth_ Азимут в градусах [0, 360].
     * @param altitude_ Высота над горизонтом в градусах [-90, 90].
     * @throws DegreeRangeError если координаты выходят за допустимые пределы.
     * @see SkyPosition::setAzimuth, SkyPosition::setAltitude
     */
    void focus(double azimuth_, double altitude_);

    /**
     * @brief Рассчитывает теоретическую разрешающую способность по критерию Рэлея.
     * @return Разрешение в угловых секундах (≈ 116 / D, где D — диаметр в мм).
     */
    double calculateResolution() const;

    /**
     * @brief Проверяет, может ли телескоп наблюдать указанный объект.
     *
     * @param object Астрономический объект.
     * @return true, если:
     * - объект достаточно яркий (magnitude ≤ limitingMagnitude), и
     * - для не-звёзд: его угловой размер ≥ разрешения телескопа.
     * Звёзды наблюдаются всегда при условии яркости.
     * @see calculateLimitingMagnitude, AstronomicalObject::calculateAngularDiameter
     */
    bool canObserve(const AstronomicalObject& object) const;

    /**
     * @brief Рассчитывает предельную звёздную величину, видимую в телескоп.
     * @return Предельная величина (≈ 2.7 + 5·log10(D), D в мм).
     */
    double calculateLimitingMagnitude() const;
};

#endif // PLANETARIUMPROJECT_TELESCOPE_H