/**
 * @file Activity.h
 * @author Aleks
 * @brief Базовый класс для всех видов мероприятий в планетарии.
 *
 * @details
 * Activity определяет общие свойства: название, продолжительность, место,
 * тематику, правила и требования к ведущему. Является родительским для
 * Stargazing, Observation, Lecture, Excursion и др.
 */

#ifndef PLANETARIUMPROJECT_ACTIVITY_H
#define PLANETARIUMPROJECT_ACTIVITY_H

#include "../Utils/Enums.h"
#include "../Utils/Date.h"
#include <vector>
#include <string>

class PlanetariumVenue;
class Employee;

/**
 * @brief Абстрактное мероприятие (активность) в планетарии.
 *
 * Может быть проведено только в открытом помещении и требует квалифицированного ведущего.
 */
class Activity {
private:
    std::string name;                                    ///< Название мероприятия.
    double duration;                                     ///< Продолжительность (в часах).
    Employee* host;                                      ///< Назначенный ведущий.
    std::vector<Enums::EmployeePosition> ableToHold;     ///< Должности, имеющие право вести.
    Enums::ActivityTheme theme;                          ///< Тематика (SCIENCE, EDUCATION и т.д.).
    PlanetariumVenue* activityPlace;                     ///< Помещение проведения.
    std::string rules;                                   ///< Правила поведения.

public:
    /**
     * @brief Конструктор базовой активности.
     *
     * @param name_ Название.
     * @param duration_ Продолжительность в часах.
     * @param theme_ Тематика мероприятия.
     * @param activityPlace_ Помещение, где проводится активность.
     */
    Activity(const std::string& name_, double duration_, Enums::ActivityTheme theme_, PlanetariumVenue* activityPlace_);

    /**
     * @brief Добавляет должность, имеющую право вести мероприятие.
     * @param position Должность (например, ASTRONOMER, LECTURER).
     */
    void addQualifiedPosition(Enums::EmployeePosition position);

    /**
     * @brief Устанавливает правила поведения.
     *
     * @param rules_ Текст правил (проходит валидацию).
     * @throws std::invalid_argument если правила содержат недопустимые символы.
     * @see StringValidator::validate
     */
    void setRules(const std::string& rules_);

    /**
     * @brief Проверяет, может ли сотрудник вести мероприятие.
     *
     * @param employee Сотрудник.
     * @return true, если его должность входит в ableToHold; иначе false.
     */
    bool canBeHeldBy(const Employee& employee);

    /**
     * @brief Назначает ведущего с проверкой квалификации.
     *
     * Если сотрудник подходит — назначается явно.
     * Иначе — автоматически выбирается из кураторов помещения.
     *
     * @param employee Указатель на сотрудника.
     * @see PlanetariumVenue::chooseCurator
     */
    void appointHost(Employee* employee);

    /**
     * @brief Принудительно устанавливает ведущего (без проверки квалификации).
     * @param employee Указатель на сотрудника.
     */
    void setHost(Employee* employee);

    /**
     * @brief Проверяет, возможно ли провести мероприятие сейчас.
     * @return true, если помещение открыто; иначе false.
     * @see PlanetariumVenue::IsOpen
     */
    bool isPossible();

    /**
 * @brief Возвращает название мероприятия.
 * @return Название в виде строки.
 */
    std::string getName() const;

/**
 * @brief Возвращает продолжительность мероприятия.
 * @return Продолжительность в часах.
 */
    double getDuration() const;

/**
 * @brief Возвращает указатель на назначенного ведущего (хоста).
 * @return Указатель на объект Employee или nullptr, если не назначен.
 */
    Employee* getHost() const;

/**
 * @brief Возвращает список должностей, имеющих право проводить мероприятие.
 * @return Вектор значений EmployeePosition.
 */
    std::vector<Enums::EmployeePosition> getAbleToHold() const;

/**
 * @brief Возвращает тематику мероприятия.
 * @return Значение перечисления ActivityTheme (например, SCIENCE, EDUCATION).
 */
    Enums::ActivityTheme getTheme() const;

/**
 * @brief Возвращает помещение, в котором проводится мероприятие.
 * @return Указатель на объект PlanetariumVenue.
 */
    PlanetariumVenue* getActivityPlace() const;

/**
 * @brief Возвращает помещение проведения (синоним для getActivityPlace).
 * @return Указатель на объект PlanetariumVenue.
 */
    PlanetariumVenue* getPlace() const;

    /**
     * @brief Выполняет мероприятие.
     *
     * Базовая реализация возвращает стандартное сообщение.
     * Должна быть переопределена в дочерних классах.
     *
     * @param date Дата проведения.
     * @return Строка с описанием.
     */
    virtual std::string hold(const Date& date);
};

#endif // PLANETARIUMPROJECT_ACTIVITY_H