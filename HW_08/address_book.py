from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        if not self.validate(phone):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(phone)

    @staticmethod
    def validate(phone):
        return bool(re.match(r"^\d{10}$", phone))


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = self.validate(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

    @staticmethod
    def validate(date_str):
        return datetime.strptime(date_str, "%d.%m.%Y")


class PhoneNotFoundError(Exception):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            raise ValueError("Phone number already exists.")
        self.phones.append(phone)

    def remove_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                self.phones.remove(phone)
                return
        raise PhoneNotFoundError("Phone number not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_birthday_str(self):
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else None

    def __str__(self):
        phone_numbers = ", ".join(str(phone) for phone in self.phones)
        birthday_str = self.get_birthday_str() or "No birthday set"
        return f"Name: {self.name}, Phones: {phone_numbers}, Birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def find_all(self, name):
        return [record for record in self.data.values() if record.name.value == name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found.")

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    greeting_date = birthday_this_year + timedelta(
                        days=(
                            2
                            if birthday_this_year.weekday() == 5
                            else 1 if birthday_this_year.weekday() == 6 else 0
                        )
                    )

                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "greeting_date": greeting_date.strftime("%B %d"),
                        }
                    )
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


book = AddressBook()

"""Test sample:"""
record1 = Record("John Doe")
record1.add_phone("1234567890")
record1.add_birthday("18.03.1990")
book.add_record(record1)

record2 = Record("Jane Smith")
record2.add_phone("0987654321")
record2.add_birthday("22.03.1992")
book.add_record(record2)

upcoming_birthdays = book.get_upcoming_birthdays()

if upcoming_birthdays:
    greetings = ", ".join(
        [f"{name['name']} on {name['greeting_date']}" for name in upcoming_birthdays]
    )
    print(f"Current week greetings list: {greetings}")
else:
    print("No upcoming birthdays this week.")
