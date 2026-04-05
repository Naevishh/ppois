"""
Юнит-тесты для всех классов модуля services.
Запуск: python -m unittest tests.test_services -v
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Добавляем корень проекта в path для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

from SmartCityModel.services.base import PublicService
from SmartCityModel.services.hospital import Hospital
from SmartCityModel.services.education import EducationService
from SmartCityModel.services.utilities import UtilitiesService, SmartHomeRegistry
from SmartCityModel.core import Domain, HospitalException, ValidationError
from SmartCityModel.citizens import Human
from SmartCityModel.energy import SmartHome


# =============================================================================
# ТЕСТЫ ДЛЯ БАЗОВОГО КЛАССА PublicService
# =============================================================================

class ConcreteService(PublicService):
    """Конкретная реализация для тестирования абстрактного класса."""

    def provide_service(self, action_type):
        return f"Service provided: {action_type}"


class TestPublicService(unittest.TestCase):

    def setUp(self):
        self.service = ConcreteService(
            name="Test Service",
            address=("Lenina", 10),
            service_id="TS001",
            service_category=Domain.HOUSING
        )

    def test_init_attributes(self):
        """Проверка инициализации атрибутов."""
        self.assertEqual(self.service.name, "Test Service")
        self.assertEqual(self.service.address, ("Lenina", 10))
        self.assertEqual(self.service.service_id, "TS001")
        self.assertEqual(self.service.service_category, Domain.HOUSING)
        self.assertTrue(self.service.is_active)
        self.assertEqual(self.service.current_load, 0)
        self.assertEqual(self.service.available_actions, [])

    def test_get_status(self):
        """Проверка метода get_status."""
        status = self.service.get_status()
        self.assertEqual(status, {"active": True, "current_load": 0})

        self.service.is_active = False
        self.service.current_load = 42
        status = self.service.get_status()
        self.assertEqual(status, {"active": False, "current_load": 42})

    def test_provide_service_abstract(self):
        """Проверка, что абстрактный метод должен быть переопределён."""
        with self.assertRaises(TypeError):
            PublicService("Test", ("St", 1), "ID", Domain.HOUSING)


# =============================================================================
# ТЕСТЫ ДЛЯ КЛАССА Hospital
# =============================================================================

class TestHospital(unittest.TestCase):

    def setUp(self):
        self.hospital = Hospital(
            name="Городская больница №1",
            address=("Pushkina", 25, 3),
            service_id="HOSP001"
        )
        self.patient = Mock(spec=Human)
        self.patient.surname = "Иванов"
        self.patient.name = "Иван"
        self.patient.address = ("Lenina", 10, 5)

    def test_init_doctors(self):
        """Проверка инициализации списка врачей."""
        expected_doctors = {'psychiatrist', 'therapist', 'surgeon'}
        self.assertEqual(set(self.hospital.doctors.keys()), expected_doctors)
        self.assertEqual(self.hospital.doctors['therapist']['limit'], 50)

    def test_order_ticket_success(self):
        """Успешная запись к врачу."""
        result = self.hospital.order_ticket_to_doctor('therapist', self.patient)
        self.assertIn("Талон к врачу Терапевт №1", result)
        self.assertIn("Иванов И.", result)
        self.assertEqual(self.hospital.doctors['therapist']['current'], 1)

    def test_order_ticket_invalid_doctor(self):
        """Запись к несуществующему врачу."""
        with self.assertRaises(ValueError) as context:
            self.hospital.order_ticket_to_doctor('dentist', self.patient)
        self.assertIn("Некорректное имя врача", str(context.exception))

    def test_order_ticket_limit_reached(self):
        """Запись при исчерпании лимита талонов."""
        self.hospital.doctors['surgeon']['current'] = 10
        self.hospital.doctors['surgeon']['limit'] = 10
        with self.assertRaises(HospitalException) as context:
            self.hospital.order_ticket_to_doctor('surgeon', self.patient)
        self.assertIn("Все талоны", str(context.exception))

    def test_order_certificate_success(self):
        """Успешный заказ справки."""
        result = self.hospital.order_certificate("Для работы", self.patient)
        self.assertIn("Справка: Для работы", result)
        self.assertIn("Городская больница №1", result)
        self.assertIn("Иванов Иван", result)

    def test_order_certificate_invalid_purpose(self):
        """Заказ справки с некорректной целью."""
        with patch.object(self.hospital, 'purpose_validator') as mock_validator:
            mock_validator.validate.return_value = False
            with self.assertRaises((ValueError, ValidationError)):
                self.hospital.order_certificate("", self.patient)

    def test_call_ambulance(self):
        """Вызов скорой помощи."""
        address = ("Gagarina", 42, 15)
        result = self.hospital.call_ambulance(address)
        self.assertIn("Скорая выехала", result)
        self.assertIn("Улица Gagarina, дом 42", result)

    def test_get_available_doctors(self):
        """Получение списка доступных врачей."""
        for _ in range(5):
            self.hospital.doctors['therapist']['current'] += 1
        result = self.hospital.get_available_doctors()
        self.assertIn('therapist', result)
        self.assertEqual(result['therapist']['available'], 45)

    def test_provide_service_get_ticket(self):
        """Интеграционный тест provide_service для записи к врачу."""
        result = self.hospital.provide_service(
            patient=self.patient, action="get_ticket", doctor_name="psychiatrist"
        )
        self.assertIn("Окулист", result)

    def test_provide_service_missing_params(self):
        """Проверка обязательных параметров в provide_service."""
        with self.assertRaises(ValueError):
            self.hospital.provide_service(self.patient, action="get_ticket")
        with self.assertRaises(ValueError):
            self.hospital.provide_service(self.patient, action="order_certificate")

    def test_provide_service_invalid_action(self):
        """Неизвестное действие в provide_service."""
        with self.assertRaises(ValueError) as context:
            self.hospital.provide_service(self.patient, action="unknown")
        self.assertIn("Неизвестное действие", str(context.exception))


# =============================================================================
# ТЕСТЫ ДЛЯ КЛАССА EducationService
# =============================================================================

class TestEducationService(unittest.TestCase):

    def setUp(self):
        self.edu_service = EducationService(
            name="IT-Академия", address=("Университетская", 1), service_id="EDU001"
        )
        self.student = Mock(spec=Human)
        self.student.surname = "Петров"
        self.student.name = "Алексей"
        self.student.person_id = "STU123"

    def test_init_courses(self):
        """Проверка инициализации курсов."""
        expected = {"Python": 50, "DataScience": 30}
        self.assertEqual(self.edu_service.courses, expected)

    def test_enroll_course_success(self):
        """Успешная запись на курс."""
        with patch.object(self.edu_service, 'course_validator') as mock_validator:
            mock_validator.validate.return_value = True
            result = self.edu_service.enroll_course("Python", self.student)
            self.assertIn("Вы записаны на курс 'Python'.", result)

    def test_enroll_course_invalid_name(self):
        """Запись на курс с некорректным названием."""
        with patch.object(self.edu_service, 'course_validator') as mock_validator:
            mock_validator.validate.return_value = False
            with self.assertRaises(ValueError):
                self.edu_service.enroll_course("123!", self.student)

    def test_set_grade_success(self):
        """Успешная установка оценки."""
        with patch.object(self.edu_service, 'subject_validator') as mock_sub:
            with patch.object(self.edu_service, 'grade_validator') as mock_gr:
                mock_sub.validate.return_value = True
                mock_gr.validate_int.return_value = True
                result = self.edu_service.set_grade(self.student, "Математика", 9)
                self.assertIn("Оценка 9 по предмету 'Математика' установлена.", result)
                grades = self.edu_service.get_grades(self.student)["grades"]
                self.assertEqual(grades.get("Математика"), 9)

    def test_set_grade_invalid_grade(self):
        """Установка некорректной оценки."""
        with patch.object(self.edu_service, 'grade_validator') as mock_gr:
            mock_gr.validate_int.return_value = False
            with self.assertRaises(ValueError):
                self.edu_service.set_grade(self.student, "Математика", 15)

    def test_get_grades_empty(self):
        """Получение оценок для студента без оценок."""
        result = self.edu_service.get_grades(self.student)
        self.assertEqual(result,
                         {"student_id": "STU123", "student_name": f"{self.student.surname} {self.student.name[0][0]}.",
                          "grades": {}})

    def test_get_available_courses(self):
        """Получение списка доступных курсов."""
        result = self.edu_service.get_available_courses()
        self.assertEqual(result, {"Python": 50, "DataScience": 30})

    def test_format_grades_output(self):
        """Форматирование вывода оценок."""
        grades_data = {"student_id": "STU123", "student_name": f"{self.student.surname} {self.student.name[0][0]}.",
                       "grades": {"Python": 10, "История": 8}}
        result = self.edu_service.format_grades_output(grades_data)
        self.assertIn("Личный кабинет", result)
        self.assertIn("Python: 10", result)

    def test_provide_service_enroll(self):
        """Интеграционный тест provide_service для записи на курс."""
        with patch.object(self.edu_service, 'course_validator') as mock_val:
            mock_val.validate.return_value = True
            result = self.edu_service.provide_service(
                student=self.student, action="enroll_course", course_name="Python"
            )
            self.assertIn("Python", result)

    def test_provide_service_invalid_action(self):
        """Неизвестное действие в provide_service."""
        with self.assertRaises(ValueError):
            self.edu_service.provide_service(self.student, action="delete_course")


# =============================================================================
# ТЕСТЫ ДЛЯ КЛАССА SmartHomeRegistry
# =============================================================================

class TestSmartHomeRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = SmartHomeRegistry()
        self.mock_home = Mock(spec=SmartHome)
        self.mock_home.address = ("Test", 1, 1)

    def test_register_and_get_home(self):
        """Регистрация и получение дома."""
        self.registry.register_home(self.mock_home)
        result = self.registry.get_home(("Test", 1, 1))
        self.assertEqual(result, self.mock_home)

    def test_get_nonexistent_home(self):
        """Получение незарегистрированного дома."""
        result = self.registry.get_home(("Unknown", 999))
        self.assertIsNone(result)


# =============================================================================
# ТЕСТЫ ДЛЯ КЛАССА UtilitiesService
# =============================================================================

class TestUtilitiesService(unittest.TestCase):

    def setUp(self):
        self.util_service = UtilitiesService(
            name="ГорСвет", address=("Service", 1), service_id="UTIL001"
        )
        self.user = Mock(spec=Human)
        self.user.address = ("Lenina", 10, 5)
        self.mock_home = Mock(spec=SmartHome)
        self.mock_home.address = ("Lenina", 10, 5)
        self.mock_home.get_metrics.return_value = {"water": 120, "electricity": 350}

    def test_auto_collect_metrics_success(self):
        """Успешный сбор метрик."""
        self.util_service.registry.register_home(self.mock_home)
        result = self.util_service.auto_collect_metrics(("Lenina", 10, 5))
        self.assertEqual(result["water"], 120)
        self.assertEqual(result["electricity"], 350)
        self.assertIn(("Lenina", 10, 5), self.util_service.sensor_data)

    def test_auto_collect_metrics_home_not_found(self):
        """Сбор метрик для незарегистрированного дома."""
        with self.assertRaises(ValueError) as context:
            self.util_service.auto_collect_metrics(("Unknown", 999))
        self.assertIn("не найден в реестре", str(context.exception))

    def test_view_metrics_success(self):
        """Просмотр показаний счётчиков."""
        self.util_service.registry.register_home(self.mock_home)
        result = self.util_service.view_metrics(("Lenina", 10, 5))
        self.assertEqual(result["address"], ("Lenina", 10, 5))
        self.assertEqual(result["water"], 120)

    def test_report_issue_success(self):
        """Успешная подача заявки."""
        with patch.object(self.util_service, 'issue_validator') as mock_validator:
            mock_validator.validate.return_value = True
            result = self.util_service.report_issue("Не работает лифт в подъезде")
            self.assertIn("issue_id", result)
            self.assertEqual(result["status"], "Передано в диспетчерскую")

    def test_report_issue_invalid_description(self):
        """Заявка с некорректным описанием."""
        with patch.object(self.util_service, 'issue_validator') as mock_validator:
            mock_validator.validate.return_value = False
            with self.assertRaises(ValueError):
                self.util_service.report_issue("Коротко")

    def test_register_home(self):
        """Регистрация умного дома."""
        result = self.util_service.register_home(self.mock_home)
        self.assertIn("зарегистрирован", result)
        retrieved = self.util_service.registry.get_home(self.mock_home.address)
        self.assertEqual(retrieved, self.mock_home)

    def test_format_metrics_output_full_address(self):
        """Форматирование метрик с полным адресом."""
        metrics = {"address": ("Lenina", 10, 5), "water": 100, "electricity": 250}
        result = self.util_service.format_metrics_output(metrics)
        self.assertIn("Улица Lenina, дом 10, квартира 5", result)
        self.assertIn("100 м³", result)

    def test_format_metrics_output_short_address(self):
        """Форматирование метрик с коротким адресом."""
        metrics = {"address": ("Lenina", 10), "water": 50, "electricity": 150}
        result = self.util_service.format_metrics_output(metrics)
        self.assertIn("Улица Lenina, дом 10", result)
        self.assertNotIn("квартира", result)

    def test_provide_service_view_metrics(self):
        """Интеграционный тест provide_service для просмотра метрик."""
        self.util_service.registry.register_home(self.mock_home)
        result = self.util_service.provide_service(person=self.user, action="view_metrics")
        self.assertIn("Вода:", result)
        self.assertIn("Электричество:", result)

    def test_provide_service_report_issue(self):
        """Интеграционный тест provide_service для подачи заявки."""
        with patch.object(self.util_service, 'issue_validator') as mock_val:
            mock_val.validate.return_value = True
            result = self.util_service.provide_service(
                person=self.user, action="report_issue", description="Проблема с отоплением"
            )
            self.assertIn("Заявка №", result)

    def test_provide_service_missing_description(self):
        """Отсутствие описания при подаче заявки."""
        with self.assertRaises(ValueError):
            self.util_service.provide_service(person=self.user, action="report_issue")


# =============================================================================
# ЗАПУСК ТЕСТОВ
# =============================================================================

if __name__ == "__main__":
    # Запустить все тесты
    unittest.main(verbosity=2)

    # Или запустить только конкретный класс:
    # loader = unittest.TestLoader()
    # suite = loader.loadTestsFromTestCase(TestHospital)
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
