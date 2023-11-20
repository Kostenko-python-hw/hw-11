from collections import UserDict
from utils import sanitize_phone_number, to_timestamp, timestamp_to_date, get_current_date


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.validate_and_transform(value)

    def validate_and_transform(self, _):
        pass

    def __str__(self):
        return str(self.value)


class Name(Field):
    def validate_and_transform(self, value):
         if value.isalpha():
            return value
         else:
            raise ValueError("The name must contain only letters.")
             


class Birthday(Field):
    def validate_and_transform(self, birthday):
        if birthday:
            timestamp = to_timestamp(birthday)
            if timestamp:
                return timestamp
            else:
                raise ValueError('Please enter the correct date.')
        else:
            return ''


class Phone(Field):
    def validate_and_transform(self, phone):
        int(sanitize_phone_number(phone))
        sunitized_phone = sanitize_phone_number(phone)
        if len(sunitized_phone) != 10:
            raise ValueError('The phone number must be 10 characters long.')
        else:
            return sunitized_phone


class Record:
    def __init__(self, name, birthday = ''):
        self.__name = ''
        self.__birthday = ''
        self.__phones = []
        self.name = name
        self.birthday = birthday

    @property
    def name(self):
        return self.__name
    
    @property
    def birthday(self):
        return self.__birthday
    
    @property
    def phones(self):
        return self.__phones

    @name.setter
    def name(self, value):
        self.__name = Name(value)

    @birthday.setter
    def birthday(self, value):
        self.__birthday = Birthday(value)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, date): # This is not a mandatory function, but a duplicate birthday setter
        self.birthday = date

    def days_to_birthday(self):
        if self.birthday:
            birthday_date = timestamp_to_date((self.birthday.value))
            current_date = get_current_date()
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
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}{f', birthday: {timestamp_to_date(self.birthday.value)}' if timestamp_to_date(self.birthday.value) else ''}"


class AddressBook(UserDict):

    def __init__(self):
        self.__current_index = None
        self.__quantity_per_iter = None
        self.current_index = 0
        self.quantity_per_iter = 3
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
            data = list_data[self.current_index: self.current_index + self.quantity_per_iter]
            self.current_index += self.quantity_per_iter
            return '\n'.join([str(record) for record in data])
        raise StopIteration

    def __iter__(self):
        return self
