/**
 * @file AudioSystem.h
 * @author Aleks
 * @brief Класс для управления полной аудиосистемой (микрофоны + динамики + пульт).
 *
 * @details
 * AudioSystem объединяет микрофоны, динамики и RemoteControl в единое целое.
 * Поддерживает добавление/удаление устройств, расчёт энергопотребления
 * и проверку общей работоспособности.
 */

#ifndef PLANETARIUMPROJECT_AUDIOSYSTEM_H
#define PLANETARIUMPROJECT_AUDIOSYSTEM_H

#include <vector>
#include "Speaker.h"
#include "RemoteControl.h"
#include "Microphone.h"
#include "../Utils/Date.h"

/**
 * @brief Аудиосистема планетария.
 *
 * Управляет набором аудиоустройств как единым комплексом.
 */
class AudioSystem {
private:
    std::vector<Microphone*> mics;          ///< Список микрофонов.
    std::vector<Speaker*> speakers;         ///< Список динамиков.
    RemoteControl remoteControl;            ///< Пульт управления (содержит копии списков).

public:
    /**
     * @brief Конструктор по умолчанию.
     *
     * Инициализирует RemoteControl с текущими списками (изначально пустыми).
     */
    AudioSystem();

    /**
     * @brief Возвращает общее количество подключённых устройств.
     * @return Сумма микрофонов и динамиков.
     */
    int devicesCount();

    /**
     * @brief Рассчитывает общее энергопотребление динамиков.
     * @return Суммарная мощность в ваттах (только динамики).
     * @see Speaker::getPower
     */
    double totalPowerConsumption();

    /**
     * @brief Добавляет микрофон в систему и пульт.
     * @param mic Указатель на микрофон.
     */
    void addMicrophone(Microphone* mic);

    /**
     * @brief Добавляет динамик в систему и пульт.
     * @param speaker Указатель на динамик.
     */
    void addSpeaker(Speaker* speaker);

    /**
     * @brief Удаляет микрофон из системы.
     *
     * @param mic Указатель на микрофон.
     * @return true, если микрофон найден и удалён; иначе false.
     */
    bool removeMicrophone(Microphone* mic);

    /**
     * @brief Удаляет динамик из системы.
     *
     * @param speaker Указатель на динамик.
     * @return true, если динамик найден и удалён; иначе false.
     */
    bool removeSpeaker(Speaker* speaker);

    /**
     * @brief Проверяет, пригодна ли вся аудиосистема к использованию.
     *
     * @param date Текущая дата.
     * @return true, если все микрофоны и динамики могут быть использованы;
     *         иначе false.
     * @see Device::canBeUsed
     */
    bool canBeUsed(const Date& date);

    /**
     * @brief Выполняет базовую настройку системы.
     *
     * Включает все устройства и устанавливает среднюю громкость +10.
     * @see RemoteControl::TurnAllOn, RemoteControl::changeAllVolume
     */
    void setUpSystem();
};

#endif // PLANETARIUMPROJECT_AUDIOSYSTEM_H