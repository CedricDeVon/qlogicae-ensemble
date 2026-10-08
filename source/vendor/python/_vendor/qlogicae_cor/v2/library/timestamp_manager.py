from __future__ import annotations

__all__ = (
    "TimestampManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .time_unit import TimeUnit
    from .timestamp import Timestamp

_time: Any = None
_UTC: Any = None
_datetime: Any = None
_SingletonManager: Any = None
_TimeUnit: Any = None
_TimeZoneManager: Any = None
_Timestamp: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _time
    global _UTC
    global _datetime
    global _SingletonManager
    global _TimeUnit
    global _TimeZoneManager
    global _Timestamp

    import time
    from datetime import UTC, datetime

    from .singleton_manager import SingletonManager
    from .time_unit import TimeUnit
    from .time_zone_manager import TimeZoneManager
    from .timestamp import Timestamp

    _time = time
    _UTC = UTC
    _datetime = datetime
    _SingletonManager = (
        SingletonManager
    )
    _TimeUnit = (
        TimeUnit
    )
    _TimeZoneManager = (
        TimeZoneManager
    )
    _Timestamp = (
        Timestamp
    )

    _handle_dynamic_imports = lambda: None


class TimestampManager:
    __slots__ = (
        "_time_zone_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._time_zone_manager = (
            _SingletonManager.get_singleton(
                _TimeZoneManager
            )
        )

    def generate_current_timestamp(
        self,
        timestamp: Timestamp | None = None,
        time_unit: TimeUnit | None = None,
    ) -> str:
        if timestamp is None:
            timestamp = _Timestamp.ISO_DATE_STRING

        if time_unit is None:
            time_unit = _TimeUnit.NANOSECOND

        timestamp_nanoseconds = _time.time_ns()

        current = _datetime.fromtimestamp(
            timestamp_nanoseconds / 1_000_000_000,
            self._time_zone_manager.selected_time_zone,
        )

        match time_unit:
            case (
                _TimeUnit.NONE
                | _TimeUnit.SECOND
            ):
                fraction = ""

            case _TimeUnit.MILLISECOND:
                fraction = (
                    f".{timestamp_nanoseconds // 1_000_000 % 1_000:03d}"
                )

            case _TimeUnit.MICROSECOND:
                fraction = (
                    f".{timestamp_nanoseconds // 1_000 % 1_000_000:06d}"
                )

            case _TimeUnit.NANOSECOND:
                fraction = (
                    f".{timestamp_nanoseconds % 1_000_000_000:09d}"
                )

            case _:
                fraction = ""

        if current.tzinfo is _UTC:
            suffix = "Z"
        else:
            suffix = current.strftime("%z")

            if suffix:
                suffix = (
                    f"{suffix[:-2]}:{suffix[-2:]}"
                )

        match timestamp:
            case _Timestamp.ISO_DATE_STRING:
                prefix = current.strftime("%Y-%m-%dT%H:%M:%S")

            case _Timestamp.ISO_FILESYSTEM_STRING:
                prefix = current.strftime("%Y-%m-%dT%H-%M-%S")
                suffix = suffix.replace(":", "-")

            case _:
                return ""

        return "".join(
            (
                prefix,
                fraction,
                suffix,
            )
        )
