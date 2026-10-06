from typing import TypeVar

from qlogicae_cor.v1.library.abstract_manager_configurations import (
    AbstractManagerConfigurations,
)
from qlogicae_cor.v1.library.error_manager import ErrorManager
from qlogicae_cor.v1.library.singleton_manager import SingletonManager

Configurations = TypeVar(
    "Configurations",
    bound=AbstractManagerConfigurations,
)


class AbstractManager[Configurations: AbstractManagerConfigurations]:
    __slots__ = "_configurations"

    def __init__(
        self,
        new_configurations: Configurations,
    ) -> None:
        self._configurations: Configurations = new_configurations

    @property
    def configurations(self) -> Configurations:
        return self._configurations

    @configurations.setter
    def configurations(self, value: Configurations) -> None:
        self._configurations = value

    def setup(
        self,
        new_configurations: Configurations,
    ) -> bool:
        if self._configurations.is_disabled_for_handling(
            new_configurations is None,
        ):
            return False

        self._configurations = new_configurations

        return True

    def reset(
        self,
    ) -> bool:
        if self._configurations.is_disabled_for_handling():
            return False

        self._configurations = type(
            self._configurations,
        )()

        return True

    def handle_error_outputs(
        self,
        error: str | Exception,
        message: str | None = None,
    ) -> bool:
        error_manager = SingletonManager.get_singleton(
            ErrorManager,
        )

        if isinstance(error, Exception):
            return error_manager.handle_error_outputs(
                error,
            )

        if message is not None:
            return error_manager.handle_error_outputs(
                error,
                message,
            )

        return error_manager.handle_error_outputs(
            error,
        )
