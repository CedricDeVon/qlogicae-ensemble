from __future__ import annotations

__all__ = (
    "LogFormat",
)

import logging
from typing import Any

_SingletonManager: Any = None
_TimestampManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _SingletonManager
    global _TimestampManager

    from .singleton_manager import SingletonManager
    from .timestamp_manager import TimestampManager

    _SingletonManager = (
        SingletonManager
    )
    _TimestampManager = (
        TimestampManager
    )

    _handle_dynamic_imports = lambda: None


class LogFormat(logging.Formatter):
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        timestamp: str = (
            _SingletonManager.get_singleton(
                _TimestampManager,
            ).generate_current_timestamp()
        )

        value: str = (
            f"[ {timestamp} ] "
            f"[ {record.levelname} ] "
            f"{record.getMessage()}"
        )

        return value
