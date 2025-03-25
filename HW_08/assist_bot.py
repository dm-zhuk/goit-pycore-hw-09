from address_book import Phone, Record, AddressBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input. Please provide the correct contact data."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner


def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me a name and phone please.")

    phone_input = args[-1]
    name = " ".join(args[:-1])

    if not Phone.validate(phone_input):
        raise ValueError("Phone number must be 10 digits and numeric.")

    phone = Phone(phone_input)

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Please provide the name, old phone, and new phone.")

    name = " ".join(args[:-2])
    old_phone = args[-2]
    new_phone = args[-1]

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")

    if old_phone not in [phone.value for phone in record.phones]:
        raise ValueError("Old phone number does not match.")

    record.remove_phone(old_phone)
    record.add_phone(Phone(new_phone))

    return "Phone number updated."


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Please provide the name of the contact to delete.")

    name = " ".join(args)
    try:
        book.delete(name)
        return f"Contact '{name}' has been deleted."
    except KeyError as e:
        return str(e)

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Give me the name please.")

    name = " ".join(args)
    record = book.find(name)

    if record:
        return (
            ", ".join(str(phone) for phone in record.phones)
            if record.phones
            else "No phone numbers found."
        )

    return "Sorry, contact not found."


@input_error
def show_all(book: AddressBook):
    if not book:
        return "Sorry, no book found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me a name and birthday.")

    birthday = args[-1]
    name = " ".join(args[:-1])

    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError("Contact not found.")


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Give me the name please.")

    name = " ".join(args)
    records = book.find_all(name)

    if records:
        birthday_info = []
        for record in records:
            birthday_str = record.get_birthday_str()
            if birthday_str:
                birthday_info.append(f"{record.name} on {birthday_str}")
            else:
                birthday_info.append(f"{record.name} has no birthday set.")

        return "\n".join(birthday_info)

    return "Sorry, contact not found."


@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(
            f"{entry['name']} on {entry['greeting_date']}"
            for entry in upcoming_birthdays
        )
    return "No upcoming birthdays this week."
