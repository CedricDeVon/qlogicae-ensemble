from __future__ import annotations

__all__ = (
    "TextFileIoManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

_pathlib: Any = None
_SingletonManager: Any = None
_TextEncodingManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _pathlib
    global _SingletonManager
    global _TextEncodingManager

    import pathlib

    from .singleton_manager import SingletonManager
    from .text_encoding_manager import TextEncodingManager

    _pathlib = pathlib
    _SingletonManager = (
        SingletonManager
    )
    _TextEncodingManager = (
        TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class TextFileIoManager:
    __slots__ = (
        "_text_encoding_manager",
    )

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._text_encoding_manager = (
            _SingletonManager.get_singleton(
                _TextEncodingManager
            )
        )

    def read_file(
        self,
        file_path: str,
    ) -> str:
        path: Path = _pathlib.Path(file_path)

        output_data = ""

        with path.open(
            mode="r",
            encoding=(
                self._text_encoding_manager
                    .selected_encoding
            ),
        ) as file:
            output_data = file.read() or ""

        return output_data

    def write_file(
        self,
        file_path: str,
        data: object,
    ) -> bool:
        path: Path = _pathlib.Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            mode="w",
            encoding=(
                self._text_encoding_manager
                    .selected_encoding
            ),
        ) as file:
            file.write(
                str(data),
            )

        return True
