#include "Weather.h"

Weather::Weather() : weather(getRandomWeather()) {}
Weather::Weather(const wCondition& condition) {
    weather=condition;
}

wCondition Weather::getWeatherByIndex(size_t index) {
    const std::vector<wCondition> weathers = {
            wCondition::SUNNY,
            wCondition::CLOUDY,
            wCondition::PARTLY_CLOUDY,
            wCondition::RAINY,
            wCondition::STORMY,
            wCondition::SNOWY,
            wCondition::FOGGY,
            wCondition::WINDY,
            wCondition::HAZY
    };

    if (index >= weathers.size()) {
        return wCondition::SUNNY;
    }
    return weathers[index];
}

wCondition Weather::getRandomWeather() {
    int random_index = rand() % 9;
    return getWeatherByIndex(random_index);
}

wCondition Weather::getWeatherCondition() const {
    return weather;
}
