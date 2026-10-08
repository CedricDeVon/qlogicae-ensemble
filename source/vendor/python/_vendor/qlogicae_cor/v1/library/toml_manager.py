from __future__ import annotations

from typing import Any

_Path: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path

    from pathlib import Path

    _Path = Path

    _handle_dynamic_imports = lambda: None


class TomlManager:
    __slots__ = (
        "_valid_file_extensions",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._valid_file_extensions: set[str] = {
            ".toml",
        }

    @property
    def valid_file_extensions(self) -> set[str]:
        return self._valid_file_extensions

    def is_valid(
        self,
        file_path: str,
    ) -> bool:
        path = _Path(file_path)

        return (
            path.suffix.lower()
            in self.valid_file_extensions
        )
