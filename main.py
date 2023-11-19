from collections import UserDict
from datetime import datetime
from utils import sanitize_phone_number, to_timestamp


class Field:
    def __init__(self, value):
        self.__value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        transformed_date = self.validate_and_transform(value)
        self.value = transformed_date
    
    def validate_and_transform(self, birthday):
        timestamp = to_timestamp(birthday)
        if timestamp:
            return timestamp
        else:
            raise ValueError('Please enter the correct date.')


class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)
    
    def validate(self, phone):
        int(sanitize_phone_number(phone))
        sunitized_phone = sanitize_phone_number(phone)
        if len(sunitized_phone) != 10:
            raise ValueError('The phone number must be 10 characters long.')


class Record:
    def __init__(self, name):
        self.__name = Name(name)
        self.__birthday = None
        self.__phones = []

    @property
    def name(self):
        return self.__name
    
    @property
    def birthday(self):
        return self.__birthday.value
    
    @property
    def phones(self):
        return self.__phones

    @name.setter
    def name(self, value):
        self.__name = value

    @birthday.setter
    def birthday(self, value):
        self.__birthday = value

    @phones.setter
    def phones(self, value):
        self.__phones.append(Phone(value))

    def add_phone(self, phone):
        # self.phones.append(Phone(phone))
        self.phones = phone

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def days_to_birthday(self):
        print(type(self.birthday))
        print(type(self.__birthday.value))
        if self.birthday:
            birthday_date = datetime.fromtimestamp((self.birthday)).date()
            current_date = datetime.today().date()
            current_year = current_date.year
            next_birthday = birthday_date.replace(year=current_year)
            if next_birthday < current_date:
                next_birthday = birthday_date.replace(year=current_year + 1)
            return (next_birthday - current_date).days
        else:
            return None

    def remove_phone(self, phone):
        filtred_array = list(filter(lambda el: el.value != phone, self.phones))
        if len(filtred_array) != len(self.phones):
            self.phones = filtred_array
        else:
            raise ValueError()

    def edit_phone(self, old_phone, new_phone):
        _index = None
        for index, el in enumerate(self.phones):
            if el.value == old_phone:
                _index = index
                break
        if _index is None:
            raise ValueError('The phone you want to change was not found')
        else:
            _new_Phone = Phone(new_phone)
            self.phones[_index] = _new_Phone

    def find_phone(self, phone):
        for el in self.phones:
            if phone == el.value:
                return el
            
    

    def __str__(self):
        print(self.__birthday)
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def __init__(self):
        self.__current_index = 0
        self.__quantity_per_iter = 3
        super().__init__(self)

    @property
    def quantity_per_iter(self):
        return self.__quantity_per_iter

    @quantity_per_iter.setter
    def quantity_per_iter(self, value):
        self.__quantity_per_iter = value

    @property
    def current_index(self):
        return self.__current_index

    @current_index.setter
    def current_index(self, value):
        self.__current_index = value
    
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError(f"Record with name '{record.name.value}' already exists.")
        
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __next__(self):
        if self.__current_index <= len(self.data) - 1:
            list_data = list(self.data.values())
            data = list_data[self.__current_index: self.__current_index + self.quantity_per_iter]
            self.__current_index += self.quantity_per_iter
            print('*'*30)
            return '; '.join([str(record) for record in data])
        raise StopIteration

    def __iter__(self):
        return self



 # Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("16.11.1987")
print('*'*20)
print(john_record.days_to_birthday())
print('*'*20)

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

jane_record = Record("J123ane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

jane_record = Record("Ja123ne")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

jane_record = Record("Janzzze")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

jane_record = Record("J123ssssane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

jane_record = Record("Ja123ddddddne")
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

book.quantity_per_iter = 4
_book = iter(book)
for i in _book:
    print(i)

    # Видалення запису Jane
# book.delete("Jane")