from __future__ import annotations

from typing import Any

_singleton_manager: Any = None
_file_io_manager: Any = None
_json_file_io_manager: Any = None
_json_manager: Any = None
_toml_file_io_manager: Any = None
_toml_manager: Any = None
_yaml_file_io_manager: Any = None
_yaml_manager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _singleton_manager
    global _file_io_manager
    global _json_file_io_manager
    global _json_manager
    global _toml_file_io_manager
    global _toml_manager
    global _yaml_file_io_manager
    global _yaml_manager

    import qlogicae_cor.v1.library.file_io_manager
    import qlogicae_cor.v1.library.json_file_io_manager
    import qlogicae_cor.v1.library.json_manager
    import qlogicae_cor.v1.library.singleton_manager
    import qlogicae_cor.v1.library.toml_file_io_manager
    import qlogicae_cor.v1.library.toml_manager
    import qlogicae_cor.v1.library.yaml_file_io_manager
    import qlogicae_cor.v1.library.yaml_manager

    _singleton_manager = (
        qlogicae_cor.v1.library.singleton_manager.SingletonManager
    )
    _file_io_manager = (
        qlogicae_cor.v1.library.file_io_manager.FileIoManager
    )
    _json_file_io_manager = (
        qlogicae_cor.v1.library.json_file_io_manager.JsonFileIoManager
    )
    _json_manager = (
        qlogicae_cor.v1.library.json_manager.JsonManager
    )
    _toml_file_io_manager = (
        qlogicae_cor.v1.library.toml_file_io_manager.TomlFileIoManager
    )
    _toml_manager = (
        qlogicae_cor.v1.library.toml_manager.TomlManager
    )
    _yaml_file_io_manager = (
        qlogicae_cor.v1.library.yaml_file_io_manager.YamlFileIoManager
    )
    _yaml_manager = (
        qlogicae_cor.v1.library.yaml_manager.YamlManager
    )

    _handle_dynamic_imports = lambda: None


class DataFileIoManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_file(
        self,
        file_path: str,
    ) -> Any:
        if _singleton_manager.get_singleton(
            _yaml_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _yaml_file_io_manager,
            ).read_file(file_path)

        elif _singleton_manager.get_singleton(
            _json_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _json_file_io_manager,
            ).read_file(file_path)

        elif _singleton_manager.get_singleton(
            _toml_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _toml_file_io_manager,
            ).read_file(file_path)

        return _singleton_manager.get_singleton(
            _file_io_manager,
        ).read_file(file_path)

    def write_file(
        self,
        file_path: str,
        data: Any,
    ) -> Any:
        if _singleton_manager.get_singleton(
            _yaml_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _yaml_file_io_manager,
            ).write_file(file_path, data)

        elif _singleton_manager.get_singleton(
            _json_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _json_file_io_manager,
            ).write_file(file_path, data)

        elif _singleton_manager.get_singleton(
            _toml_manager,
        ).is_valid(file_path):
            return _singleton_manager.get_singleton(
                _toml_file_io_manager,
            ).write_file(file_path, data)

        return _singleton_manager.get_singleton(
            _file_io_manager,
        ).write_file(file_path, data)
