from collections import UserDict
from datetime import date, datetime, timedelta
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


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

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

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict]:
        current_date = date.today()
        upcoming_birthdays: list[dict] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            current_year_birthday = date(
                year=current_date.year,
                month=record.birthday.month,
                day=record.birthday.day,
            )

            if current_year_birthday >= current_date:
                next_birthday = current_year_birthday
            else:
                next_birthday = date(
                    year=current_date.year + 1,
                    month=record.birthday.month,
                    day=record.birthday.day,
                )

            dates_diff = next_birthday - current_date
            if dates_diff.days > 7:
                continue

            congratulation_date = next_birthday
            if congratulation_date.isoweekday() == 6:  # Saturday -> Monday
                congratulation_date += timedelta(days=2)
            elif congratulation_date.isoweekday() == 7:  # Sunday -> Monday
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                {
                    "name": record.name,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                }
            )

        return upcoming_birthdays
