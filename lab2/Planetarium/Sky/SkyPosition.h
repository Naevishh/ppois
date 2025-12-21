/**
 * @file SkyPosition.h
 * @author Aleks
 * @brief Класс для представления положения объекта на небесной сфере.
 *
 * @details
 * SkyPosition хранит азимут и высоту (альтитуду) в градусах.
 * Поддерживает проверку корректности диапазонов и определение видимости над горизонтом.
 */

#ifndef PLANETARIUMPROJECT_SKYPOSITION_H
#define PLANETARIUMPROJECT_SKYPOSITION_H

#include <string>

/**
 * @brief Класс для хранения небесных координат (азимут и высота).
 */
class SkyPosition {
private:
    double azimuth;   ///< Азимут в градусах [0, 360].
    double altitude;  ///< Высота над горизонтом в градусах [-90, 90].

public:
    /**
     * @brief Конструктор позиции.
     *
     * @param azimuth_ Азимут в градусах.
     * @param altitude_ Высота над горизонтом в градусах.
     * @note Нет валидации в конструкторе — проверка выполняется в сеттерах.
     */
    SkyPosition(double azimuth_, double altitude_);

    /**
     * @brief Возвращает азимут.
     * @return Значение в градусах [0, 360].
     */
    double getAzimuth() const;

    /**
     * @brief Возвращает высоту над горизонтом.
     * @return Значение в градусах [-90, 90].
     */
    double getAltitude() const;

    /**
     * @brief Устанавливает азимут.
     *
     * @param azimuth_ Новое значение азимута.
     * @throws DegreeRangeError если значение не в диапазоне [0, 360].
     */
    void setAzimuth(double azimuth_);

    /**
     * @brief Устанавливает высоту над горизонтом.
     *
     * @param altitude_ Новое значение высоты.
     * @throws DegreeRangeError если значение не в диапазоне [-90, 90].
     */
    void setAltitude(double altitude_);

    /**
     * @brief Проверяет, находится ли объект над горизонтом.
     * @return true, если altitude >= 0; иначе false.
     */
    bool isAboveHorizon() const;

    /**
     * @brief Возвращает строковое представление позиции.
     * @return Строка вида "Az: 120.5°, Alt: 30.2°".
     */
    std::string toString() const;
};

#endif // PLANETARIUMPROJECT_SKYPOSITION_H