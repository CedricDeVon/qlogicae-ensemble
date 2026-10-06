from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.log_options import (
        LogOptions,
    )

_logging: Any = None
_console_log_manager: Any = None
_file_log_manager: Any = None
_log_options_manager: Any = None
_singleton_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _console_log_manager
    global _file_log_manager
    global _log_options_manager
    global _singleton_manager

    import logging

    from qlogicae_cor.v1.library.console_log_manager import (
        ConsoleLogManager,
    )
    from qlogicae_cor.v1.library.file_log_manager import (
        FileLogManager,
    )
    from qlogicae_cor.v1.library.log_options_manager import (
        LogOptionsManager,
    )
    from qlogicae_cor.v1.library.singleton_manager import (
        SingletonManager,
    )

    _logging = logging
    _console_log_manager = ConsoleLogManager
    _file_log_manager = FileLogManager
    _log_options_manager = LogOptionsManager
    _singleton_manager = SingletonManager

    _handle_dynamic_imports = lambda: None


class LogManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def log(
        self,
        message: str,
        console_options: LogOptions,
        file_options: LogOptions,
    ) -> str:
        _singleton_manager.get_singleton(
            _console_log_manager,
        ).log(
            message,
            console_options,
        )

        _singleton_manager.get_singleton(
            _file_log_manager,
        ).log(
            message,
            file_options,
        )

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
                _singleton_manager.get_singleton(
                    _console_log_manager,
                ).options,
                log_level=_logging.DEBUG,
            ),
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                _singleton_manager.get_singleton(
                    _file_log_manager,
                ).options,
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
                _singleton_manager.get_singleton(
                    _console_log_manager,
                ).options,
                log_level=_logging.INFO,
            ),
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                _singleton_manager.get_singleton(
                    _file_log_manager,
                ).options,
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
                _singleton_manager.get_singleton(
                    _console_log_manager,
                ).options,
                log_level=_logging.WARNING,
            ),
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                _singleton_manager.get_singleton(
                    _file_log_manager,
                ).options,
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
                _singleton_manager.get_singleton(
                    _console_log_manager,
                ).options,
                log_level=_logging.ERROR,
            ),
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                _singleton_manager.get_singleton(
                    _file_log_manager,
                ).options,
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
                _singleton_manager.get_singleton(
                    _console_log_manager,
                ).options,
                log_level=_logging.CRITICAL,
            ),
            _singleton_manager.get_singleton(
                _log_options_manager,
            ).generate_modified_defaults(
                _singleton_manager.get_singleton(
                    _file_log_manager,
                ).options,
                log_level=_logging.CRITICAL,
            ),
        )

    def shutdown(self) -> bool:
        _singleton_manager.get_singleton(
            _file_log_manager,
        ).shutdown()

        return True
