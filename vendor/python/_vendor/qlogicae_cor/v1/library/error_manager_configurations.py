from qlogicae_cor.v1.library.abstract_manager_configurations import (
    AbstractManagerConfigurations,
)


class ErrorManagerConfigurations(
    AbstractManagerConfigurations,
):
    __slots__ = (
        "_is_output_enabled",
        "_is_output_override_enabled",
        "_is_asynchronous_output_enabled",
        "_is_asynchronous_output_override_enabled",
        "_is_console_output_enabled",
        "_is_runtime_throw_output_enabled",
        "_title",
        "_message",
        "_title_message_separator",
    )

    def __init__(self) -> None:
        super().__init__()

        self._is_output_enabled: bool = True
        self._is_output_override_enabled: bool = False
        self._is_asynchronous_output_enabled: bool = True
        self._is_asynchronous_output_override_enabled: bool = False
        self._is_console_output_enabled: bool = True
        self._is_runtime_throw_output_enabled: bool = False
        self._title: str = "error at 'qlogicae-cor1'"
        self._message: str = "something went wrong here"
        self._title_message_separator: str = " - "

    @property
    def is_output_enabled(self) -> bool:
        return self._is_output_enabled

    @is_output_enabled.setter
    def is_output_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_output_enabled = value

    @property
    def is_output_override_enabled(self) -> bool:
        return self._is_output_override_enabled

    @is_output_override_enabled.setter
    def is_output_override_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_output_override_enabled = value

    @property
    def is_asynchronous_output_enabled(self) -> bool:
        return self._is_asynchronous_output_enabled

    @is_asynchronous_output_enabled.setter
    def is_asynchronous_output_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_asynchronous_output_enabled = value

    @property
    def is_asynchronous_output_override_enabled(self) -> bool:
        return self._is_asynchronous_output_override_enabled

    @is_asynchronous_output_override_enabled.setter
    def is_asynchronous_output_override_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_asynchronous_output_override_enabled = value

    @property
    def is_console_output_enabled(self) -> bool:
        return self._is_console_output_enabled

    @is_console_output_enabled.setter
    def is_console_output_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_console_output_enabled = value

    @property
    def is_runtime_throw_output_enabled(self) -> bool:
        return self._is_runtime_throw_output_enabled

    @is_runtime_throw_output_enabled.setter
    def is_runtime_throw_output_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_runtime_throw_output_enabled = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(
        self,
        value: str,
    ) -> None:
        self._title = value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(
        self,
        value: str,
    ) -> None:
        self._message = value

    @property
    def title_message_separator(self) -> str:
        return self._title_message_separator

    @title_message_separator.setter
    def title_message_separator(
        self,
        value: str,
    ) -> None:
        self._title_message_separator = value

    def is_enabled_for_runtime_throw_output(
        self,
    ) -> bool:
        return (
            self.is_output_enabled
            if self.is_output_override_enabled
            else self.is_runtime_throw_output_enabled
        )

    def is_enabled_for_console_output(
        self,
    ) -> bool:
        return (
            self.is_output_enabled
            if self.is_output_override_enabled
            else self.is_console_output_enabled
        )
