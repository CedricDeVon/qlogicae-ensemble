from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.enum_conversion_value import (
        EnumConversionValue,
    )

_enum_conversion_value: Any = None
_timestamp: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _enum_conversion_value
    global _timestamp


    import qlogicae_cor.v1.library.enum_conversion_value
    import qlogicae_cor.v1.library.timestamp

    _enum_conversion_value = (
        qlogicae_cor.v1.library.enum_conversion_value.EnumConversionValue
    )
    _timestamp = (
        qlogicae_cor.v1.library.timestamp.Timestamp
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
            output_type = _enum_conversion_value.STRING

        match output_type:
            case _enum_conversion_value.STRING:
                match input_type:
                    case _timestamp.ISO_DATE_STRING:
                        return "iso_date_string"

                    case _timestamp.ISO_FILESYSTEM_STRING:
                        return "iso_filesystem_string"

                    case _:
                        return "iso_date_string"

            case _enum_conversion_value.ENUM:
                match input_type.lower():
                    case "local":
                        return _timestamp.ISO_DATE_STRING

                    case "iso_filesystem_string":
                        return _timestamp.ISO_FILESYSTEM_STRING

                    case _:
                        return _timestamp.NONE

            case _:
                return _enum_conversion_value.NONE
