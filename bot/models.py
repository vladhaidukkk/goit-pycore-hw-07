from collections import UserDict
from typing import Any


class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        # Name validation
        if not value:
            raise ValueError("Name cannot be empty")

        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        # Phone number validation
        if not value:
            raise ValueError("Phone number cannot be empty")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        phone_idx = self._find_phone_index(phone)
        if phone_idx is not None:
            raise ValueError(f"Phone number '{phone}' already exists")

        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone_idx = self._find_phone_index(phone)
        if phone_idx is None:
            raise ValueError(f"Phone number '{phone}' does not exist")

        del self.phones[phone_idx]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_idx = self._find_phone_index(old_phone)
        if phone_idx is None:
            raise ValueError(f"Phone number '{old_phone}' does not exist")

        self.phones[phone_idx] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p

    def _find_phone_index(self, phone: str) -> int | None:
        for i, p in enumerate(self.phones):
            if p.value == phone:
                return i

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        del self.data[name]
