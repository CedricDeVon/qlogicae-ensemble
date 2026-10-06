from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class FolderEntityFileSystemTreeSetupOptions:
    name: str = "folder"
    entities: list[Any] = field(default_factory=list)

