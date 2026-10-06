from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import tzinfo

_enum_conversion_value: Any = None
_singleton_manager: Any = None
_time_zone_enum_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _enum_conversion_value
    global _singleton_manager
    global _time_zone_enum_manager

    import qlogicae_cor.v1.library.enum_conversion_value
    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.time_zone_enum_manager

    _enum_conversion_value = (
        qlogicae_cor.v1.library.enum_conversion_value.EnumConversionValue
    )
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _time_zone_enum_manager = (
        qlogicae_cor.v1.library.time_zone_enum_manager.TimeZoneEnumManager
    )

    _handle_dynamic_imports = lambda: None


class TimeZoneManager:
    __slots__ = (
        "_selected_time_zone_type",
        "_valid_time_zone_types",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

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
            _singleton_manager.get_singleton(
                _time_zone_enum_manager,
            ).convert_value(
                self._selected_time_zone_type,
                _enum_conversion_value.CUSTOM,
            )
        )

        return value
