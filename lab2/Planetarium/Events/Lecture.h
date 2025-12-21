/**
 * @file Lecture.h
 * @author Aleks
 * @brief Класс образовательной лекции в лекционном зале.
 *
 * @details
 * Lecture наследуется от Activity и представляет структурированное
 * образовательное мероприятие с темой, уровнем сложности и материалами.
 */

#ifndef PLANETARIUMPROJECT_LECTURE_H
#define PLANETARIUMPROJECT_LECTURE_H

#include "Activity.h"
#include "../Utils/Enums.h"
#include <vector>

class Auditorium;

/**
 * @brief Образовательная лекция.
 *
 * Поддерживает материалы, уровень сложности и автоматическое определение
 * необходимости проектора.
 */
class Lecture : public Activity {
private:
    Auditorium* auditorium;                 ///< Лекционный зал.
    Enums::Theme lectureTheme;              ///< Тема лекции (например, SOLAR_SYSTEM).
    int difficultyLevel;                    ///< Уровень сложности (1–10).
    std::vector<Enums::LectureMaterial> materials; ///< Используемые материалы.

public:
    /**
     * @brief Конструктор лекции.
     *
     * @param name Название лекции.
     * @param duration_ Продолжительность в часах.
     * @param theme_ Общая тематика мероприятия (например, EDUCATION).
     * @param auditorium_ Указатель на лекционный зал.
     * @param lectureTheme_ Астрономическая тема лекции.
     */
    Lecture(const std::string& name, double duration_, Enums::ActivityTheme theme_, Auditorium* auditorium_,
            Enums::Theme lectureTheme_);

    /**
     * @brief Проверяет, подходит ли лекция для детей.
     * @return true, если difficultyLevel < 5; иначе false.
     */
    bool isValidForChildren() const;

    /**
     * @brief Определяет, требуется ли проектор для лекции.
     * @return true, если среди материалов есть слайды или видео; иначе false.
     */
    bool isProjectorNeeded();

    /**
     * @brief Возвращает человекочитаемое название темы лекции.
     * @return Строка, например "Solar System".
     * @see Enums::themeToString
     */
    std::string getLectureTheme() const;

    /**
     * @brief Проводит лекцию в зале.
     *
     * @param date Дата проведения.
     * @return Строка с описанием лекции и датой.
     * @see Auditorium::holdLecture
     */
    std::string hold(const Date& date) override;

    /**
     * @brief Устанавливает уровень сложности.
     * @param level Целое число (рекомендуется 1–10).
     */
    void setDifficultyLevel(int level);

    /**
     * @brief Добавляет учебный материал к лекции.
     * @param material Тип материала (слайды, модели, видео и т.д.).
     */
    void addMaterial(Enums::LectureMaterial material);
};

#endif // PLANETARIUMPROJECT_LECTURE_H