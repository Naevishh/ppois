import json
import os
from pathlib import Path
from typing import Optional, Any
from .models import Human


class UserRepository:
    def __init__(self, file_name: str = "users_db.json") -> None:
        # 1. Находим папку, где лежит ЭТОТ файл (user_repo.py)
        current_module_dir = Path(__file__).resolve().parent

        # 2. Поднимаемся на уровень выше (из SmartCityModel в ppois)
        # Если репозиторий лежит в SmartCityModel, а data в корне ppois
        project_root = current_module_dir.parent

        # 3. Проверяем, есть ли папка data в корне проекта, иначе ищем рядом с модулем
        data_dir = project_root / "data"
        if not data_dir.exists():
            data_dir = current_module_dir / "data"

        self.file_path = data_dir / file_name
        self._cache: dict[str, dict[str, Any]] = {}
        self._load_from_file()

    def _load_from_file(self) -> None:
        # Теперь используем self.file_path

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                users_list = json.load(f)
                self._cache = {u['person_id']: u for u in users_list}
        except FileNotFoundError:
            self._cache = {}
        except json.JSONDecodeError:
            self._cache = {}

    def save_to_file(self) -> None:
        # Важно: создаем папку, если её нет, перед записью
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self._cache.values()), f, ensure_ascii=False, indent=4)

    def get_user(self, person_id: str) -> Optional[Human]:
        """Получение объекта Human по ID"""
        data = self._cache.get(person_id)
        if data:
            if isinstance(data.get('address'), list):
                data['address'] = tuple(data['address'])
            return Human(**data)
        return None

    def add_user(self, human: Human) -> None:
        """Регистрация нового пользователя"""
        self._cache[human.person_id] = {
            'name': human.name,
            'surname': human.surname,
            'age': human.age,
            'address': human.address,  # Убедитесь, что tuple сохраняется корректно
            'person_id': human.person_id
        }
        self.save_to_file()

    def get_all_users(self):
        return self._cache

    def authenticate(self, person_id: str) -> bool:
        """Проверка существования пользователя"""
        return person_id in self._cache
