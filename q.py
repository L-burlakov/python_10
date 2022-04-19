from collections import UserDict


class Field:  # логіка роботи з полями
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


class Email(Field):
    pass


class Record:  # тут треба організувати запис та збереження за полями
    def __init__(self, name: Name, phones: Phone = []):
        self.name = name
        self.phones = phones

    def phone_change(self, numb: int, phone_new: Phone):
        self.phones.pop(numb - 1)
        self.phones.insert(numb - 1, phone_new)
        print(self.phones)
        print(self.phones[0])
        print(self.phones[1])

    def phone_del(self, numb=int):
        self.phones.pop(numb)

    def __str__(self):
        # a_str = str()
        # for p in self.phones:
        #     a_str = a_str + ' ' + str(p)
        # return str(a_str)
        return f"{','.join([f'{p.value}' for p in self.phones])}"


class AddressBook(UserDict):
    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec

    def delete_record(self, param: str):
        #   if key == param:
        del self.data[param]

    def search_record(self, param: str):  # от тут краще приймати str
        for key, value in self.items():
            if key == param:
                a = print(key, ":", value)

    def show_all(self):
        result = []
        for k, v in self.items():
            result.append(f"{k} : {','.join([p.value for p in v.phones])}")
        result_str = "\n".join(result)
        return result_str


phone_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError as e:
            return e
        except ValueError as e:
            return e
        except TypeError as e:
            return e

    return inner


@input_error
def save_new_rec(*args):
    name = Name(args[0])
    dig = []
    for arg in args:
        dig.append(arg)
    phones = []
    for p in dig[1:]:
        phones.append(Phone(p))
    phone = Phone(dig)
    rec = Record(name, phones)
    phone_book.add_record(rec)
    return f"Added name {args[0]} with phone {', '.join(dig)}"


@input_error
def show_number(*args):
    if not args[0]:
        raise ValueError(f"Not enough param for command 'Show all'")
    if args[0].lower() == "all":
        return phone_book.show_all()
    else:
        for k, v in phone_book.items():
            if k == args[0]:
                return f"{k} : {v}"


@input_error
def delete_rec(*args):
    phone_book.delete_record(args[0])
    return f"Record {args[0]} was deleted"


@input_error
def change_rec(*args):
    if args[0] in phone_book:
        phone_book.search_record(args[0])
        rd = int(input("Which phone number you want to change? "))
        cd = input("On what? (if U want to delete - just let it go (press Enter)) ")
        if cd == "":
            phone_book[args[0]].phone_del(rd)
        else:
            p = Phone(cd)
            phone_book[args[0]].phone_change(rd, p)
        return f"Contact {args[0]} change phone successfull."
    else:
        return f"Contact {args[0]} not in phonebook."


@input_error
def finish(*args):
    print("Good Bye")
    return "exit"


def start_the_bot(*args):
    return "How can I help U? "


operations = {
    "hello": start_the_bot,
    "add": save_new_rec,
    "change": change_rec,
    "delete": delete_rec,
    "phone": show_number,
    "show": show_number,
    "good": finish,
    "close": finish,
    "exit": finish,
    ".": finish,
}


def parser_func(string_ask: str):
    command = None
    data = None
    for key, func in operations.items():
        if string_ask.lower().startswith(key.lower()):
            command = func
        if command:
            data = string_ask[len(key) :].strip().split(" ")
            return command, data


while True:
    user_input = input("Type command: ")
    try:
        command, data = parser_func(user_input)
    except TypeError:
        print("wrong command")
        continue
    if command == None or data == None:
        continue
    result = command(*data)
    if result == "exit":
        break
    else:
        print(result)