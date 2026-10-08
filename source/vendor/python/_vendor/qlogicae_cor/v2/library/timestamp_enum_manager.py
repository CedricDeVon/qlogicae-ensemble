from __future__ import annotations

__all__ = (
    "TimestampEnumManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .enum_conversion_value import (
        EnumConversionValue,
    )

_EnumConversionValue: Any = None
_Timestamp: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _EnumConversionValue
    global _Timestamp


    from .enum_conversion_value import EnumConversionValue
    from .timestamp import Timestamp

    _EnumConversionValue = (
        EnumConversionValue
    )
    _Timestamp = (
        Timestamp
    )

    _handle_dynamic_imports = lambda: None


class TimestampEnumManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def convert_value(
        self,
        input_type: Any,
        output_type: EnumConversionValue | None = None,
    ) -> object:
        if output_type is None:
            output_type = _EnumConversionValue.STRING

        match output_type:
            case _EnumConversionValue.STRING:
                match input_type:
                    case _Timestamp.ISO_DATE_STRING:
                        return "iso_date_string"

                    case _Timestamp.ISO_FILESYSTEM_STRING:
                        return "iso_filesystem_string"

                    case _:
                        return "iso_date_string"

            case _EnumConversionValue.ENUM:
                match input_type.lower():
                    case "local":
                        return _Timestamp.ISO_DATE_STRING

                    case "iso_filesystem_string":
                        return _Timestamp.ISO_FILESYSTEM_STRING

                    case _:
                        return _Timestamp.NONE

            case _:
                return _EnumConversionValue.NONE
