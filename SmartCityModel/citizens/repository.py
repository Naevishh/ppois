import json
from typing import Optional

from .models import Human


class UserRepository:
    def __init__(self, file_name: str = "users_db.json") -> None:
        self.file_name = file_name
        self._cache: dict[str, dict] = {}  # Кеш: {id: данные}
        self._load_from_file()

    def _load_from_file(self) -> None:
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                users_list = json.load(f)
                self._cache = {u['person_id']: u for u in users_list}
        except FileNotFoundError:
            self._cache = {}  # Если файла нет, начинаем с пустого
        except json.JSONDecodeError:
            self._cache = {}

    def save_to_file(self) -> None:
        """Сохранение изменений обратно в файл"""
        with open(self.file_name, 'w', encoding='utf-8') as f:
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

    def authenticate(self, person_id: str) -> bool:
        """Проверка существования пользователя"""
        return person_id in self._cache
