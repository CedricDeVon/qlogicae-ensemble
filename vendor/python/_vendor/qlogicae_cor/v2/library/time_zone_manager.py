from __future__ import annotations

__all__ = (
    "TimeZoneManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import tzinfo

_EnumConversionValue: Any = None
_SingletonManager: Any = None
_TimeZoneEnumManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _EnumConversionValue
    global _SingletonManager
    global _TimeZoneEnumManager

    from .enum_conversion_value import EnumConversionValue
    from .singleton_manager import SingletonManager
    from .time_zone_enum_manager import TimeZoneEnumManager

    _EnumConversionValue = (
        EnumConversionValue
    )
    _SingletonManager = (
        SingletonManager
    )
    _TimeZoneEnumManager = (
        TimeZoneEnumManager
    )

    _handle_dynamic_imports = lambda: None


class TimeZoneManager:
    __slots__ = (
        "_selected_time_zone_type",
        "_valid_time_zone_types",
        "_time_zone_enum_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._time_zone_enum_manager = (
            _SingletonManager.get_singleton(
                _TimeZoneEnumManager
            )
        )

        self._selected_time_zone_type: str = "local"
        self._valid_time_zone_types: set[str] = {
            "local",
            "utc",
        }

    @property
    def selected_time_zone_type(self) -> str:
        return self._selected_time_zone_type

    @selected_time_zone_type.setter
    def selected_time_zone_type(
        self,
        value: str,
    ) -> None:
        if value not in self._valid_time_zone_types:
            raise ValueError(
                "time zones must include the followwing: "
                f"{self._valid_time_zone_types}",
            )

        self._selected_time_zone_type = value

    @property
    def selected_time_zone(self) -> tzinfo:
        value: tzinfo = (
            self._time_zone_enum_manager.convert_value(
                self._selected_time_zone_type,
                _EnumConversionValue.CUSTOM,
            )
        )

        return value
