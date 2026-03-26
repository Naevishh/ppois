from abc import ABC, abstractmethod

from ..citizens import Human
from ..core import Domain


class PublicService(ABC):
    def __init__(self, name: str, address: tuple, service_id: str, service_category: Domain) -> None:
        self.name = name
        self.address = address
        self.service_category = service_category
        self.service_id = service_id
        self.is_active = True
        self.current_load = 0
        self.available_actions = []

    @abstractmethod
    def provide_service(self, action_type, person: Human) -> None:
        pass

    def get_status(self) -> dict:
        return {
            "active": self.is_active,
            "current_load": self.current_load
        }