/**
 * @file Enums.h
 * @author Aleks
 * @brief Файл с перечислениями, используемыми в проекте PlanetariumProject.
 *
 * @details
 * Содержит все основные перечисления: погода, типы объектов, спектральные классы,
 * должности сотрудников, технологии проекции и др. Также включает вспомогательную
 * функцию преобразования themeToString.
 */

#ifndef PLANETARIUMPROJECT_ENUMS_H
#define PLANETARIUMPROJECT_ENUMS_H

#include <string>

/**
 * @brief Контейнер для всех перечислений проекта.
 *
 * Все перечисления объявлены как public и доступны через Enums::Name.
 */
class Enums {
public:
    /**
     * @brief Перечисление возможных погодных условий.
     */
    enum class WeatherCondition {
        SUNNY,          ///< Солнечно
        CLOUDY,         ///< Облачно
        PARTLY_CLOUDY,  ///< Переменная облачность
        RAINY,          ///< Дождливо
        STORMY,         ///< Гроза
        SNOWY,          ///< Снег
        FOGGY,          ///< Туман
        WINDY,          ///< Ветрено
        HAZY            ///< Дымка
    };

    /**
     * @brief Типы астрономических объектов.
     */
    enum class ObjectType {
        STAR, PLANET, MOON, GALAXY, NEBULA, STAR_CLUSTER,
        ASTEROID, COMET, QUASAR, BLACK_HOLE, CONSTELLATION
    };

    /**
     * @brief Спектральные классы звёзд (по системе Моргана — Кинана).
     */
    enum class SpectralClass { O, B, A, F, G, K, M };

    /**
     * @brief Типы планет.
     */
    enum PlanetType {
        TERRESTRIAL, GAS_GIANT, ICE_GIANT, DWARF, SUPER_EARTH,
        NEPTUNIAN, PROTOPLANET, EXOPLANET, HYCEAN, CHTHONIAN
    };

    /**
     * @brief Типы телескопов.
     */
    enum class TelescopeType { REFRACTOR, REFLECTOR, CATADIOPTRIC };

    /**
     * @brief Стандарты разрешения проекции.
     */
    enum class StandardResolution {
        FULL_HD, QHD, UHD_4K, UHD_8K, FULHDOME_2K, FULHDOME_4K
    };

    /**
     * @brief Категории льгот для посетителей.
     */
    enum class DiscountCategory {
        NONE, STUDENT, PUPIL, SENIOR, DISABLED, VETERAN, EMPLOYEE
    };

    /**
     * @brief Типы аудиоэффектов.
     */
    enum class AudioEffectType {
        NONE, EQUALIZER, REVERB, DELAY, CHORUS, FLANGER, DISTORTION,
        COMPRESSOR, BASS_BOOST, SURROUND
    };

    /**
     * @brief Встроенные демонстрационные шоу планетария.
     */
    enum class BuiltInPlanetariumShow {
        CALIBRATION_GRID, TEST_PATTERN, STARFIELD_DEMO, SOLAR_SYSTEM_DEMO,
        CONSTELLATION_DEMO, DAY_NIGHT_CYCLE, MILKY_WAY_PREVIEW,
        PLANETARY_MOTION, ZENITH_DEMONSTRATION
    };

    /**
     * @brief Цвета инструментов аннотации.
     */
    enum class ToolColor {
        BLACK, WHITE, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, GRAY, TRANSPARENT
    };

    /**
     * @brief Типы инструментов аннотации.
     */
    enum class ToolType {
        PEN, HIGHLIGHTER, ERASER, LINE, RECTANGLE, CIRCLE, ARROW,
        TEXT, SELECT, IMAGE, STICKER
    };

    /**
     * @brief Должности сотрудников планетария.
     */
    enum class EmployeePosition {
        DIRECTOR, MANAGER, DEPUTY_DIRECTOR, ASTRONOMER, LECTURER, PRESENTER,
        TOUR_GUIDE, EDUCATION_COORDINATOR, TECHNICIAN, PROJECTIONIST,
        TICKET_SELLER, CASHIER, SECURITY_GUARD, CLEANER, VOLUNTEER
    };

    /**
     * @brief Технологии проекции.
     */
    enum class ProjectionTechnology { DLP, LCD, LCOS };

    /**
     * @brief Источники света в проекторах.
     */
    enum class LightSource { LED, LASER, LAMP_LIFE };

    /**
     * @brief Типы подключения оборудования.
     */
    enum class ConnectionType {
        USB, USB_C, HDMI, AUX_3_5MM, BLUETOOTH, OPTICAL, RCA, XLR, TRS, WIFI
    };

    /**
     * @brief Тематики лекций и шоу.
     */
    enum class Theme {
        ASTRONOMY, SOLAR_SYSTEM, EXOPLANETS, STARS_FORMATION, GALAXIES_COSMOLOGY,
        ASTRONOMY_HISTORY, SPACE_EXPLORATION, SPACE_EXPLORATION_HISTORY,
        ANCIENT_ASTRONOMY, ROCKET_SCIENCE, SPACE_TELESCOPES, PLANETARY_SCIENCE,
        ASTROPHYSICS, ASTROBIOLOGY, SPACE_MISSIONS, FUTURE_SPACE_EXPLORATION,
        SPACE_COLONIZATION
    };

    /**
     * @brief Преобразует Theme в человекочитаемую строку.
     * @param theme Элемент перечисления Theme.
     * @return Строка, например "Solar System".
     */
    static std::string themeToString(Theme theme) {
        switch (theme) {
            case Theme::ASTRONOMY: return "Astronomy";
            case Theme::SOLAR_SYSTEM: return "Solar System";
            case Theme::EXOPLANETS: return "Exoplanets";
            case Theme::STARS_FORMATION: return "Stars Formation";
            case Theme::GALAXIES_COSMOLOGY: return "Galaxies and Cosmology";
            case Theme::ASTRONOMY_HISTORY: return "Astronomy History";
            case Theme::SPACE_EXPLORATION_HISTORY: return "Space Exploration History";
            case Theme::ANCIENT_ASTRONOMY: return "Ancient Astronomy";
            case Theme::ROCKET_SCIENCE: return "Rocket Science";
            case Theme::SPACE_TELESCOPES: return "Space Telescopes";
            case Theme::PLANETARY_SCIENCE: return "Planetary Science";
            case Theme::ASTROPHYSICS: return "Astrophysics";
            case Theme::ASTROBIOLOGY: return "Astrobiology";
            case Theme::SPACE_MISSIONS: return "Space Missions";
            case Theme::FUTURE_SPACE_EXPLORATION: return "Future Space Exploration";
            case Theme::SPACE_COLONIZATION: return "Space Colonization";
            default: return "Unknown";
        }
    }

    /**
     * @brief Материалы, используемые в лекциях.
     */
    enum class LectureMaterial {
        PRESENTATION_SLIDES, HANDOUTS, VIDEO_CLIPS, ANIMATIONS, MODELS,
        POSTERS, WORKBOOKS, QUIZ_CARDS, STAR_MAPS, GLOBE_MODEL,
        ASTRONOMICAL_PHOTOS
    };

    /**
     * @brief Тематическая категория мероприятий.
     */
    enum class ActivityTheme {
        HISTORY, SCIENCE, EDUCATION, ENTERTAINMENT, NONE
    };
};

#endif // PLANETARIUMPROJECT_ENUMS_H