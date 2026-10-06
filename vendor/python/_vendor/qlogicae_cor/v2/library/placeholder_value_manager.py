__all__ = (
    "PlaceholderValueManager",
)

class PlaceholderValueManager:
    __slots__ = (
        "_none",
        "_not_a_number",
        "_redacted",
        "_expunged",
    )

    def __init__(self) -> None:
        self._none: str = "none"
        self._not_a_number: str = "nan"
        self._redacted: str = "redacted"
        self._expunged: str = "expunged"

    @property
    def none(self) -> str:
        return self._none

    @none.setter
    def none(
        self,
        value: str,
    ) -> None:
        self._none = value

    @property
    def not_a_number(self) -> str:
        return self._not_a_number

    @not_a_number.setter
    def not_a_number(
        self,
        value: str,
    ) -> None:
        self._not_a_number = value

    @property
    def redacted(self) -> str:
        return self._redacted

    @redacted.setter
    def redacted(
        self,
        value: str,
    ) -> None:
        self._redacted = value

    @property
    def expunged(self) -> str:
        return self._expunged

    @expunged.setter
    def expunged(
        self,
        value: str,
    ) -> None:
        self._expunged = value
