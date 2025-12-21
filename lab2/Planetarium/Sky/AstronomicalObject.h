/**
 * @file AstronomicalObject.h
 * @author Aleks
 * @brief Базовый класс для всех астрономических объектов.
 *
 * @details
 * Содержит общие свойства: название, звёздные величины, положение на небе,
 * время восхода/захода, диаметр. Предоставляет методы для расчёта расстояния,
 * углового диаметра и видимости.
 */

#ifndef PLANETARIUMPROJECT_ASTRONOMICALOBJECT_H
#define PLANETARIUMPROJECT_ASTRONOMICALOBJECT_H

#include <string>
#include "SkyPosition.h"
#include "../Utils/Enums.h"
#include "../Utils/MyTime.h"

/**
 * @brief Абстрактный базовый класс для астрономических объектов.
 *
 * Используется как основа для Star, Planet, Moon и других типов объектов.
 */
class AstronomicalObject {
private:
    std::string name;               ///< Название объекта.
    double magnitude;               ///< Видимая звёздная величина.
    double absoluteMagnitude;       ///< Абсолютная звёздная величина.
    double diameter;                ///< Физический диаметр (в км).
    SkyPosition position;           ///< Текущее положение на небе.
    Enums::ObjectType type;         ///< Тип объекта (звезда, планета и т.д.).
    MyTime riseTime;                ///< Время восхода.
    MyTime setTime;                 ///< Время захода.

public:
    /**
     * @brief Конструктор базового астрономического объекта.
     *
     * @param name_ Название объекта.
     * @param magnitude_ Видимая звёздная величина.
     * @param absMagnitude_ Абсолютная звёздная величина.
     * @param azimuth_ Азимут (в градусах).
     * @param altitude_ Высота над горизонтом (в градусах).
     * @param type_ Тип объекта.
     */
    AstronomicalObject(const std::string& name_, double magnitude_, double absMagnitude_,
                       double azimuth_, double altitude_, Enums::ObjectType type_);

    /**
     * @brief Возвращает абсолютную звёздную величину.
     * @return Значение абсолютной величины.
     */
    double getAbsoluteMagnitude() const;

    /**
     * @brief Возвращает тип объекта.
     * @return Значение перечисления ObjectType.
     */
    Enums::ObjectType getType() const;

    /**
     * @brief Возвращает название объекта.
     * @return Строка с названием.
     */
    std::string getName() const;

    /**
     * @brief Возвращает текущее положение на небе.
     * @return Объект SkyPosition.
     */
    SkyPosition getPosition() const;

    /**
     * @brief Возвращает видимую звёздную величину.
     * @return Значение видимой величины.
     */
    double getMagnitude() const;

    /**
     * @brief Возвращает физический диаметр объекта.
     * @return Диаметр (в единицах, принятых в проекте).
     */
    double getDiameter() const;

    /**
     * @brief Устанавливает физический диаметр объекта.
     * @param diameter_ Новое значение диаметра.
     */
    void setDiameter(double diameter_);

    /**
     * @brief Проверяет, виден ли объект невооружённым глазом.
     * @return true, если magnitude < 6; иначе false.
     */
    bool isVisibleToNakedEye() const;

    /**
     * @brief Вычисляет расстояние до объекта по формуле модуля расстояния.
     * @return Расстояние в парсеках.
     */
    double calculateDistance() const;

    /**
     * @brief Вычисляет угловой диаметр объекта.
     * @return Угловой диаметр в угловых минутах.
     */
    double calculateAngularDiameter() const;

    /**
     * @brief Устанавливает время восхода.
     *
     * @param hours Часы (0–23).
     * @param minutes Минуты (0–59).
     * @param seconds Секунды (0–59).
     * @throws std::invalid_argument если время некорректно.
     * @see TimeValidator::isValidTime
     */
    void setRiseTime(int hours, int minutes, int seconds);

    /**
     * @brief Устанавливает время захода.
     *
     * @param hours Часы (0–23).
     * @param minutes Минуты (0–59).
     * @param seconds Секунды (0–59).
     * @throws std::invalid_argument если время некорректно.
     * @see TimeValidator::isValidTime
     */
    void setSetTime(int hours, int minutes, int seconds);

    /**
     * @brief Проверяет, виден ли объект в указанное время.
     *
     * @param time Время для проверки.
     * @return true, если объект находится над горизонтом в это время
     *         (с учётом возможного пересечения полуночи).
     */
    bool isVisibleAtTime(const MyTime& time) const;
};

#endif // PLANETARIUMPROJECT_ASTRONOMICALOBJECT_H