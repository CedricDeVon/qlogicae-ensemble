from __future__ import annotations

__all__ = (
    "ScriptProcessEnumManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .enum_conversion_value import (
        EnumConversionValue,
    )

_EnumConversionValue: Any = None
_ScriptProcess: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _EnumConversionValue
    global _ScriptProcess

    from .enum_conversion_value import EnumConversionValue
    from .script_process import ScriptProcess

    _EnumConversionValue = (
        EnumConversionValue
    )
    _ScriptProcess = (
        ScriptProcess
    )

    _handle_dynamic_imports = lambda: None


class ScriptProcessEnumManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def convert_value(
        self,
        input_type: object,
        output_type: EnumConversionValue | None = None,
    ) -> Any:
        if output_type is None:
            output_type = _EnumConversionValue.STRING

        match output_type:
            case _EnumConversionValue.STRING:
                match input_type:
                    case _ScriptProcess.SHELL:
                        return "shell"

                    case _ScriptProcess.SUBPROCESS:
                        return "subprocess"

                    case _:
                        return "none"

            case _EnumConversionValue.ENUM:
                match str(input_type).lower():
                    case "shell":
                        return _ScriptProcess.SHELL

                    case "subprocess":
                        return _ScriptProcess.SUBPROCESS

                    case _:
                        return _ScriptProcess.SUBPROCESS

            case _:
                return _EnumConversionValue.NONE
