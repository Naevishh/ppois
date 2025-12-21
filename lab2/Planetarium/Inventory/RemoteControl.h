/**
 * @file RemoteControl.h
 * @author Aleks
 * @brief Класс для централизованного управления аудиоустройствами (микрофонами и динамиками).
 *
 * @details
 * RemoteControl объединяет несколько микрофонов и динамиков, позволяя
 * включать их одновременно, регулировать громкость синхронно или независимо,
 * а также отслеживать средний уровень громкости.
 */

#ifndef PLANETARIUMPROJECT_REMOTECONTROL_H
#define PLANETARIUMPROJECT_REMOTECONTROL_H

#include <vector>
#include "AudioDevice.h"
#include "Speaker.h"
#include "Microphone.h"

/**
 * @brief Класс пульта дистанционного управления аудиосистемой.
 *
 * Поддерживает управление группой Microphone и Speaker.
 */
class RemoteControl {
private:
    std::vector<Microphone*> mics;      ///< Список подключённых микрофонов.
    std::vector<Speaker*> speakers;     ///< Список подключённых динамиков.

public:
    /**
     * @brief Конструктор с инициализацией списков устройств.
     * @param mics_ Вектор указателей на микрофоны.
     * @param speakers_ Вектор указателей на динамики.
     */
    RemoteControl(std::vector<Microphone*> mics_, std::vector<Speaker*> speakers_);

    /**
     * @brief Включает все микрофоны и динамики.
     *
     * Для каждого устройства проверяется текущее состояние: если выключено — включается.
     * @see AudioDevice::active, AudioDevice::turnOn
     */
    void TurnAllOn();

    /**
     * @brief Изменяет громкость всех динамиков.
     *
     * @param difference Изменение громкости (положительное — громче, отрицательное — тише).
     * @param synchronize Если true — все динамики устанавливаются на (средняя громкость + difference);
     *                    если false — к каждому прибавляется difference.
     * @note Динамики с нулевой громкостью игнорируются при расчёте среднего.
     */
    void changeAllVolume(int difference, bool synchronize);

    /**
     * @brief Устанавливает одинаковую громкость для всех динамиков.
     * @param newVolume Новое значение громкости (применяется ко всем, включая выключенные).
     * @note Реализован через changeAllVolume(0, true) с последующей коррекцией.
     */
    void setAllVolumes(double newVolume);

    /**
     * @brief Добавляет микрофон в управляемый список.
     * @param newMic Указатель на микрофон.
     */
    void addMicrophone(Microphone* newMic);

    /**
     * @brief Добавляет динамик в управляемый список.
     * @param newSpeaker Указатель на динамик.
     */
    void addSpeaker(Speaker* newSpeaker);

    /**
     * @brief Вычисляет среднюю громкость активных динамиков.
     * @return Среднее арифметическое громкости (игнорируются динамики с volume = 0).
     *         Возвращает 0, если нет динамиков или все выключены.
     */
    double getAverageVolume() const;

    /**
     * @brief Увеличивает громкость всех динамиков на 2 единицы.
     * @see changeAllVolume
     */
    void allVolumeUp();

    /**
     * @brief Уменьшает громкость всех динамиков на 2 единицы.
     * @see changeAllVolume
     */
    void allVolumeDown();
};

#endif // PLANETARIUMPROJECT_REMOTECONTROL_H