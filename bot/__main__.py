import sys

from bot.commands import (
    CommandArgs,
    CommandContext,
    CommandNotFoundError,
    CommandsRegistry,
    InvalidCommandArgumentsError,
)
from bot.models import AddressBook, Record

commands = CommandsRegistry()


@commands.register("hello")
def say_hello() -> None:
    print("How can I help you?")


@commands.register("add", args=["name", "phone number"])
def add_contact(args: CommandArgs, context: CommandContext) -> None:
    name, phone = args
    book = context["book"]

    if name not in book:
        try:
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
        except ValueError as e:
            print(e)
        else:
            print("Contact added.")
    else:
        print("Contact already exists.")


@commands.register("change", args=["name", "old phone number", "new phone number"])
def change_contact(args: CommandArgs, context: CommandContext) -> None:
    name, old_phone, new_phone = args
    book = context["book"]

    record = book.find(name)
    if record:
        try:
            record.edit_phone(old_phone, new_phone)
        except ValueError as e:
            print(e)
        else:
            print("Contact updated.")
    else:
        print("Contact doesn't exist.")


@commands.register("phone", args=["name"])
def show_phone(args: CommandArgs, context: CommandContext) -> None:
    name = args[0]
    book = context["book"]

    record = book.find(name)
    if record:
        print(record.phones[0])
    else:
        print("Contact doesn't exist.")


@commands.register("all")
def show_all(context: CommandContext) -> None:
    book = context["book"]
    if book:
        print(
            "\n".join(f"{record.name}: {record.phones[0]}" for record in book.values())
        )
    else:
        print("No contacts.")


@commands.register("add-birthday", args=["name", "birthday"])
def add_birthday(args: CommandArgs, context: CommandContext) -> None:
    name, birthday = args
    book = context["book"]

    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            print(e)
        else:
            print("Birthday added.")
    else:
        print("Contact doesn't exist.")


@commands.register("show-birthday", args=["name"])
def show_birthday(args: CommandArgs, context: CommandContext) -> None:
    name = args[0]
    book = context["book"]

    record = book.find(name)
    if record:
        birthday = record.get_birthday()
        print(birthday or "Contact doesn't have a birthday set.")
    else:
        print("Contact doesn't exist.")


@commands.register("birthdays")
def birthdays(context: CommandContext) -> None:
    book = context["book"]

    if not book:
        print("No contacts.")
        return

    if book.birthdays_count == 0:
        print("No contacts with birthdays.")
        return

    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        print("No contacts with upcoming birthdays.")
        return

    print(
        "\n".join(
            f"{upcoming_birthday['name']}: {upcoming_birthday['birthday']} (Congratulate: {upcoming_birthday['congratulation_date']})"
            for upcoming_birthday in upcoming_birthdays
        )
    )


@commands.register("exit", "close", "quit", "bye")
def say_goodbye() -> None:
    print("Good bye!")
    sys.exit(0)


def parse_input(user_input: str) -> tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args


def main() -> None:
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        try:
            commands.run(command, *args, book=book)
        except CommandNotFoundError:
            print("Invalid command.")
        except InvalidCommandArgumentsError as e:
            expected_args_str = (
                ", ".join(e.expected_args[:-1]) + " and " + e.expected_args[-1]
                if len(e.expected_args) > 1
                else e.expected_args[0]
            )
            print(f"Give me {expected_args_str} please.")
        except Exception as e:
            print(f"Whoops, an unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
