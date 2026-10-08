from __future__ import annotations

__all__ = (
    "EnumConversionValueEnumManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .enum_conversion_value import (
        EnumConversionValue,
    )

_enum_conversion_value: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _enum_conversion_value

    from .enum_conversion_value import (
        EnumConversionValue,
    )

    _enum_conversion_value = (
        EnumConversionValue
    )

    _handle_dynamic_imports = lambda: None


class EnumConversionValueEnumManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def convert_value(
        self,
        input_type: object,
        output_type: EnumConversionValue | None = None
    ) -> Any:
        if output_type is None:
            output_type = EnumConversionValue.STRING

        match output_type:
            case _enum_conversion_value.STRING:
                match input_type:
                    case _enum_conversion_value.STRING:
                        return "string"

                    case _enum_conversion_value.ENUM:
                        return "enum"

                    case _enum_conversion_value.CUSTOM:
                        return "custom"

                    case _:
                        return "none"

            case _enum_conversion_value.ENUM:
                match str(input_type).lower():
                    case "string":
                        return _enum_conversion_value.STRING

                    case "none":
                        return _enum_conversion_value.ENUM

                    case "custom":
                        return _enum_conversion_value.CUSTOM

                    case _:
                        return _enum_conversion_value.NONE

            case _:
                return _enum_conversion_value.NONE
