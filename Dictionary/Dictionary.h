/**
 * @file Dictionary.h
 * @brief Заголовочный файл класса dictionary - словаря английских слов с переводами
 * @author Ященко Александра
 */

#ifndef SEM3_L1_PPOIS_DICTIONARY_H
#define SEM3_L1_PPOIS_DICTIONARY_H

#include <string>
#include "Binary_tree.h"

/**
 * @class dictionary
 * @brief Класс словаря для хранения пар "английское слово - русский перевод"
 * @details Класс реализует словарь с использованием бинарного дерева поиска (AVL-дерева).
 * Предоставляет операции добавления, удаления, поиска слов, а также ввода/вывода.
 * Словарь автоматически поддерживает сбалансированность дерева для обеспечения
 * эффективного доступа к элементам.
 */
class dictionary{
private:
    binary_tree<std::string, std::string> dictionary_tree; ///< Бинарное дерево для хранения пар слово-перевод

public:
    /**
     * @brief Проверяет наличие слова в словаре
     * @param[in] english_word Английское слово для поиска
     * @return true если слово найдено, false в противном случае
     */
    bool contains_word(const std::string& english_word) const;

    /**
     * @brief Оператор доступа к переводу слова (константная версия)
     * @param[in] input_word Английское слово
     * @return Константная ссылка на русский перевод
     * @see operator[](const std::string&)
     */
    const std::string& operator[](const std::string& input_word) const;

    /**
     * @brief Оператор доступа к переводу слова
     * @param[in] input_word Английское слово
     * @return Ссылка на русский перевод
     * @see operator[](const std::string&) const
     */
    std::string& operator[](const std::string& input_word);

    /**
     * @brief Оператор вывода словаря в поток
     * @param[out] output Выходной поток
     * @param[in] dictionary Словарь для вывода
     * @return Ссылка на выходной поток
     * @see operator>>
     */
    friend std::ostream& operator<<(std::ostream& output, const dictionary& dictionary);

    /**
     * @brief Оператор ввода словаря из потока
     * @param[in] input Входной поток
     * @param[out] dictionary Словарь для заполнения
     * @return Ссылка на входной поток
     * @see operator<<
     */
    friend std::istream& operator>>(std::istream& input, dictionary& dictionary);

    /**
     * @brief Добавление пары слово-перевод в словарь
     * @param[in] english_russian_pair Пара "английское слово - русский перевод"
     * @return Ссылка на текущий объект словаря
     * @throw std::invalid_argument если слово уже существует в словаре
     * @see operator+=(const std::pair<const char*, const char*>&)
     * @see operator-=
     */
    dictionary& operator+=(const std::pair<std::string, std::string>& english_russian_pair);

    /**
     * @brief Добавление пары слово-перевод в словарь (версия для C-строк)
     * @param[in] english_russian_pair Пара "английское слово - русский перевод" в виде C-строк
     * @return Ссылка на текущий объект словаря
     * @see operator+=(const std::pair<std::string, std::string>&)
     * @see operator-=
     */
    dictionary& operator+=(const std::pair<const char*, const char*>& english_russian_pair);

    /**
     * @brief Удаление слова из словаря
     * @param[in] english_word Английское слово для удаления
     * @return Ссылка на текущий объект словаря
     * @see operator+=
     */
    dictionary& operator-=(const std::string& english_word);

    /**
     * @brief Оператор сравнения словарей на равенство
     * @param[in] other Словарь для сравнения
     * @return true если словари идентичны, false в противном случае
     * @see operator!=
     */
    bool operator==(const dictionary& other) const;

    /**
     * @brief Оператор сравнения словарей на неравенство
     * @param[in] other Словарь для сравнения
     * @return true если словари различаются, false в противном случае
     * @see operator==
     */
    bool operator!=(const dictionary& other) const;

    /**
     * @brief Получение количества слов в словаре
     * @return Количество пар слово-перевод в словаре
     * @see is_empty
     */
    int get_size() const;

    /**
     * @brief Проверка пустоты словаря
     * @return true если словарь пуст, false в противном случае
     * @see get_size
     */
    bool is_empty() const;

    /**
     * @brief Чтение словаря из файла
     * @param[in] file_name Имя файла для чтения
     * @details Файл должен содержать пары "английское слово - русский перевод",
     * разделенные переводом строки. Некорректные строки игнорируются.
     * @see operator>>
     */
    void read_from_file(const std::string& file_name);
};

#endif //SEM3_L1_PPOIS_DICTIONARY_H