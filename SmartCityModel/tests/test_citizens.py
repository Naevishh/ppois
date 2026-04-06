"""
Юнит-тесты для модуля SmartCityModel.citizens
Классы: Human, UserRepository
Запуск: pytest tests/test_citizens.py -v
"""

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from SmartCityModel.citizens import Human, UserRepository


class TestHuman:
    """Тесты для класса Human (модель пользователя)"""

    def test_human_initialization(self):
        """Проверка корректной инициализации объекта Human"""
        human = Human(
            name="Анна",
            surname="Петрова",
            age=28,
            address=("г. Москва", "ул. Ленина", "д. 10", "кв. 42"),
            person_id="user_001"
        )

        assert human.name == "Анна"
        assert human.surname == "Петрова"
        assert human.age == 28
        assert human.address == ("г. Москва", "ул. Ленина", "д. 10", "кв. 42")
        assert human.person_id == "user_001"

    def test_address_property_getter(self):
        """Проверка геттера свойства address"""
        address = ("г. СПб", "Невский проспект", "д. 25")
        human = Human("Иван", "Иванов", 35, address, "user_002")

        assert human.address == address
        assert isinstance(human.address, tuple)

    def test_address_property_setter(self):
        """Проверка сеттера свойства address"""
        human = Human("Мария", "Сидорова", 42, ("старый", "адрес"), "user_003")

        new_address = ("г. Казань", "ул. Баумана", "д. 5")
        human.address = new_address

        assert human.address == new_address
        assert human._address == new_address

    def test_address_immutability_check(self):
        """Проверка, что адрес возвращается как кортеж (неизменяемый)"""
        human = Human("Тест", "Тестов", 30, ("адрес1", "адрес2"), "user_004")

        addr = human.address

        human.address = ("новый", "адрес", "полностью")
        assert human.address == ("новый", "адрес", "полностью")

    def test_human_with_minimal_address(self):
        """Проверка работы с адресом минимальной длины"""
        human = Human("Коротко", "Строков", 25, ("г. Город",), "user_005")
        assert human.address == ("г. Город",)

    def test_human_with_empty_address_tuple(self):
        """Проверка работы с пустым кортежем адреса"""
        human = Human("Без", "Адреса", 20, (), "user_006")
        assert human.address == ()

    @pytest.mark.parametrize("age", [0, 1, 18, 65, 100, 120])
    def test_human_age_boundary_values(self, age):
        """Проверка инициализации с граничными значениями возраста"""
        human = Human("Возрастной", "Тестов", age, ("адрес",), "user_007")
        assert human.age == age

    def test_human_special_characters_in_name(self):
        """Проверка поддержки спецсимволов и юникода в имени/фамилии"""
        human = Human("Марія", "O'Браен-Смит", 33, ("адрес",), "user_008")
        assert human.name == "Марія"
        assert human.surname == "O'Браен-Смит"


class TestUserRepository:
    """Тесты для класса UserRepository (репозиторий пользователей)"""

    @pytest.fixture
    def sample_human(self):
        """Фикстура: тестовый объект Human"""
        return Human(
            name="Тест",
            surname="Пользователь",
            age=30,
            address=("г. Тестов", "ул. Тестовая", "д. 1"),
            person_id="test_user_123"
        )

    @pytest.fixture
    def mock_json_data(self):
        """Фикстура: тестовые данные в формате JSON"""
        return [
            {
                "name": "Анна",
                "surname": "Петрова",
                "age": 28,
                "address": ["г. Москва", "ул. Ленина", "д. 10"],
                "person_id": "user_001"
            },
            {
                "name": "Иван",
                "surname": "Иванов",
                "age": 35,
                "address": ["г. СПб", "Невский пр.", "д. 25"],
                "person_id": "user_002"
            }
        ]

    def test_init_default_filename(self, tmp_path):
        """Проверка инициализации с именем файла по умолчанию"""
        with patch.object(Path, 'exists', return_value=True):
            repo = UserRepository()

        assert "users_db.json" in str(repo.file_path)

    def test_init_custom_filename(self, tmp_path):
        """Проверка инициализации с кастомным именем файла"""
        with patch.object(Path, 'exists', return_value=True):
            repo = UserRepository("custom_db.json")
        assert "custom_db.json" in str(repo.file_path)

    def test_load_from_file_success(self, tmp_path, mock_json_data):
        """Проверка успешной загрузки данных из файла"""

        test_file = tmp_path / "users_db.json"
        test_file.write_text(json.dumps(mock_json_data, ensure_ascii=False), encoding="utf-8")

        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = test_file
                repo._cache = {}
                UserRepository._load_from_file(repo)

        assert "user_001" in repo._cache
        assert "user_002" in repo._cache
        assert repo._cache["user_001"]["name"] == "Анна"

    def test_load_from_file_not_found(self, tmp_path):
        """Проверка обработки отсутствия файла"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "nonexistent.json"
                repo._cache = {"old": "data"}
                UserRepository._load_from_file(repo)

        assert repo._cache == {}

    def test_load_from_file_invalid_json(self, tmp_path):
        """Проверка обработки невалидного JSON"""
        test_file = tmp_path / "broken.json"
        test_file.write_text("{ invalid json }", encoding="utf-8")

        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = test_file
                repo._cache = {"old": "data"}
                UserRepository._load_from_file(repo)

        assert repo._cache == {}

    def test_save_to_file_creates_directory(self, tmp_path):
        """Проверка, что save_to_file создаёт папку при необходимости"""
        nested_dir = tmp_path / "new" / "nested" / "dir"

        with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
            repo = UserRepository.__new__(UserRepository)
            repo.file_path = nested_dir / "users_db.json"
            repo._cache = {
                "user_1": {"name": "Test", "surname": "User", "age": 25,
                           "address": ["addr"], "person_id": "user_1"}
            }
            UserRepository.save_to_file(repo)

        assert (nested_dir / "users_db.json").exists()

    def test_save_to_file_writes_correct_data(self, tmp_path):
        """Проверка корректной записи данных в файл"""
        test_file = tmp_path / "users_db.json"

        with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
            repo = UserRepository.__new__(UserRepository)
            repo.file_path = test_file
            repo._cache = {
                "user_1": {
                    "name": "Анна",
                    "surname": "Петрова",
                    "age": 28,
                    "address": ("г. Москва", "ул. Ленина"),
                    "person_id": "user_1"
                }
            }
            UserRepository.save_to_file(repo)

        with open(test_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)

        assert len(saved_data) == 1
        assert saved_data[0]["name"] == "Анна"

        assert isinstance(saved_data[0]["address"], list)

    def test_get_user_exists(self, tmp_path, sample_human):
        """Проверка получения существующего пользователя"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {
                    sample_human.person_id: {
                        "name": sample_human.name,
                        "surname": sample_human.surname,
                        "age": sample_human.age,
                        "address": list(sample_human.address),
                        "person_id": sample_human.person_id
                    }
                }

        result = repo.get_user(sample_human.person_id)

        assert isinstance(result, Human)
        assert result.name == sample_human.name
        assert result.person_id == sample_human.person_id
        assert isinstance(result.address, tuple)

    def test_get_user_not_exists(self, tmp_path):
        """Проверка получения несуществующего пользователя"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {}

        result = repo.get_user("nonexistent_id")
        assert result is None

    def test_add_user(self, tmp_path, sample_human):
        """Проверка добавления нового пользователя"""
        test_file = tmp_path / "users_db.json"

        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = test_file
                repo._cache = {}

                repo.save_to_file = MagicMock()

        repo.add_user(sample_human)

        assert sample_human.person_id in repo._cache
        saved = repo._cache[sample_human.person_id]
        assert saved["name"] == sample_human.name
        assert saved["address"] == sample_human.address

        repo.save_to_file.assert_called_once()

    def test_get_all_users(self, tmp_path):
        """Проверка получения всех пользователей"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {
                    "id1": {"name": "User1", "person_id": "id1"},
                    "id2": {"name": "User2", "person_id": "id2"}
                }

        all_users = repo.get_all_users()

        assert isinstance(all_users, dict)
        assert len(all_users) == 2
        assert "id1" in all_users
        assert "id2" in all_users

    def test_authenticate_success(self, tmp_path):
        """Проверка успешной аутентификации"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {"valid_id": {"person_id": "valid_id"}}

        assert repo.authenticate("valid_id") is True

    def test_authenticate_failure(self, tmp_path):
        """Проверка неудачной аутентификации"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {"valid_id": {"person_id": "valid_id"}}

        assert repo.authenticate("invalid_id") is False

    def test_address_list_to_tuple_conversion(self, tmp_path):
        """Проверка конвертации списка адреса в кортеж при загрузке"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"

                repo._cache = {
                    "user_1": {
                        "name": "Test",
                        "surname": "User",
                        "age": 30,
                        "address": ["г. Тест", "ул. Тестовая"],
                        "person_id": "user_1"
                    }
                }

        user = repo.get_user("user_1")
        assert isinstance(user.address, tuple)
        assert user.address == ("г. Тест", "ул. Тестовая")

    def test_add_user_preserves_tuple_address(self, tmp_path, sample_human):
        """Проверка, что tuple-адрес корректно сохраняется в кэше"""
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(UserRepository, '__init__', lambda self, file_name="users_db.json": None):
                repo = UserRepository.__new__(UserRepository)
                repo.file_path = tmp_path / "test.json"
                repo._cache = {}
                repo.save_to_file = MagicMock()

        repo.add_user(sample_human)

        cached = repo._cache[sample_human.person_id]
        assert cached["address"] == sample_human.address
