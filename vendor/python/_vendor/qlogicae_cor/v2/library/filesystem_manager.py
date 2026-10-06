from __future__ import annotations

__all__ = (
    "FilesystemManager",
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .folder_entity_filesystem_tree_setup_options import (
        FolderEntityFileSystemTreeSetupOptions,
    )

_shutil: Any = None
_Path: Any = None
_FileEntityFileSystemTreeSetupOptions: Any = None
_FolderEntityFileSystemTreeSetupOptions: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _shutil
    global _Path
    global _FileEntityFileSystemTreeSetupOptions
    global _FolderEntityFileSystemTreeSetupOptions

    import shutil
    from pathlib import Path

    from .file_entity_filesystem_tree_setup_options import (
        FileEntityFileSystemTreeSetupOptions,
    )
    from .folder_entity_filesystem_tree_setup_options import (
        FolderEntityFileSystemTreeSetupOptions,
    )

    _shutil = shutil
    _Path = Path
    _FileEntityFileSystemTreeSetupOptions = (
        FileEntityFileSystemTreeSetupOptions
    )
    _FolderEntityFileSystemTreeSetupOptions = (
        FolderEntityFileSystemTreeSetupOptions
    )

    _handle_dynamic_imports = lambda: None


class FilesystemManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def throw_if_filesystem_path_invalid(
        self,
        value: str,
    ) -> bool:
        path = _Path(value)

        if not path.exists():
            raise ValueError(
                f"filesystem path '{path}' is invalid"
            )

        return False

    def throw_if_file_path_invalid(
        self,
        value: str,
    ) -> bool:
        path = _Path(value)

        if not path.is_file():
            raise ValueError(
                f"file path '{path}' is invalid"
            )

        return False

    def throw_if_folder_path_invalid(
        self,
        value: str,
    ) -> bool:
        path = _Path(value)

        if not path.is_dir():
            raise ValueError(
                f"folder path '{path}' is invalid"
            )

        return False

    def is_filesystem_path_valid(
        self,
        value: str,
    ) -> bool:
        result: bool = _Path(value).exists()
        return result

    def is_file_path_valid(
        self,
        value: str,
    ) -> bool:
        result: bool = _Path(value).is_file()
        return result

    def is_folder_path_valid(
        self,
        value: str,
    ) -> bool:
        result: bool = _Path(value).is_dir()
        return result

    def clean_filesystem_path(
        self,
        path: str,
    ) -> bool:
        directory = _Path(path).resolve()

        protected_paths = {
            _Path(""),
            _Path("/"),
            _Path.home(),
        }

        if directory in protected_paths:
            raise ValueError(
                f"folder path '{path}' is protected"
            )

        if not directory.exists():
            return True

        if not directory.is_dir():
            raise ValueError(
                f"file path '{path}' is not a folder"
            )

        for item in directory.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()

            elif item.is_dir():
                _shutil.rmtree(item)

        return True

    def copy_filesystem_path(
        self,
        first_path: str,
        second_path: str,
    ) -> bool:
        fs_first_path = _Path(first_path)
        fs_second_path = _Path(second_path)

        if fs_first_path.is_dir():
            _shutil.copytree(
                fs_first_path,
                fs_second_path,
                dirs_exist_ok=True,
            )

        elif fs_first_path.is_file():
            fs_second_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            _shutil.copy2(
                fs_first_path,
                fs_second_path,
            )

        else:
            return False

        return True

    def move_filesystem_path(
        self,
        first_path: str,
        second_path: str,
    ) -> bool:
        source = _Path(first_path)
        destination = _Path(second_path)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        _shutil.move(
            str(source),
            str(destination),
        )

        return True

    def setup_filesystem_tree(
        self,
        parent_path: str,
        options: FolderEntityFileSystemTreeSetupOptions,
    ) -> None:
        path = _Path(parent_path)

        if not path.exists():
            raise ValueError(
                f"filesystem path '{path}' is invalid"
            )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        for entity in options.entities or []:
            entity_path = path / entity.name

            if isinstance(
                entity,
                _FolderEntityFileSystemTreeSetupOptions,
            ):
                entity_path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                self.setup_filesystem_tree(
                    entity_path,
                    entity,
                )

            elif isinstance(
                entity,
                _FileEntityFileSystemTreeSetupOptions,
            ):
                if not entity_path.exists():
                    entity_path.write_text(
                        entity.content,
                        encoding=entity.encoding,
                    )

    def rename_filesystem_entity(
        self,
        source: str,
        destination: str,
    ) -> bool:
        _Path(source).rename(destination)

        return True

    def setup_filesystem_tree_path(
        self,
        directory: str,
    ) -> bool:
        _Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )

        return True

