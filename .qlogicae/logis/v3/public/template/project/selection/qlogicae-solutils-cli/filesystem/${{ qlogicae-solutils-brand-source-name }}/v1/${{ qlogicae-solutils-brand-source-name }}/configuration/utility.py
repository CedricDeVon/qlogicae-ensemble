from typing import Any

exports: dict[str, dict[str, Any]] = {    
    "data": {
        "company-name": {
            "value": "${{ qlogicae-solutils-company-base-name }}"
        },
        "project-name": {
            "value": "${{ qlogicae-solutils-project-base-name }}"
        },
        "project-description": {
            "value": "${{ qlogicae-solutils-project-base-description }}"
        },
        "active-major-version-label": {
            "value": "${{ qlogicae-solutils-active-major-version-label }}"
        },
        "debug": {
            "is-enabled": {
                "value": True
            }
        },
    },
    "metadata": {

    },
}
