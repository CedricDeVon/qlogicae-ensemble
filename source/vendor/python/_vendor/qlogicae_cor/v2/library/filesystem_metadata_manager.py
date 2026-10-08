from __future__ import annotations

__all__ = (
    "FilesystemMetadataManager",
)

from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    pass


_Path: Any = None
_FilesystemMetadata: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _FilesystemMetadata

    from pathlib import Path

    from .filesystem_metadata import FilesystemMetadata

    _Path = Path
    _FilesystemMetadata = (
        FilesystemMetadata
    )

    _handle_dynamic_imports = lambda: None


class FilesystemMetadataManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def read_metadata(
        self,
        filesystem_path: str,
    ) -> Any:
        stat = _Path(filesystem_path).stat()

        return cast(
            _FilesystemMetadata,
            _FilesystemMetadata(
                mode=stat.st_mode,
                inode=stat.st_ino,
                device=stat.st_dev,
                hard_links=stat.st_nlink,
                uid=stat.st_uid,
                gid=stat.st_gid,
                size=stat.st_size,
                access_time=stat.st_atime,
                modification_time=stat.st_mtime,
                status_change_time=stat.st_ctime,
            )
        )
