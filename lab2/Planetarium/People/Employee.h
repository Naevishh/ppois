/**
 * @file Employee.h
 * @author Aleks
 * @brief Класс для представления сотрудника планетария.
 *
 * @details
 * Employee наследуется от Human и добавляет информацию о должности.
 * Используется для управления персоналом и расписанием.
 */

#ifndef PLANETARIUMPROJECT_EMPLOYEE_H
#define PLANETARIUMPROJECT_EMPLOYEE_H

#include <string>
#include "Human.h"
#include "../Utils/Enums.h"

/**
 * @brief Класс сотрудника планетария.
 *
 * Расширяет Human должностью (например, астроном, билетёр, техник).
 */
class Employee : public Human {
private:
    Enums::EmployeePosition position; ///< Должность сотрудника.

public:
    /**
     * @brief Конструктор сотрудника.
     *
     * @param name Имя сотрудника.
     * @param age Возраст в годах.
     * @param position_ Должность (например, ASTRONOMER, TICKET_SELLER).
     */
    Employee(std::string name, int age, Enums::EmployeePosition position_);

    /**
     * @brief Возвращает должность сотрудника.
     * @return Значение перечисления EmployeePosition.
     * @see Enums::EmployeePosition
     */
    Enums::EmployeePosition getPosition() const;
};

#endif // PLANETARIUMPROJECT_EMPLOYEE_H