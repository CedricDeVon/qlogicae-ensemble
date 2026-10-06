from __future__ import annotations

__all__ = (
    "FilesystemMetadata",
)

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FilesystemMetadata:
    mode: int
    inode: int
    device: int
    hard_links: int
    uid: int
    gid: int
    size: int
    access_time: float
    modification_time: float
    status_change_time: float
