/**
 * @file Device.h
 * @author Aleks
 * @brief Базовый класс для всех технических устройств в планетарии.
 *
 * @details
 * Device инкапсулирует общие свойства оборудования: состояние (включено/выключено),
 * дату окончания гарантии, дату последнего ТО, интервал обслуживания.
 * Предоставляет методы для проверки пригодности к использованию.
 */

#ifndef PLANETARIUMPROJECT_DEVICE_H
#define PLANETARIUMPROJECT_DEVICE_H

#include "../Utils/Date.h"
#include <string>

/**
 * @brief Абстрактный базовый класс устройства.
 *
 * Используется как основа для проекторов, динамиков, микрофонов, экранов и т.д.
 */
class Device {
private:
    std::string name;                   ///< Название устройства.
    bool isActive;                      ///< Включено ли устройство.
    Date warrantyExpiryDate;            ///< Дата окончания гарантии.
    Date lastMaintenance;               ///< Дата последнего технического обслуживания.
    int maintenanceInterval;            ///< Интервал ТО в годах.

public:
    /**
     * @brief Конструктор устройства.
     *
     * @param name_ Название устройства.
     * @note По умолчанию: выключено, гарантия = текущая дата + 3 года,
     *       последнее ТО = сегодня, интервал = 1 год.
     */
    explicit Device(std::string name_);

    /**
     * @brief Включает устройство.
     */
    void turnOn();

    /**
     * @brief Выключает устройство.
     */
    void turnOff();

    /**
     * @brief Устанавливает интервал технического обслуживания.
     * @param interval Интервал в годах.
     */
    void setMaintenanceInterval(int interval);

    /**
     * @brief Устанавливает дату последнего техобслуживания.
     *
     * @param year_ Год.
     * @param month_ Месяц (1–12).
     * @param day_ День (1–31).
     */
    void setlastMaintenance(int year_, int month_, int day_);

    /**
     * @brief Проверяет, включено ли устройство.
     * @return true, если включено; иначе false.
     */
    bool active() const;

    /**
     * @brief Проверяет, действует ли гарантия на текущую дату.
     *
     * @param currentDate Текущая дата.
     * @return true, если currentDate < warrantyExpiryDate; иначе false.
     */
    bool isUnderWarranty(const Date& currentDate) const;

    /**
     * @brief Проверяет, требуется ли техобслуживание.
     *
     * @param currentDate Текущая дата.
     * @return true, если currentDate > (lastMaintenance + maintenanceInterval); иначе false.
     */
    bool needsMaintenance(const Date& currentDate);

    /**
     * @brief Проверяет, можно ли использовать устройство сегодня.
     *
     * @param currentDate Текущая дата.
     * @return true, если устройство на гарантии и не требует ТО; иначе false.
     * @see isUnderWarranty, needsMaintenance
     */
    bool canBeUsed(const Date& currentDate);

    /**
     * @brief Возвращает название устройства.
     * @return Строка с именем.
     */
    std::string getName() const;

    /**
     * @brief Возвращает дату окончания гарантии.
     * @return Объект Date.
     */
    Date getWarrantyExpiryDate() const;

    /**
     * @brief Возвращает дату последнего ТО.
     * @return Объект Date.
     */
    Date getLastMaintenance() const;

    /**
     * @brief Возвращает интервал ТО (в годах).
     * @return Целое число.
     */
    int getMaintenanceInterval() const;
};

#endif // PLANETARIUMPROJECT_DEVICE_H