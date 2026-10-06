from __future__ import annotations

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

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.text_encoding_manager

    _Path = Path
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _text_encoding_manager = (
        qlogicae_cor.v1.library.text_encoding_manager.TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class FileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> str:
        path = _Path(file_path)

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
                _singleton_manager
                .get_singleton(
                    _text_encoding_manager,
                )
                .selected_encoding
            ),
        ) as file:
            file.write(str(data))

        return True
