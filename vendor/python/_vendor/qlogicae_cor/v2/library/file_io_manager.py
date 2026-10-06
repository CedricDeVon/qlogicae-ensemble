from __future__ import annotations

__all__ = (
    "FileIoManager",
)

from typing import Any

_Path: Any = None
_singleton_manager: Any = None
_text_encoding_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path
    global _singleton_manager
    global _text_encoding_manager

    from pathlib import Path

    from .singleton_manager import SingletonManager
    from .text_encoding_manager import (
        TextEncodingManager,
    )

    _Path = Path
    _singleton_manager = (
        SingletonManager
    )
    _text_encoding_manager = (
        TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class FileIoManager:
    __slots__ = (
        "_text_encoding_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._text_encoding_manager = _singleton_manager.get_singleton(
            _text_encoding_manager
        )

    def read_file(
        self,
        file_path: str,
    ) -> str:
        path = _Path(file_path)

        with path.open(
            mode="r",
            encoding=(
                self._text_encoding_manager.selected_encoding
            ),
        ) as file:
            return file.read() or ""

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
            file.write(str(data))

        return True
