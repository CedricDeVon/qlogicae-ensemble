from __future__ import annotations

__all__ = (
    "TimeZoneEnumManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .enum_conversion_value import EnumConversionValue

_datetime: Any = None
_UTC: Any = None
_EnumConversionValue: Any = None
_TimeZone: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _datetime
    global _UTC
    global _EnumConversionValue
    global _TimeZone

    from datetime import UTC, datetime

    from .enum_conversion_value import EnumConversionValue
    from .time_zone import TimeZone

    _datetime = datetime
    _UTC = UTC
    _EnumConversionValue = (
        EnumConversionValue
    )
    _TimeZone = (
        TimeZone
    )

    _handle_dynamic_imports = lambda: None


class TimeZoneEnumManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def convert_value(
        self,
        input_type: object,
        output_type: EnumConversionValue | None = None,
    ) -> object:
        if output_type is None:
            output_type = _EnumConversionValue.STRING

        match output_type:
            case _EnumConversionValue.STRING:
                match input_type:
                    case _TimeZone.LOCAL:
                        return "local"

                    case _TimeZone.UTC:
                        return "utc"

                    case _TimeZone.CUSTOM:
                        return "custom"

                    case _:
                        return "local"

            case _EnumConversionValue.ENUM:
                match str(input_type).lower():
                    case "local":
                        return _TimeZone.LOCAL

                    case "utc":
                        return _TimeZone.UTC

                    case "custom":
                        return _TimeZone.CUSTOM

                    case _:
                        return _TimeZone.LOCAL

            case _EnumConversionValue.CUSTOM:
                match str(input_type).lower():
                    case "local":
                        return _datetime.now().astimezone().tzinfo

                    case "utc":
                        return _UTC

                    case "custom":
                        return _datetime.now().astimezone().tzinfo

                    case _:
                        return _datetime.now().astimezone().tzinfo

            case _:
                return _EnumConversionValue.NONE
