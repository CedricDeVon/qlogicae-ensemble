from qlogicae_cor.v1.library.abstract_manager_configurations import (
    AbstractManagerConfigurations,
)


class SingletonManagerConfigurations(
    AbstractManagerConfigurations,
):
    def __init__(self) -> None:
        super().__init__()
