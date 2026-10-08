from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.time_unit import TimeUnit
    from qlogicae_cor.v1.library.timestamp import Timestamp

_time: Any = None
_UTC: Any = None
_datetime: Any = None
_singleton_manager: Any = None
_time_unit: Any = None
_time_zone_manager: Any = None
_timestamp: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _time
    global _UTC
    global _datetime
    global _singleton_manager
    global _time_unit
    global _time_zone_manager
    global _timestamp

    import time
    from datetime import UTC, datetime

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.time_unit
    import qlogicae_cor.v1.library.time_zone_manager
    import qlogicae_cor.v1.library.timestamp

    _time = time
    _UTC = UTC
    _datetime = datetime
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _time_unit = (
        qlogicae_cor.v1.library.time_unit.TimeUnit
    )
    _time_zone_manager = (
        qlogicae_cor.v1.library.time_zone_manager.TimeZoneManager
    )
    _timestamp = (
        qlogicae_cor.v1.library.timestamp.Timestamp
    )

    _handle_dynamic_imports = lambda: None


class TimestampManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def generate_current_timestamp(
        self,
        timestamp: Timestamp | None = None,
        time_unit: TimeUnit | None = None,
    ) -> str:
        if timestamp is None:
            timestamp = _timestamp.ISO_DATE_STRING

        if time_unit is None:
            time_unit = _time_unit.NANOSECOND

        timestamp_nanoseconds = _time.time_ns()

        current = _datetime.fromtimestamp(
            timestamp_nanoseconds / 1_000_000_000,
            _singleton_manager.get_singleton(
                _time_zone_manager,
            ).selected_time_zone,
        )

        match time_unit:
            case (
                _time_unit.NONE
                | _time_unit.SECOND
            ):
                fraction = ""

            case _time_unit.MILLISECOND:
                fraction = (
                    f".{timestamp_nanoseconds // 1_000_000 % 1_000:03d}"
                )

            case _time_unit.MICROSECOND:
                fraction = (
                    f".{timestamp_nanoseconds // 1_000 % 1_000_000:06d}"
                )

            case _time_unit.NANOSECOND:
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
            case _timestamp.ISO_DATE_STRING:
                prefix = current.strftime("%Y-%m-%dT%H:%M:%S")

            case _timestamp.ISO_FILESYSTEM_STRING:
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
