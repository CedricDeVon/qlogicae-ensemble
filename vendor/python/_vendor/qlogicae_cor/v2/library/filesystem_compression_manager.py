from __future__ import annotations

__all__ = (
    "FilesystemCompressionManager",
)

from typing import Any

_zipfile: Any = None
_Path: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _zipfile
    global _Path

    import zipfile
    from pathlib import Path

    _zipfile = zipfile
    _Path = Path

    _handle_dynamic_imports = lambda: None


class FilesystemCompressionManager:
    def __init__(self) -> None:
        _handle_dynamic_imports()

    def get_zip_format_compression(
        self,
        value: str,
    ) -> int:
        result: int

        match value.lower():
            case "store" | "stored" | "none":
                result = _zipfile.ZIP_STORED

            case "deflate" | "deflated":
                result = _zipfile.ZIP_DEFLATED

            case "bz2" | "bzip2":
                result = _zipfile.ZIP_BZIP2

            case "lzma" | "xz":
                result = _zipfile.ZIP_LZMA

            case _:
                result = _zipfile.ZIP_DEFLATED

        return result

    def zip_extract(
        self,
        archive_path: str,
        destination_path: str,
        overwrite: bool = False,
    ) -> bool:
        fs_archive_path = _Path(archive_path)
        fs_destination_path = _Path(
            destination_path,
        ).resolve()

        fs_destination_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        with _zipfile.ZipFile(
            fs_archive_path,
            "r",
        ) as archive:
            for member in archive.infolist():
                target = (
                    fs_destination_path
                    / member.filename
                ).resolve()

                if (
                    fs_destination_path not in target.parents
                    and target != fs_destination_path
                ):
                    raise ValueError(
                        f"unsafe archive filesystem path "
                        f"'{member.filename}'"
                    )

                if not overwrite and target.exists():
                    continue

                archive.extract(
                    member,
                    fs_destination_path,
                )

        return True
