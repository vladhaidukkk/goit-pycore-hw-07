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


@commands.register("change", args=["name", "new phone number"])
def change_contact(args: CommandArgs, context: CommandContext) -> None:
    name, new_phone = args
    book = context["book"]

    record = book.find(name)
    if record:
        try:
            record.replace_phone(0, new_phone)
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
