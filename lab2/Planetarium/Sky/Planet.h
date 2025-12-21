/**
 * @file Planet.h
 * @author Aleks
 * @brief Класс для представления планеты как астрономического объекта.
 *
 * @details
 * Planet наследуется от AstronomicalObject и добавляет планетарные характеристики:
 * тип, орбитальные параметры, массу, спутники и звезду-хозяина.
 * Поддерживает расчёт эксцентриситета, длины орбиты и расстояния до звезды.
 */

#ifndef PLANETARIUMPROJECT_PLANET_H
#define PLANETARIUMPROJECT_PLANET_H

#include <string>
#include <memory>
#include <vector>
#include "AstronomicalObject.h"
#include "Star.h"
#include "Moon.h"

/**
 * @brief Класс, представляющий планету.
 *
 * Может иметь спутники (Moons) и быть привязан к звезде (Star).
 */
class Planet : public AstronomicalObject {
private:
    Enums::PlanetType type;               ///< Тип планеты (земной, газовый гигант и т.д.).
    std::shared_ptr<Star> hostStar;       ///< Указатель на звезду, вокруг которой вращается планета.
    double orbitalPeriod;                 ///< Орбитальный период (в днях).
    double semiMajorAxis;                 ///< Большая полуось орбиты (в а.е.).
    double semiMinorAxis;                 ///< Малая полуось орбиты (в а.е.).
    std::vector<Moon> moons;              ///< Список спутников планеты.
    double mass;                          ///< Масса планеты (в массах Земли или Юпитера — по контексту).

public:
    /**
     * @brief Конструктор планеты (без привязки к звезде).
     *
     * @param name_ Название планеты.
     * @param magnitude_ Видимая звёздная величина.
     * @param absMagnitude_ Абсолютная звёздная величина.
     * @param azimuth_ Азимут.
     * @param altitude_ Высота над горизонтом.
     * @param type_ Тип планеты.
     * @param orbitalPeriod_ Орбитальный период (в днях).
     * @param semiMajorAxis_ Большая полуось (в а.е.).
     * @param semiMinorAxis_ Малая полуось (в а.е.).
     * @param mass_ Масса.
     */
    Planet(const std::string& name_, double magnitude_, double absMagnitude_, double azimuth_,
           double altitude_, Enums::PlanetType type_, double orbitalPeriod_, double semiMajorAxis_,
           double semiMinorAxis_, double mass_);

    /**
     * @brief Вычисляет эксцентриситет орбиты.
     * @return Значение эксцентриситета (0 ≤ e < 1).
     */
    double getEccentricity() const;

    /**
     * @brief Вычисляет расстояние до звезды по истинной аномалии.
     *
     * @param trueAnomaly Угол истинной аномалии в градусах [0, 360].
     * @return Расстояние до звезды (в а.е.).
     * @throws DegreeRangeError если угол вне диапазона [0, 360].
     */
    double getDistanceToHostStar(double trueAnomaly) const;

    /**
     * @brief Добавляет спутник к планете.
     * @param moon Спутник (Moon).
     */
    void addMoon(const Moon& moon);

    /**
     * @brief Возвращает количество спутников.
     * @return Число спутников.
     */
    int getMoonCount() const;

    /**
     * @brief Устанавливает звезду-хозяина.
     * @param star Умный указатель на звезду.
     */
    void setHostStar(std::shared_ptr<Star> star);

    /**
     * @brief Вычисляет приблизительную длину орбиты (по формуле Рамануджана).
     * @return Длина орбиты (в а.е.).
     */
    double calculateOrbitLength() const;

    /**
     * @brief Возвращает тип планеты.
     * @return Значение перечисления PlanetType.
     */
    Enums::PlanetType getPlanetType() const;
};

#endif // PLANETARIUMPROJECT_PLANET_H