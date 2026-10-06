from __future__ import annotations

from typing import Any

_json: Any = None
_Path: Any = None
_singleton_manager: Any = None
_json_manager: Any = None
_text_encoding_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _json
    global _Path
    global _singleton_manager
    global _json_manager
    global _text_encoding_manager

    import json
    from pathlib import Path

    import qlogicae_cor.v1.library.json_manager
    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.text_encoding_manager

    _json = json
    _Path = Path
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _json_manager = (
        qlogicae_cor.v1.library.json_manager.JsonManager
    )
    _text_encoding_manager = (
        qlogicae_cor.v1.library.text_encoding_manager.TextEncodingManager
    )

    _handle_dynamic_imports = lambda: None


class JsonFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> Any:
        path = _Path(file_path)

        output_data: Any = {}

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

        manager: _json_manager = (
            _singleton_manager
            .get_singleton(
                _json_manager,
            )
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
            _json.dump(
                data,
                file,
                indent=manager.indent_count,
                ensure_ascii=(
                    manager.is_ascii_format_enabled
                ),
                sort_keys=(
                    manager.is_key_sortable
                ),
            )

        return True
