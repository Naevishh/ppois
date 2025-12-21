/**
 * @file Star.h
 * @author Aleks
 * @brief Класс для представления звезды как астрономического объекта.
 *
 * @details
 * Star наследуется от AstronomicalObject и добавляет звёздно-специфичные свойства:
 * спектральный класс, массу, признак кратности и созвездие.
 * Название созвездия валидируется через StringValidator.
 */

#ifndef PLANETARIUMPROJECT_STAR_H
#define PLANETARIUMPROJECT_STAR_H

#include <string>
#include "AstronomicalObject.h"
#include "../Utils/Enums.h"

/**
 * @brief Класс, представляющий звезду.
 *
 * Расширяет базовый AstronomicalObject информацией о спектральном классе,
 * массе, кратности и созвездии.
 */
class Star : public AstronomicalObject {
private:
    Enums::SpectralClass spectralClass; ///< Спектральный класс звезды (O, B, A, ..., M).
    bool isMultiple;                    ///< Является ли система кратной (двойной, тройной и т.д.).
    double mass;                        ///< Масса звезды в солнечных массах.
    std::string constellation;          ///< Название созвездия, в котором находится звезда.

public:
    /**
     * @brief Конструктор звезды.
     *
     * @param name_ Название звезды.
     * @param magnitude_ Видимая звёздная величина.
     * @param absMagnitude_ Абсолютная звёздная величина.
     * @param azimuth_ Азимут в градусах.
     * @param altitude_ Высота над горизонтом в градусах.
     * @param spectralClass_ Спектральный класс.
     * @param isMultiple_ Признак кратной системы.
     * @param mass_ Масса в солнечных массах.
     */
    Star(const std::string& name_, double magnitude_, double absMagnitude_, double azimuth_, double altitude_,
         Enums::SpectralClass spectralClass_, bool isMultiple_, double mass_);

    /**
     * @brief Устанавливает название созвездия.
     *
     * @param constellation_ Название созвездия (только латиница, цифры, пробел, дефис, апостроф, точка).
     * @throws std::invalid_argument если строка содержит недопустимые символы.
     * @see StringValidator::validate
     */
    void addConstellation(const std::string& constellation_);

    /**
     * @brief Возвращает спектральный класс звезды.
     * @return Значение перечисления SpectralClass.
     */
    Enums::SpectralClass getSpectralClass() const;

    /**
     * @brief Возвращает признак кратной звёздной системы.
     * @return true, если звезда — часть кратной системы; иначе false.
     */
    bool getIsMultiple() const;

    /**
     * @brief Возвращает массу звезды.
     * @return Масса в солнечных массах.
     */
    double getMass() const;

    /**
     * @brief Возвращает название созвездия.
     * @return Строка с названием созвездия.
     */
    std::string getConstellation() const;
};

#endif // PLANETARIUMPROJECT_STAR_H