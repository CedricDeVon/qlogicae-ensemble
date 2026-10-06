from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.log_options import LogOptions

_logging: Any = None
_log_format: Any = None
_log_options: Any = None
_log_options_manager: Any = None
_singleton_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _log_format
    global _log_options
    global _log_options_manager
    global _singleton_manager

    import logging

    import qlogicae_cor.v1.library.log_format
    import qlogicae_cor.v1.library.log_options
    import qlogicae_cor.v1.library.log_options_manager
    import qlogicae_cor.v1.library.singleton_manager

    _logging = logging
    _log_format = qlogicae_cor.v1.library.log_format.LogFormat
    _log_options = qlogicae_cor.v1.library.log_options.LogOptions
    _log_options_manager = (
        qlogicae_cor.v1.library.log_options_manager.LogOptionsManager
    )
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )

    _handle_dynamic_imports = lambda: None


class ConsoleLogManager:
    __slots__ = (
        "_logger",
        "_options",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

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
            _log_format(),
        )

        self._logger.addHandler(
            handler,
        )

        self._options: LogOptions = _log_options()

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
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
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
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
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
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
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
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
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
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                self._options,
                log_level=_logging.CRITICAL,
            ),
        )
