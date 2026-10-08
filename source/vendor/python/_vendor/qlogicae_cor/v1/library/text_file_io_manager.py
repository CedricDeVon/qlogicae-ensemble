from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

_pathlib: Any = None
_singleton_manager: Any = None
_text_encoding_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _pathlib
    global _singleton_manager
    global _text_encoding_manager

    import pathlib

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.text_encoding_manager

    _pathlib = pathlib
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _text_encoding_manager = (
        qlogicae_cor.v1.library.text_encoding_manager.TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class TextFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> str:
        path: Path = _pathlib.Path(file_path)

        output_data = ""

        with path.open(
            mode="r",
            encoding=(
                _singleton_manager
                .get_singleton(
                    _text_encoding_manager,
                )
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
                _singleton_manager
                .get_singleton(
                    _text_encoding_manager,
                )
                .selected_encoding
            ),
        ) as file:
            file.write(
                str(data),
            )

        return True
