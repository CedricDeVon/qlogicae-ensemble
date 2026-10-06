from enum import Enum


class Timestamp(Enum):
    ISO_DATE_STRING = 0
    ISO_FILESYSTEM_STRING = 1
    NONE = 2
