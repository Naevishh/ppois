/**
 * @file Projector.h
 * @author Aleks
 * @brief Базовый класс проектора с поддержкой основных параметров проекции.
 *
 * @details
 * Projector наследуется от Device и управляет яркостью, расстоянием проекции,
 * технологией, разрешением и источником света. Может проецировать на Screen.
 */

#ifndef PLANETARIUMPROJECT_PROJECTOR_H
#define PLANETARIUMPROJECT_PROJECTOR_H

#include "Device.h"
#include "Screen.h"
#include "../Utils/Enums.h"

/**
 * @brief Базовый класс проектора.
 *
 * Предназначен для обычных (не купольных) проекционных систем.
 */
class Projector : public Device {
private:
    Enums::ProjectionTechnology technology; ///< Технология проекции (DLP, LCD и т.д.).
    Enums::StandardResolution resolution;   ///< Поддерживаемое разрешение.
    Enums::LightSource lamp;                ///< Тип источника света.
    double brightness;                      ///< Яркость (в люменах).
    double throwDistance;                   ///< Текущее расстояние до экрана (в метрах).
    double throwRatio;                      ///< Соотношение throw (расстояние / ширина экрана).
    double fov;                             ///< Угол обзора (поле зрения) в градусах.

public:
    /**
     * @brief Конструктор проектора.
     *
     * @param name_ Название устройства.
     * @param brightness_ Начальная яркость (в люменах).
     * @param throwRatio_ Throw-коэффициент (расстояние / размер экрана).
     * @param fov_ Угол обзора в градусах.
     */
    Projector(std::string name_, double brightness_, double throwRatio_, double fov_);

    /**
     * @brief Регулирует яркость проектора.
     * @param level Изменение яркости (может быть отрицательным).
     */
    void adjustBrightness(int level);

    /**
     * @brief Устанавливает размер проекции и обновляет расстояние до экрана.
     *
     * @param screenSize Размер экрана (обычно ширина или высота в метрах).
     * @throws std::invalid_argument если размер вне допустимого диапазона [0, 15].
     */
    virtual void setProjectionSize(double screenSize);

    /**
     * @brief Производит проекцию на указанный экран.
     *
     * @param screen Указатель на экран.
     * @note Автоматически включает проектор, если выключен.
     *       Размер проекции устанавливается по высоте экрана.
     */
    virtual void project(Screen* screen);

    // --- Сеттеры ---

    /**
     * @brief Устанавливает расстояние до экрана.
     * @param throwDistance_ Новое расстояние (в метрах).
     * @throws std::invalid_argument если значение отрицательное.
     */
    void setThrowDistance(double throwDistance_);

    /**
     * @brief Устанавливает технологию проекции.
     * @param tech Новое значение (DLP, LCD, LCOS).
     */
    void setTechnology(Enums::ProjectionTechnology tech);

    /**
     * @brief Устанавливает стандарт разрешения.
     * @param res Новое значение (FULL_HD, UHD_4K и т.д.).
     */
    void setResolution(Enums::StandardResolution res);

    /**
     * @brief Устанавливает тип источника света.
     * @param light Новое значение (LED, LASER, LAMP_LIFE).
     */
    void setLamp(Enums::LightSource light);

    /**
     * @brief Возвращает текущую яркость проектора.
     * @return Яркость в люменах (или в условных единицах, принятых в системе).
     */
    double getBrightness() const;
    
    /**
     * @brief Возвращает текущее расстояние от проектора до экрана.
     * @return Расстояние в метрах.
     */
    double getThrowDistance() const;
    
    /**
     * @brief Возвращает коэффициент throw (соотношение расстояния к размеру изображения).
     * @return Безразмерное число (например, 1.5 означает: 1.5 м на 1 м ширины экрана).
     */
    double getThrowRatio() const;
    
    /**
     * @brief Возвращает угол поля зрения (Field of View) проектора.
     * @return Угол в градусах.
     */
    double getFov() const;
    };

#endif // PLANETARIUMPROJECT_PROJECTOR_H
