/**
 * @file AudioDevice.h
 * @author Aleks
 * @brief Базовый класс для аудиоустройств (микрофоны, динамики).
 *
 * @details
 * AudioDevice расширяет Device поддержкой аудиоэффектов и типов подключения.
 * Используется как основа для Speaker и Microphone.
 */

#ifndef PLANETARIUMPROJECT_AUDIODEVICE_H
#define PLANETARIUMPROJECT_AUDIODEVICE_H

#include "Device.h"
#include "../Utils/Enums.h"
#include <vector>

/**
 * @brief Абстрактный базовый класс аудиоустройства.
 *
 * Содержит информацию о поддерживаемых эффектах и интерфейсах подключения.
 */
class AudioDevice : public Device {
private:
    Enums::AudioEffectType effect;                    ///< Текущий аудиоэффект (NONE, REVERB и т.д.).
    std::vector<Enums::ConnectionType> connections;   ///< Поддерживаемые типы подключения.

public:
    /**
     * @brief Конструктор аудиоустройства.
     * @param name_ Название устройства.
     * @note По умолчанию эффект = NONE, список подключений пуст.
     */
    explicit AudioDevice(const std::string& name_);

    /**
     * @brief Устанавливает аудиоэффект.
     * @param effect_ Новое значение (EQUALIZER, REVERB, COMPRESSOR и т.д.).
     */
    void setEffect(Enums::AudioEffectType effect_);

    /**
     * @brief Возвращает список поддерживаемых типов подключения.
     * @return Вектор значений ConnectionType (USB, HDMI, BLUETOOTH и т.д.).
     */
    std::vector<Enums::ConnectionType> getConnections() const;

    /**
     * @brief Проверяет, поддерживает ли устройство указанный тип подключения.
     *
     * @param connection_ Тип подключения для проверки.
     * @return true, если connection_ содержится в списке connections; иначе false.
     */
    bool supportsConnection(Enums::ConnectionType connection_);
};

#endif // PLANETARIUMPROJECT_AUDIODEVICE_H