/**
 * @file PlanetariumException.h
 * @author Aleks
 * @brief Базовый класс для всех пользовательских исключений в проекте PlanetariumProject.
 *
 * @details
 * PlanetariumException наследуется от std::exception и предоставляет
 * общий механизм хранения и возврата текстового сообщения об ошибке.
 * Все специфичные исключения проекта должны наследоваться от этого класса.
 */

#ifndef PLANETARIUMPROJECTCOPY_PLANETARIUMEXCEPTION_H
#define PLANETARIUMPROJECTCOPY_PLANETARIUMEXCEPTION_H

#include <exception>
#include <string>

/**
 * @brief Базовое исключение системы планетария.
 *
 * Используется как родительский класс для всех доменных исключений.
 */
class PlanetariumException : public std::exception {
private:
    std::string message; ///< Сообщение об ошибке.

public:
    /**
     * @brief Конструктор с пользовательским сообщением.
     * @param message_ Текст ошибки (перемещается во внутреннее поле).
     */
    explicit PlanetariumException(std::string message_);

    /**
     * @brief Возвращает сообщение об ошибке.
     * @return Указатель на C-строку с описанием.
     * @note Переопределяет метод std::exception::what().
     */
    const char* what() const noexcept override;
};

#endif // PLANETARIUMPROJECTCOPY_PLANETARIUMEXCEPTION_H