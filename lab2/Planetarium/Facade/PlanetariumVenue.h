/**
 * @file PlanetariumVenue.h
 * @author Aleks
 * @brief Базовый класс для любого помещения планетария (зал, выставочный зал и т.д.).
 *
 * @details
 * PlanetariumVenue управляет вместимостью, графиком работы, ценой билета,
 * персоналом и посетителями. Может проводить мероприятия и события.
 */

#ifndef PLANETARIUMPROJECT_PLANETARIUMVENUE_H
#define PLANETARIUMPROJECT_PLANETARIUMVENUE_H

#include <string>
#include <vector>
#include "../People/Employee.h"
#include "../Service/Schedule.h"
#include "../Utils/MyTime.h"

class Date;
class Activity;
class Event;
class Lecture;
class Ticket;

/**
 * @brief Абстрактное помещение планетария.
 *
 * Может быть залом, выставочным пространством, лекционной и т.д.
 */
class PlanetariumVenue {
private:
    std::string name;                     ///< Название помещения.
    int capacity;                         ///< Максимальное количество посетителей.
    std::vector<Employee*> curators;      ///< Список кураторов/ведущих.
    bool isOpen;                          ///< Открыто ли помещение.
    int currentVisitors;                  ///< Текущее количество посетителей.
    double ticketPrice;                   ///< Цена билета.
    Schedule schedule;                    ///< График работы.

public:
    /**
     * @brief Конструктор помещения.
     *
     * @param name_ Название.
     * @param capacity_ Вместимость (≥ 0).
     * @note По умолчанию: закрыто, цена билета = 30, график = 08:00–20:00.
     */
    PlanetariumVenue(std::string name_, int capacity_);

    /**
     * @brief Открывает помещение для посетителей.
     */
    void openVenue();

    /**
     * @brief Закрывает помещение и сбрасывает число посетителей.
     */
    void closeVenue();

    /**
     * @brief Назначает случайного куратора для мероприятия.
     *
     * @param activity Мероприятие, для которого требуется ведущий.
     * @note Если список кураторов пуст — ничего не происходит.
     */
    void chooseCurator(Activity* activity);

    /**
     * @brief Проводит событие в помещении.
     *
     * @param event Событие с указанием числа ожидаемых посетителей.
     * @return Строка с описанием события или ошибкой.
     * @throws VenueClosedException если помещение закрыто.
     * @throws CapacityExceededException если не хватает мест.
     */
    std::string hostEvent(const Event& event);

    /**
     * @brief Добавляет посетителей в помещение.
     *
     * @param visitorsNumber Количество новых посетителей.
     * @throws std::invalid_argument если число отрицательное.
     * @throws CapacityExceededException если превышена вместимость.
     */
    void addVisitors(int visitorsNumber);

    /**
     * @brief Удаляет посетителей из помещения.
     *
     * @param visitorsNumber Количество уходящих посетителей.
     * @throws std::invalid_argument если число отрицательное.
     * @throws VenueIsEmpty если в зале никого нет.
     * @throws std::out_of_range если уходит больше, чем находится.
     */
    void removeVisitors(int visitorsNumber);

    /**
     * @brief Устанавливает цену билета.
     *
     * @param price Новая цена (≥ 0).
     * @throws std::invalid_argument если цена отрицательная.
     */
    void setTicketPrice(double price);

    /**
     * @brief Добавляет куратора в список персонала.
     *
     * @param curator Указатель на сотрудника.
     * @throws std::invalid_argument если curator == nullptr.
     */
    void addCurator(Employee* curator);

    /**
     * @brief Настраивает график работы.
     *
     * @param openingHour Час открытия.
     * @param openingMinutes Минуты открытия.
     * @param workdayDuration Продолжительность рабочего дня (в часах).
     * @param lunchStartHour Час начала обеда.
     * @param lunchStartMinutes Минуты начала обеда.
     * @param lunchDuration Длительность обеда (в минутах).
     */
    void setSchedule(int openingHour, int openingMinutes, int workdayDuration, int lunchStartHour,
                     int lunchStartMinutes, int lunchDuration);

    /**
 * @brief Возвращает название помещения.
 * @return Название в виде строки.
 */
    std::string getName() const;

/**
 * @brief Возвращает максимальную вместимость помещения.
 * @return Максимальное количество посетителей.
 */
    int getCapacity() const;

/**
 * @brief Возвращает список кураторов (сотрудников), закреплённых за помещением.
 * @return Вектор указателей на объекты Employee.
 */
    std::vector<Employee*> getCurators() const;

/**
 * @brief Проверяет, открыто ли помещение для посетителей.
 * @return true, если открыто; иначе false.
 */
    bool IsOpen() const;

/**
 * @brief Возвращает текущее количество посетителей в помещении.
 * @return Число посетителей (≥ 0).
 */
    int getCurrentVisitors() const;

/**
 * @brief Возвращает текущую цену билета в это помещение.
 * @return Цена в денежных единицах.
 */
    double getTicketPrice() const;

/**
 * @brief Возвращает время открытия помещения.
 * @return Объект MyTime с часами и минутами открытия.
 */
    MyTime getOpeningTime() const;

/**
 * @brief Возвращает время закрытия помещения.
 * @return Объект MyTime с часами и минутами закрытия.
 */
    MyTime getClosingTime() const;

/**
 * @brief Возвращает время начала обеденного перерыва.
 * @return Объект MyTime с часами и минутами начала обеда.
 */
    MyTime getLunchStart() const;

/**
 * @brief Возвращает время окончания обеденного перерыва.
 * @return Объект MyTime с часами и минутами конца обеда.
 */
    MyTime getLunchEnd() const;
};

#endif // PLANETARIUMPROJECT_PLANETARIUMVENUE_H