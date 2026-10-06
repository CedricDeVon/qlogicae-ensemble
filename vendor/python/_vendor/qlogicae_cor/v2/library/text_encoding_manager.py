
__all__ = (
    "TextEncodingManager",
)

class TextEncodingManager:
    __slots__ = (
        "_selected_encoding",
    )

    def __init__(self) -> None:
        self._selected_encoding: str = "utf-8"

    @property
    def selected_encoding(self) -> str:
        return self._selected_encoding

    @selected_encoding.setter
    def selected_encoding(self, value: str) -> None:
        self._selected_encoding = value
