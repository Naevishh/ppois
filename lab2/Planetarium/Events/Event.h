/**
 * @file Event.h
 * @author Aleks
 * @brief Класс комплексного мероприятия (события), объединяющего несколько активностей.
 *
 * @details
 * Event представляет собой организованное событие с датой, посетителями,
 * списком активностей и ответственным сотрудником.
 */

#ifndef PLANETARIUMPROJECT_EVENT_H
#define PLANETARIUMPROJECT_EVENT_H

#include <string>
#include <vector>
#include "../People/Visitor.h"
#include "../People/Employee.h"
#include "../Utils/Date.h"
#include "Activity.h"

/**
 * @brief Комплексное событие (например, день открытых дверей, фестиваль).
 *
 * Состоит из нескольких активностей и группы посетителей.
 */
class Event {
private:
    std::string eventName;               ///< Название события.
    Date eventDate;                      ///< Дата проведения.
    std::vector<Visitor*> visitors;      ///< Список посетителей.
    std::vector<Activity> activities;    ///< Список активностей (хранятся по значению).
    Employee* organizer;                 ///< Организатор события.

public:
    /**
     * @brief Конструктор события.
     *
     * @param eventName_ Название события.
     * @param eventDate_ Дата проведения.
     * @param visitorsNumber_ Ожидаемое количество посетителей (резервирует место в векторе).
     * @param organiser_ Указатель на организатора.
     */
    Event(std::string eventName_, Date eventDate_, int visitorsNumber_, Employee* organiser_);

    /**
     * @brief Возвращает название события.
     * @return Строка с названием.
     */
    std::string getName() const;

    /**
     * @brief Добавляет посетителя к событию.
     *
     * Проверяет, имеет ли посетитель билеты на все активности события.
     *
     * @param visitor Указатель на посетителя.
     * @throws BreakingRules если у посетителя нет доступа к хотя бы одной активности.
     * @see Visitor::canVisitVenue
     */
    void addVisitor(Visitor* visitor);

    /**
     * @brief Рассчитывает общую стоимость события для всех посетителей.
     * @return Общая сумма (в текущей реализации возвращает 0 — заглушка).
     * @note Метод требует доработки: не использует данные об активах или билетах.
     */
    double calculateWholePrice();

    /**
     * @brief Добавляет активность к событию.
     * @param activity Активность (копируется в вектор).
     */
    void includeActivity(const Activity& activity);

    /**
     * @brief Рассчитывает общую продолжительность события с перерывами.
     *
     * @param breakTime Длительность перерыва между активностями (в минутах).
     * @return Общая продолжительность в часах.
     * @throws std::invalid_argument если breakTime вне [0, 60].
     */
    double eventDuration(double breakTime) const;

    /**
     * @brief Возвращает текущее количество посетителей.
     * @return Число зарегистрированных посетителей.
     */
    int getVisitorsNumber() const;

    /**
     * @brief Возвращает имя организатора.
     * @return Строка с именем сотрудника.
     */
    std::string getOrganizerName() const;

    /**
     * @brief Устанавливает нового организатора.
     * @param organizer_ Указатель на сотрудника.
     */
    void setOrganizer(Employee* organizer_);
};

#endif // PLANETARIUMPROJECT_EVENT_H