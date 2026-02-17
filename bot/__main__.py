import sys

from bot.commands import (
    CommandArgs,
    CommandContext,
    CommandNotFoundError,
    CommandsRegistry,
    InvalidCommandArgumentsError,
)

commands = CommandsRegistry()


@commands.register("hello")
def say_hello() -> None:
    print("How can I help you?")


@commands.register("add", args=["name", "phone number"])
def add_contact(args: CommandArgs, context: CommandContext) -> None:
    name, phone = args
    contacts = context["contacts"]

    if name not in contacts:
        contacts[name] = phone
        print("Contact added.")
    else:
        print("Contact already exists.")


@commands.register("change", args=["name", "new phone number"])
def change_contact(args: CommandArgs, context: CommandContext) -> None:
    name, new_phone = args
    contacts = context["contacts"]

    if name in contacts:
        contacts[name] = new_phone
        print("Contact updated.")
    else:
        print("Contact doesn't exist.")


@commands.register("phone", args=["name"])
def show_phone(args: CommandArgs, context: CommandContext) -> None:
    name = args[0]
    contacts = context["contacts"]

    if name in contacts:
        phone = contacts[name]
        print(phone)
    else:
        print("Contact doesn't exist.")


@commands.register("all")
def show_all(context: CommandContext) -> None:
    contacts = context["contacts"]
    if contacts:
        print("\n".join(f"{name}: {phone}" for name, phone in contacts.items()))
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
    contacts: dict[str, str] = {}

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        try:
            commands.run(command, *args, contacts=contacts)
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
