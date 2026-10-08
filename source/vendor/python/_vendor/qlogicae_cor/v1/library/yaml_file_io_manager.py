from __future__ import annotations

from typing import Any

_Path: Any = None
_yaml: Any = None
_singleton_manager: Any = None
_text_encoding_manager: Any = None
_yaml_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _Path
    global _yaml
    global _singleton_manager
    global _text_encoding_manager
    global _yaml_manager

    from pathlib import Path

    import yaml

    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.text_encoding_manager
    import qlogicae_cor.v1.library.yaml_manager

    _Path = Path
    _yaml = yaml
    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _text_encoding_manager = (
        qlogicae_cor.v1.library.text_encoding_manager.TextEncodingManager
    )
    _yaml_manager = (
        qlogicae_cor.v1.library.yaml_manager.YamlManager
    )

    _handle_dynamic_imports = lambda: None


class YamlFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> object:
        path = _Path(file_path)

        with path.open(
            mode="r",
            encoding=_singleton_manager.get_singleton(
                _text_encoding_manager,
            ).selected_encoding,
        ) as file:
            return _yaml.safe_load(file) or {}

    def write_file(
        self,
        file_path: str,
        data: object,
    ) -> bool:
        path = _Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        manager = _singleton_manager.get_singleton(
            _yaml_manager.YamlManager,
        )

        with path.open(
            mode="w",
            encoding=_singleton_manager.get_singleton(
                _text_encoding_manager,
            ).selected_encoding,
        ) as file:
            _yaml.safe_dump(
                data,
                file,
                sort_keys=manager.is_key_sorting_enabled,
                default_flow_style=manager.is_default_flow_state_enabled,
                allow_unicode=manager.is_unicode_enabled,
                indent=manager.indent_count,
            )

        return True

    def format_to_string(
        self,
        value: str,
    ) -> object:
        manager = _singleton_manager.get_singleton(
            _yaml_manager.YamlManager,
        )

        return (
            _yaml.dump(
                value,
                sort_keys=manager.is_key_sorting_enabled,
                default_flow_style=manager.is_default_flow_state_enabled,
                allow_unicode=manager.is_unicode_enabled,
                indent=manager.indent_count,
            )
            or ""
        )
