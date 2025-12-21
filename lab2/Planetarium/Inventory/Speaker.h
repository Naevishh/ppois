/**
 * @file Speaker.h
 * @author Aleks
 * @brief Класс для представления акустической системы (динамика).
 *
 * @details
 * Speaker наследуется от AudioDevice и управляет громкостью,
 * потреблением энергии и воспроизведением звука.
 */

#ifndef PLANETARIUMPROJECT_SPEAKER_H
#define PLANETARIUMPROJECT_SPEAKER_H

#include "AudioDevice.h"

/**
 * @brief Класс динамика.
 *
 * Поддерживает управление громкостью и отслеживание состояния воспроизведения.
 */
class Speaker : public AudioDevice {
private:
    double volumeLevel;       ///< Текущий уровень громкости (0–30).
    double powerConsumption;  ///< Потребляемая мощность в ваттах.

public:
    /**
     * @brief Конструктор динамика.
     * @param name Название устройства.
     * @note По умолчанию громкость = 0, мощность = 600 Вт.
     */
    explicit Speaker(const std::string& name);

    /**
     * @brief Устанавливает уровень громкости.
     *
     * @param volume Желаемый уровень (ограничен диапазоном [0, 30]).
     * @note Значения вне диапазона автоматически ограничиваются.
     */
    void setVolume(double volume);

    /**
     * @brief Запускает воспроизведение с заданной громкостью.
     *
     * @param volumeLevel_ Уровень громкости (не ограничен в методе — см. setVolume).
     * @note Если устройство выключено, оно автоматически включается.
     */
    void startPlayback(double volumeLevel_);

    /**
     * @brief Останавливает воспроизведение (устанавливает громкость в 0).
     */
    void stopPlayback();

    /**
     * @brief Возвращает текущий уровень громкости.
     * @return Число в диапазоне [0, 30].
     */
    double getVolume() const;

    /**
     * @brief Возвращает потребляемую мощность.
     * @return Мощность в ваттах (фиксировано 600 Вт).
     */
    double getPower() const;
};

#endif // PLANETARIUMPROJECT_SPEAKER_H