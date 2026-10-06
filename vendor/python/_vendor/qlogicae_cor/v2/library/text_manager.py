from typing import Any

__all__ = (
    "TextManager",
)

class TextManager:
    __slots__ = (
        "_valid_file_extensions",
    )

    def __init__(self) -> None:
        self._valid_file_extensions: set[str] = {".txt"}

    @property
    def valid_file_extensions(self) -> set[str]:
        return self._valid_file_extensions

    def is_valid(self, file_path: Any) -> bool:
        if file_path.suffix.lower() not in self.valid_file_extensions:
            return False

        return True

