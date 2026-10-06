from __future__ import annotations

__all__ = (
    "LogOptionsManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:

    from .log_options import (
        LogOptions,
    )

_logging: Any = None
_LogOptions: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _LogOptions

    import logging

    from .log_options import (
        LogOptions,
    )

    _logging = logging
    _LogOptions = (
        LogOptions
    )

    _handle_dynamic_imports = lambda: None


class LogOptionsManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def generate_modified_defaults(
        self,
        default_log_options: LogOptions,
        log_level: object | None = None,
    ) -> LogOptions:
        if log_level is None:
            log_level = _logging.DEBUG

        value: LogOptions = _LogOptions(
            is_enabled=default_log_options.is_enabled,
            is_verbose_enabled=(
                default_log_options.is_verbose_enabled
            ),
            log_level=log_level,
            stack_level=default_log_options.stack_level,
        )

        return value
