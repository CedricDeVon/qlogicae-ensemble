from enum import Enum


class TimeZone(Enum):
    UTC = 0
    LOCAL = 1
    CUSTOM = 2
    NONE = 3
