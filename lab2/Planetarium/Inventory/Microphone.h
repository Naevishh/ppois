/**
 * @file Microphone.h
 * @author Aleks
 * @brief Класс микрофона как аудиоустройства с поддержкой подключения к динамику.
 *
 * @details
 * Microphone наследуется от AudioDevice и может быть подвижным (на стойке или нет),
 * а также подключаться к одному динамику через уникальный указатель.
 */

#ifndef PLANETARIUMPROJECT_MICROPHONE_H
#define PLANETARIUMPROJECT_MICROPHONE_H

#include "AudioDevice.h"
#include "Speaker.h"
#include <memory>

/**
 * @brief Класс микрофона.
 *
 * Поддерживает монтаж на стойку и подключение к совместимому динамику.
 */
class Microphone : public AudioDevice {
private:
    bool isMovable;                            ///< Может ли микрофон перемещаться (true = не на стойке).
    std::unique_ptr<Speaker> connectedSpeaker; ///< Динамик, к которому подключён микрофон.

public:
    /**
     * @brief Конструктор микрофона.
     *
     * @param name Имя устройства.
     * @param isWireless_ Флаг беспроводности (в текущей реализации не используется напрямую).
     * @note По умолчанию микрофон подвижен и не подключён к динамику.
     */
    Microphone(const std::string& name, bool isWireless_);

    /**
     * @brief Монтирует микрофон на неподвижную стойку.
     * @note После монтажа isMovable становится false.
     */
    void mountOnStand();

    /**
     * @brief Подключает микрофон к динамику через совместимый интерфейс.
     *
     * @param speaker Умный указатель на динамик.
     * @throws DeviceSwitchedOff если динамик выключен.
     * @note Подключение происходит только если хотя бы один тип соединения
     *       (из getConnections()) поддерживается динамиком (см. Speaker::supportsConnection).
     */
    void connectToSpeaker(std::unique_ptr<Speaker> speaker);
};

#endif // PLANETARIUMPROJECT_MICROPHONE_H