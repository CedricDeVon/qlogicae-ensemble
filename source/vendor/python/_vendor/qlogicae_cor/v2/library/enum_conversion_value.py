from enum import Enum

__all__ = (
    "EnumConversionValue",
)

class EnumConversionValue(Enum):
    STRING = 0
    ENUM = 1
    CUSTOM = 2
    NONE = 3
