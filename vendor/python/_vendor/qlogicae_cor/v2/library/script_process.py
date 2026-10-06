from enum import Enum

__all__ = (
    "ScriptProcess",
)

class ScriptProcess(Enum):
    SHELL = 0
    SUBPROCESS = 1
    NONE = 2
