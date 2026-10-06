from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FileEntityFileSystemTreeSetupOptions:
    content: str = "data"
    name: str = "file"
    encoding: str = "utf-8"
    is_modifiable: bool = False
