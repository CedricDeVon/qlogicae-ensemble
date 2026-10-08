from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.enum_conversion_value import (
        EnumConversionValue,
    )

_enum_conversion_value: Any = None
_script_process: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _enum_conversion_value
    global _script_process

    import qlogicae_cor.v1.library.enum_conversion_value
    import qlogicae_cor.v1.library.script_process

    _enum_conversion_value = (
        qlogicae_cor.v1.library.enum_conversion_value.EnumConversionValue
    )
    _script_process = (
        qlogicae_cor.v1.library.script_process.ScriptProcess
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
            output_type = _enum_conversion_value.STRING

        match output_type:
            case _enum_conversion_value.STRING:
                match input_type:
                    case _script_process.SHELL:
                        return "shell"

                    case _script_process.SUBPROCESS:
                        return "subprocess"

                    case _:
                        return "none"

            case _enum_conversion_value.ENUM:
                match str(input_type).lower():
                    case "shell":
                        return _script_process.SHELL

                    case "subprocess":
                        return _script_process.SUBPROCESS

                    case _:
                        return _script_process.SUBPROCESS

            case _:
                return _enum_conversion_value.NONE
