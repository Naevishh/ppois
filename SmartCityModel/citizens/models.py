class Human:
    def __init__(self, name: str, surname: str, age: int, address: tuple, person_id: str) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self._address = address
        self.person_id = person_id

    @property
    def address(self) -> tuple[str, ...]:
        return self._address

    @address.setter
    def address(self, value: tuple[str, ...]) -> None:
        self._address = value