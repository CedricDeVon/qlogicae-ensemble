from __future__ import annotations

__all__ = (
    "JsonFileIoManager",
)

from typing import Any

_json: Any = None
_Path: Any = None
_SingletonManager: Any = None
_JsonManager: Any = None
_TextEncodingManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _json
    global _Path
    global _SingletonManager
    global _JsonManager
    global _TextEncodingManager

    import json
    from pathlib import Path

    from .json_manager import JsonManager
    from .singleton_manager import SingletonManager
    from .text_encoding_manager import TextEncodingManager

    _json = json
    _Path = Path
    _SingletonManager = (
        SingletonManager
    )
    _JsonManager = (
        JsonManager
    )
    _TextEncodingManager = (
        TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class JsonFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._json_manager = _SingletonManager.get_singleton(
            _JsonManager
        )
        self._text_encoding_manager = _SingletonManager.get_singleton(
            _TextEncodingManager
        )

    def read_file(
        self,
        file_path: str,
    ) -> Any:
        path = _Path(file_path)

        output_data: Any = {}

        with path.open(
            mode="r",
            encoding=(
                self._text_encoding_manager.selected_encoding
            ),
        ) as file:
            output_data = _json.load(file) or {}

        return output_data

    def write_file(
        self,
        file_path: str,
        data: Any,
    ) -> bool:
        path = _Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            mode="w",
            encoding=(
                self._text_encoding_manager.selected_encoding
            ),
        ) as file:
            _json.dump(
                data,
                file,
                indent=self._json_manager.indent_count,
                ensure_ascii=(
                    self._json_manager.is_ascii_format_enabled
                ),
                sort_keys=(
                    self._json_manager.is_key_sortable
                ),
            )

        return True
