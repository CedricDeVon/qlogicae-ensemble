from enum import Enum

__all__ = (
    "TimeZone",
)

class TimeZone(Enum):
    UTC = 0
    LOCAL = 1
    CUSTOM = 2
    NONE = 3
