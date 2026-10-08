from __future__ import annotations

__all__ = (
    "ConsoleLogManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .log_options import LogOptions

_logging: Any = None
_LogFormat: Any = None
_LogOptions: Any = None
_LogOptionsManager: Any = None
_SingletonManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _LogFormat
    global _LogOptions
    global _LogOptionsManager
    global _SingletonManager

    import logging

    from .log_format import LogFormat
    from .log_options import LogOptions
    from .log_options_manager import LogOptionsManager
    from .singleton_manager import SingletonManager

    _logging = logging
    _LogFormat = LogFormat
    _LogOptions = LogOptions
    _LogOptionsManager = (
        LogOptionsManager
    )
    _SingletonManager = (
        SingletonManager
    )

    _handle_dynamic_imports = lambda: None


class ConsoleLogManager:
    __slots__ = (
        "_logger",
        "_options",
        "_log_options_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._log_options_manager = _SingletonManager.get_singleton(
            _LogOptionsManager
        )

        self._logger = _logging.getLogger(
            "console-logger",
        )

        self._logger.setLevel(
            _logging.DEBUG,
        )

        self._logger.propagate = False

        self._logger.handlers.clear()

        handler = _logging.StreamHandler()

        handler.setFormatter(
            _LogFormat(),
        )

        self._logger.addHandler(
            handler,
        )

        self._options: LogOptions = _LogOptions()

    @property
    def options(self) -> LogOptions:
        return self._options

    @options.setter
    def options(
        self,
        value: LogOptions,
    ) -> None:
        self._options = value

    def log(
        self,
        message: str,
        options: LogOptions,
    ) -> str:
        if not options.is_enabled:
            return ""

        message = str(message).strip()

        if options.is_verbose_enabled:
            self._logger.log(
                options.log_level,
                message,
                stacklevel=options.stack_level,
            )
        else:
            print(message)

        return message

    def log_debug(
        self,
        message: str,
    ) -> str:
        return self.log(
            message,
            self._log_options_manager.generate_modified_defaults(
                self._options,
                log_level=_logging.DEBUG,
            ),
        )

    def log_info(
        self,
        message: str,
    ) -> str:
        return self.log(
            message,
            self._log_options_manager.generate_modified_defaults(
                self._options,
                log_level=_logging.INFO,
            ),
        )

    def log_warning(
        self,
        message: str,
    ) -> str:
        return self.log(
            message,
            self._log_options_manager.generate_modified_defaults(
                self._options,
                log_level=_logging.WARNING,
            ),
        )

    def log_error(
        self,
        message: str,
    ) -> str:
        return self.log(
            message,
            self._log_options_manager.generate_modified_defaults(
                self._options,
                log_level=_logging.ERROR,
            ),
        )

    def log_critical(
        self,
        message: str,
    ) -> str:
        return self.log(
            message,
            self._log_options_manager.generate_modified_defaults(
                self._options,
                log_level=_logging.CRITICAL,
            ),
        )
