from __future__ import annotations

import logging
from typing import Any

_singleton_manager: Any = None
_timestamp_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _logging
    global _singleton_manager
    global _timestamp_manager

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.timestamp_manager

    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _timestamp_manager = (
        qlogicae_cor.v1.library.timestamp_manager.TimestampManager
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
            _singleton_manager.get_singleton(
                _timestamp_manager,
            ).generate_current_timestamp()
        )

        value: str = (
            f"[ {timestamp} ] "
            f"[ {record.levelname} ] "
            f"{record.getMessage()}"
        )

        return value
