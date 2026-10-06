from __future__ import annotations

__all__ = (
    "JsonManager",
)

from typing import Any

_Path: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path

    from pathlib import Path

    _Path = Path

    _handle_dynamic_imports = lambda: None

class JsonManager:
    __slots__ = (
        "_valid_file_extensions",
        "_is_ascii_format_enabled",
        "_indent_count",
        "_is_key_sortable",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._valid_file_extensions: set[str] = {
            ".json",
        }
        self._is_ascii_format_enabled = False
        self._indent_count = 4
        self._is_key_sortable = False

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

    @property
    def is_ascii_format_enabled(self) -> bool:
        return self._is_ascii_format_enabled

    @is_ascii_format_enabled.setter
    def is_ascii_format_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_ascii_format_enabled = value

    @property
    def indent_count(self) -> int:
        return self._indent_count

    @indent_count.setter
    def indent_count(
        self,
        value: int,
    ) -> None:
        if value < 0:
            raise ValueError(
                "indent_count must be non-negative.",
            )

        self._indent_count = value

    @property
    def is_key_sortable(self) -> bool:
        return self._is_key_sortable

    @is_key_sortable.setter
    def is_key_sortable(
        self,
        value: bool,
    ) -> None:
        self._is_key_sortable = value
