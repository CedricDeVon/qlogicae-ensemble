class AbstractManagerConfigurations:
    __slots__ = (
        "_is_override_enabled",
        "_is_enabled",
        "_is_runtime_execution_handling_enabled",
        "_is_edge_case_handling_enabled",
        "_is_error_handling_enabled",
    )

    def __init__(self) -> None:
        self._is_override_enabled: bool = False
        self._is_enabled: bool = True
        self._is_runtime_execution_handling_enabled: bool = True
        self._is_edge_case_handling_enabled: bool = True
        self._is_error_handling_enabled: bool = True

    @property
    def is_override_enabled(self) -> bool:
        return self._is_override_enabled

    @is_override_enabled.setter
    def is_override_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_override_enabled = value

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_enabled = value

    @property
    def is_runtime_execution_handling_enabled(self) -> bool:
        return self._is_runtime_execution_handling_enabled

    @is_runtime_execution_handling_enabled.setter
    def is_runtime_execution_handling_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_runtime_execution_handling_enabled = value

    @property
    def is_edge_case_handling_enabled(self) -> bool:
        return self._is_edge_case_handling_enabled

    @is_edge_case_handling_enabled.setter
    def is_edge_case_handling_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_edge_case_handling_enabled = value

    @property
    def is_error_handling_enabled(self) -> bool:
        return self._is_error_handling_enabled

    @is_error_handling_enabled.setter
    def is_error_handling_enabled(
        self,
        value: bool,
    ) -> None:
        self._is_error_handling_enabled = value

    def is_disabled_for_handling(
        self,
        conditions: bool = False,
    ) -> bool:
        return not self.is_enabled_for_runtime_execution_handling() or (
            self.is_enabled_for_edge_case_handling() and conditions
        )

    def is_enabled_for_runtime_execution_handling(
        self,
    ) -> bool:
        return (
            self.is_enabled
            if self.is_override_enabled
            else self.is_runtime_execution_handling_enabled
        )

    def is_enabled_for_edge_case_handling(
        self,
    ) -> bool:
        return (
            self.is_enabled
            if self.is_override_enabled
            else self.is_edge_case_handling_enabled
        )

    def is_enabled_for_error_handling(
        self,
    ) -> bool:
        return (
            self.is_enabled
            if self.is_override_enabled
            else self.is_error_handling_enabled
        )
