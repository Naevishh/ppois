/**
 * @file Moon.h
 * @author Aleks
 * @brief Класс для представления спутника планеты.
 *
 * @details
 * Moon наследуется от AstronomicalObject и добавляет информацию
 * о родительской планете, орбитальном периоде и массе.
 * Поддерживает расчёт угловой скорости, силы тяжести и расстояния до планеты.
 */

#ifndef PLANETARIUMPROJECT_MOON_H
#define PLANETARIUMPROJECT_MOON_H

#include <string>
#include "AstronomicalObject.h"
#include "../Utils/Enums.h"

class Planet;

/**
 * @brief Класс, представляющий спутник (луну).
 */
class Moon : public AstronomicalObject {
private:
    Planet* hostPlanet;   ///< Указатель на родительскую планету.
    double orbitalPeriod; ///< Орбитальный период (в днях).
    double mass;          ///< Масса спутника (в кг).

public:
    /**
     * @brief Конструктор спутника.
     *
     * @param name_ Название спутника.
     * @param magnitude_ Видимая звёздная величина.
     * @param absMagnitude_ Абсолютная звёздная величина.
     * @param azimuth_ Азимут.
     * @param altitude_ Высота над горизонтом.
     * @param hostPlanet_ Указатель на планету.
     * @param period_ Орбитальный период (в днях).
     * @param mass_ Масса (в кг).
     */
    Moon(const std::string& name_, double magnitude_, double absMagnitude_, double azimuth_,
         double altitude_, Planet* hostPlanet_, double period_, double mass_);

    /**
     * @brief Вычисляет расстояние до планеты по угловому диаметру.
     *
     * @param diameterFromPlanet Угловой диаметр спутника как видно с планеты (в градусах).
     * @return Расстояние до планеты (в тех же единицах, что и диаметр объекта).
     * @throws std::invalid_argument если угол отрицательный.
     */
    double getDistanceToPlanet(double diameterFromPlanet) const;

    /**
     * @brief Вычисляет угловую скорость обращения вокруг планеты.
     * @return Угловая скорость (рад/день).
     */
    double getAngularVelocity() const;

    /**
     * @brief Вычисляет ускорение свободного падения на поверхности спутника.
     * @return Ускорение (м/с²), используя G = 6.67430e-11.
     */
    double calculateSurfaceGravity() const;

    /**
     * @brief Возвращает название родительской планеты.
     * @return Строка с названием планеты.
     */
    std::string getHostPlanetName() const;

    /**
     * @brief Возвращает указатель на родительскую планету.
     * @return Указатель на Planet.
     */
    Planet* getHostPlanet() const;

    /**
     * @brief Возвращает орбитальный период.
     * @return Период в днях.
     */
    double getOrbitalPeriod() const;

    /**
     * @brief Возвращает массу спутника.
     * @return Масса в килограммах.
     */
    double getMass() const;
};

#endif // PLANETARIUMPROJECT_MOON_H