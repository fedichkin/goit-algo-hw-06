from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise ValueError

    def validate(self, value):
        return re.match(r'^\d{10}$', value) is not None


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f'Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        index_phone = next((index for (index, item) in enumerate(self.phones) if item.value == phone), None)

        if index_phone is not None:
            del self.phones[index_phone]

    def edit_phone(self, old_phone, new_phone):
        index_phone = next((index for (index, item) in enumerate(self.phones) if item.value == old_phone), None)

        if index_phone is not None:
            self.phones[index_phone] = Phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        return next((item for item in self.phones if item.value == phone), None)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name] if name in self.data else None

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)


def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    john.remove_phone("5555555555")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)


if __name__ == '__main__':
    main()
