import inspect
from typing import Any, Callable, NamedTuple, get_type_hints


class CommandError(Exception):
    pass


class CommandAlreadyExistsError(CommandError):
    pass


class CommandNotFoundError(CommandError):
    pass


class ForbiddenCommandArgumentError(CommandError):
    pass


class InvalidCommandArgumentsError(CommandError):
    def __init__(self, message: str, *, expected_args: list[str]) -> None:
        self.expected_args = expected_args
        super().__init__(message)


CommandArgs = tuple[str, ...]
CommandContext = dict[str, Any]


class Command(NamedTuple):
    name: str
    func: Callable
    expected_args: list[str]


class CommandsRegistry:
    def __init__(self) -> None:
        self._commands_registry: dict[str, Command] = {}

    def register(self, *command_names: str, args: list[str] | None = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            for name in command_names:
                if name in self._commands_registry:
                    raise CommandAlreadyExistsError(
                        f"Command '{name}' is already registered."
                    )
                self._commands_registry[name] = Command(
                    name=name,
                    func=func,
                    expected_args=args or [],
                )
            return func

        return decorator

    def get(self, command_name: str) -> Command:
        command = self._commands_registry.get(command_name)
        if not command:
            raise CommandNotFoundError(f"Command '{command_name}' is not registered.")
        return command

    def run(self, command_name: str, *args: str, **kwargs: Any) -> None:
        command = self.get(command_name)
        command_args: dict[str, Any] = {}

        sig = inspect.signature(command.func)
        hints = get_type_hints(command.func)

        for param_name, _ in sig.parameters.items():
            param_type = hints.get(param_name)

            # Check args quantity & inject them
            if param_type == CommandArgs:
                if command.expected_args and len(command.expected_args) != len(args):
                    raise InvalidCommandArgumentsError(
                        f"Command '{command_name}' expects {len(command.expected_args)} args",
                        expected_args=command.expected_args,
                    )
                command_args[param_name] = args

            # Inject context
            if param_type == CommandContext:
                command_args[param_name] = kwargs

            # Forbid all other arguments
            if param_type != CommandArgs and param_type != CommandContext:
                raise ForbiddenCommandArgumentError(
                    f"Argument '{param_name}' with '{param_type}' type is not allowed."
                )

        command.func(**command_args)
