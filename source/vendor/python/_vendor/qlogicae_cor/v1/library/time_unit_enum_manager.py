from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from qlogicae_cor.v1.library.enum_conversion_value import (
        EnumConversionValue,
    )

_enum_conversion_value: Any = None
_time_unit: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _enum_conversion_value
    global _time_unit

    import qlogicae_cor.v1.library.enum_conversion_value
    import qlogicae_cor.v1.library.time_unit

    _enum_conversion_value = (
        qlogicae_cor.v1.library.enum_conversion_value.EnumConversionValue
    )
    _time_unit = (
        qlogicae_cor.v1.library.time_unit.TimeUnit
    )

    _handle_dynamic_imports = lambda: None


class TimeUnitEnumManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def convert_value(
        self,
        input_type: object,
        output_type: EnumConversionValue | None = None,
    ) -> object:
        if output_type is None:
            output_type = _enum_conversion_value.STRING

        match output_type:
            case _enum_conversion_value.STRING:
                match input_type:
                    case _time_unit.NANOSECOND:
                        return "nanosecond"

                    case _time_unit.MICROSECOND:
                        return "microsecond"

                    case _time_unit.MILLISECOND:
                        return "millisecond"

                    case _time_unit.SECOND:
                        return "second"

                    case _time_unit.MINUTE:
                        return "minute"

                    case _time_unit.HOUR:
                        return "hour"

                    case _time_unit.DAY:
                        return "day"

                    case _time_unit.WEEK:
                        return "week"

                    case _time_unit.MONTH:
                        return "month"

                    case _time_unit.YEAR:
                        return "year"

                    case _time_unit.DECADE:
                        return "decade"

                    case _time_unit.CENTURY:
                        return "century"

                    case _time_unit.MILLENNIUM:
                        return "millennium"

                    case _:
                        return "none"

            case _enum_conversion_value.ENUM:
                match str(input_type).lower():
                    case "nanosecond" | "ns":
                        return _time_unit.NANOSECOND

                    case "microsecond" | "us":
                        return _time_unit.MICROSECOND

                    case "millisecond" | "ms":
                        return _time_unit.MILLISECOND

                    case "second" | "sec":
                        return _time_unit.SECOND

                    case "minute" | "min":
                        return _time_unit.MINUTE

                    case "hour" | "hr":
                        return _time_unit.HOUR

                    case "day" | "d":
                        return _time_unit.DAY

                    case "week" | "wk":
                        return _time_unit.WEEK

                    case "month" | "mon":
                        return _time_unit.MONTH

                    case "year" | "yr":
                        return _time_unit.YEAR

                    case "decade" | "deca":
                        return _time_unit.DECADE

                    case "century" | "cen":
                        return _time_unit.CENTURY

                    case "millennium" | "mil":
                        return _time_unit.MILLENNIUM

                    case _:
                        return _time_unit.NONE

            case _:
                return _enum_conversion_value.NONE
