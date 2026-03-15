class Human:
    def __init__(self, name: str, surname: str, age: int, address: tuple, person_id: str):
        self.name = name
        self.surname = surname
        self.age = age
        self.address = address
        self.person_id = person_id

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, tuple):
            raise TypeError(f"Адрес должен быть типа 'кортеж'.")
        self._address = value
