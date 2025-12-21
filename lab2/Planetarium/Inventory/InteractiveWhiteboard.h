/**
 * @file InteractiveWhiteboard.h
 * @author Aleks
 * @brief Класс интерактивной доски — расширение Screen с поддержкой инструментов и лекций.
 *
 * @details
 * InteractiveWhiteboard наследуется от Screen и добавляет функционал
 * для работы в режиме лекции: выбор пера, цвета, ширины линии,
 * очистка экрана, поддержка мультитача и подготовка к проекции.
 */

#ifndef PLANETARIUMPROJECT_INTERACTIVEWHITEBOARD_H
#define PLANETARIUMPROJECT_INTERACTIVEWHITEBOARD_H

#include "Device.h"
#include "Screen.h"
#include "../Utils/Enums.h"

/**
 * @brief Интерактивная доска для лекций и проекций.
 */
class InteractiveWhiteboard : public Screen {
public:
    /**
     * @brief Структура, описывающая текущий инструмент рисования.
     */
    struct Tool {
        Enums::ToolColor color; ///< Цвет инструмента.
        Enums::ToolType type;   ///< Тип инструмента (перо, ластик, маркер и т.д.).
        int width;              ///< Толщина линии (в пикселях или условных единицах).

        /**
         * @brief Конструктор по умолчанию.
         *
         * Инициализирует: чёрное перо, ширина 5.
         */
        Tool();
    };

private:
    std::string content;        ///< Текущее содержимое доски.
    Tool currentTool;           ///< Текущий активный инструмент.
    bool multiTouch;            ///< Включена ли поддержка мультитача.

public:
    /**
     * @brief Конструктор интерактивной доски.
     *
     * @param name Название устройства.
     * @param width_ Ширина экрана в метрах.
     * @param length_ Длина (высота) экрана в метрах.
     */
    InteractiveWhiteboard(const std::string& name, double width_, double length_);

    /**
     * @brief Подготавливает доску к режиму проекции.
     *
     * Очищает экран и выключает устройство.
     * @note Используется, когда доска временно заменяется проектором.
     */
    void readyForProjection();

    /**
     * @brief Устанавливает базовый инструмент: чёрное перо, ширина 5.
     * @see selectTool, setPenColor, setPenWidth
     */
    void setBasicTool();

    /**
     * @brief Переводит доску в режим лекции.
     *
     * Включает устройство (если выключено), очищает экран,
     * устанавливает базовый инструмент и отключает мультитач.
     */
    void readyForLecture();

    /**
     * @brief Включает поддержку мультитача.
     */
    void enableMultiTouch();

    /**
     * @brief Очищает содержимое доски.
     */
    void clearScreen();

    /**
     * @brief Выбирает тип инструмента.
     * @param type_ Новый тип (PEN, HIGHLIGHTER, ERASER и т.д.).
     */
    void selectTool(Enums::ToolType type_);

    /**
     * @brief Устанавливает цвет пера (или другого инструмента).
     * @param color_ Новый цвет (BLACK, RED, BLUE и т.д.).
     */
    void setPenColor(Enums::ToolColor color_);

    /**
     * @brief Устанавливает толщину линии.
     *
     * @param width_ Новое значение (должно быть в диапазоне [0, 30]).
     * @throws std::invalid_argument если ширина вне допустимого диапазона.
     */
    void setPenWidth(int width_);

    /**
     * @brief Возвращает текущий инструмент.
     * @return Копия структуры Tool.
     */
    Tool getTool() const;
};

#endif // PLANETARIUMPROJECT_INTERACTIVEWHITEBOARD_H