from typing import Any

DATA: dict[str, dict[str, Any]]= {
    "brand-name": {
        "name": "Brand Name",
        "value": "${{ qlogicae-logis-display-brand-name }}",
        "is-tabular": False,
    },
    "project-version": {
        "name": "Project Version",
        "value": "${{ qlogicae-logis-current-version-label }}",
        "is-tabular": True,
    },
    "project-description": {
        "name": "Description",
        "value": "${{ qlogicae-logis-base-description }}",
        "is-tabular": False,
    },
    "project-name": {
        "name": "Project Name",
        "value": "${{ qlogicae-logis-display-project-name }}",
        "is-tabular": True,
    },
    "company-name": {
        "name": "Company Name",
        "value": "${{ main-company-display-name }}",
        "is-tabular": True,
    },
    "workspace-name": {
        "name": "Workspace Name",
        "value": "${{ qlogicae-logis-base-brand-name }}",
        "is-tabular": False,
    },
    "author-name": {
        "name": "Author Name",
        "value": "${{ main-author-full-name }}",
        "is-tabular": True,
    },
    "author-email": {
        "name": "Author Email",
        "value": "${{ main-author-base-email }}",
        "is-tabular": True,
    },
    "repository-link": {
        "name": "Repository Link",
        "value": "${{ qlogicae-logis-base-repository-link }}",
        "is-tabular": True,
    },
    "repository-keywords": {
        "name": "Repository Keywords",
        "value": "${{ main-company-base-name }}, ${{ qlogicae-logis-base-project-name }}",
        "is-tabular": True,
    },
}

METADATA: dict[str, dict[str, Any]] = {    

}



