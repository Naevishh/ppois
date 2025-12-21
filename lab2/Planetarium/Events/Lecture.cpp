#include "Lecture.h"
#include "../Facade/Auditorium.h"

Lecture::Lecture(const std::string& name, double duration_, Enums::ActivityTheme theme_, Auditorium* auditorium_,
                 Enums::Theme lectureTheme_) :
        Activity(name, duration_, theme_, auditorium_),
        auditorium(auditorium_), lectureTheme(lectureTheme_) {
    setRules("Quiet environment");
}

bool Lecture::isValidForChildren() const {
    return difficultyLevel < 5;
}

bool Lecture::isProjectorNeeded() {
    for (const auto& material : materials) {
        if (material == Enums::LectureMaterial::PRESENTATION_SLIDES ||
            material == Enums::LectureMaterial::VIDEO_CLIPS) {
            return true;
        }
    }
    return false;
}

std::string Lecture::getLectureTheme() const {
    return Enums::themeToString(lectureTheme);
}

std::string Lecture::hold(const Date& date) {
    return auditorium->holdLecture(date, this) + " is being held on " + date.getDate() + ".";
}

void Lecture::setDifficultyLevel(int level) {difficultyLevel=level;}

void Lecture::addMaterial(Enums::LectureMaterial material) {
    materials.push_back(material);
}