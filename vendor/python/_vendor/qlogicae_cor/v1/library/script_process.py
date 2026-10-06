from enum import Enum


class ScriptProcess(Enum):
    SHELL = 0
    SUBPROCESS = 1
    NONE = 2
