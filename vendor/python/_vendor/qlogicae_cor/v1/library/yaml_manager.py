from __future__ import annotations

from typing import Any

_Path: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path

    from pathlib import Path

    _Path = Path

    _handle_dynamic_imports = lambda: None

class YamlManager:
    __slots__ = (
        "_valid_file_extensions",
        "_is_key_sorting_enabled",
        "_is_default_flow_state_enabled",
        "_is_unicode_enabled",
        "_indent_count",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._valid_file_extensions: set[str] = {
            ".yaml",
            ".yml",
        }
        self._is_key_sorting_enabled: bool = False
        self._is_default_flow_state_enabled: bool = False
        self._is_unicode_enabled: bool = True
        self._indent_count: int = 4

    @property
    def valid_file_extensions(self) -> set[str]:
        return self._valid_file_extensions

    def is_valid(self, file_path: str) -> bool:
        path = _Path(file_path)

        return path.suffix.lower() in self.valid_file_extensions

    @property
    def is_key_sorting_enabled(self) -> bool:
        return self._is_key_sorting_enabled

    @is_key_sorting_enabled.setter
    def is_key_sorting_enabled(self, value: bool) -> None:
        self._is_key_sorting_enabled = value

    @property
    def is_default_flow_state_enabled(
        self,
    ) -> bool:
        return self._is_default_flow_state_enabled

    @is_default_flow_state_enabled.setter
    def is_default_flow_state_enabled(self, value: bool) -> None:
        self._is_default_flow_state_enabled = value

    @property
    def is_unicode_enabled(self) -> bool:
        return self._is_unicode_enabled

    @is_unicode_enabled.setter
    def is_unicode_enabled(self, value: bool) -> None:
        self._is_unicode_enabled = value

    @property
    def indent_count(self) -> int:
        return self._indent_count

    @indent_count.setter
    def indent_count(self, value: int) -> None:
        if value < 0:
            raise ValueError("indent_count must be non-negative.")
        self._indent_count = value

