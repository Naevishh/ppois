/**
 * @file PlanetariumProjector.h
 * @author Aleks
 * @brief Специализированный проектор для купольного планетария.
 *
 * @details
 * PlanetariumProjector расширяет Projector возможностью проецировать
 * астрономические объекты и встроенные шоу на купольный экран (DomeShapedScreen).
 * Поддерживает управление списком доступных объектов и текущего шоу.
 */

#ifndef PLANETARIUMPROJECT_PLANETARIUMPROJECTOR_H
#define PLANETARIUMPROJECT_PLANETARIUMPROJECTOR_H

#include "Projector.h"
#include "DomeShapedScreen.h"
#include "../Sky/AstronomicalObject.h"
#include "../Utils/Enums.h"

/**
 * @brief Проектор для купольного планетария.
 *
 * Работает только с DomeShapedScreen и поддерживает проекцию объектов и демонстраций.
 */
class PlanetariumProjector : public Projector {
private:
    std::vector<AstronomicalObject*> objects;               ///< Доступные для проекции объекты.
    std::vector<Enums::BuiltInPlanetariumShow> shows;       ///< Поддерживаемые встроенные шоу.
    Enums::BuiltInPlanetariumShow currentShow;              ///< Текущее активное шоу.
    std::string currentObjectName;                          ///< Имя текущего проецируемого объекта.

public:
    /**
     * @brief Добавляет астрономический объект в список доступных для проекции.
     * @param object Указатель на объект.
     */
    void addObject(AstronomicalObject* object);

    /**
     * @brief Конструктор купольного проектора.
     *
     * @param name Название устройства.
     * @param brightness_ Начальная яркость.
     * @param throwRatio_ Throw-коэффициент.
     * @param fov_ Угол обзора (в градусах).
     */
    PlanetariumProjector(const std::string& name, double brightness_, double throwRatio_, double fov_);

    /**
     * @brief Устанавливает размер проекции на основе радиуса купола.
     *
     * @param screenRadius Радиус купольного экрана (в метрах).
     * @throws std::invalid_argument если радиус вне [0, 15].
     * @note Расстояние до экрана вычисляется по формуле: R / sin(FOV/2).
     */
    void setProjectionSize(double screenRadius) override;

    /**
     * @brief Производит проекцию указанного астрономического объекта.
     *
     * @param screen Купольный экран.
     * @param object Объект для проекции.
     * @throws IncompatibleDevices если проектор несовместим с экраном.
     * @throws DeviceCapabilityException если объект не добавлен в список доступных.
     */
    void projectObject(DomeShapedScreen* screen, AstronomicalObject* object);

    /**
     * @brief Запускает встроенное демонстрационное шоу.
     *
     * @param screen Купольный экран.
     * @param show Тип шоу (например, SOLAR_SYSTEM_DEMO).
     * @throws IncompatibleDevices если проектор несовместим с экраном.
     */
    void projectShow(DomeShapedScreen* screen, const Enums::BuiltInPlanetariumShow& show);

    /**
     * @brief Возвращает текущее активное шоу.
     * @return Значение перечисления BuiltInPlanetariumShow.
     */
    Enums::BuiltInPlanetariumShow getShow() const;
};

#endif // PLANETARIUMPROJECT_PLANETARIUMPROJECTOR_H