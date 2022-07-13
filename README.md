# Notification Service
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green?style=for-the-badge)](https://www.python.org/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/PilotDataPlatform/notification/CI/develop?style=for-the-badge)](https://github.com/PilotDataPlatform/notification/actions/workflows/ci.yml)
[![codecov](https://img.shields.io/codecov/c/github/PilotDataPlatform/notification?style=for-the-badge)](https://codecov.io/gh/PilotDataPlatform/notification)

Manages emails and system maintenance notifications.


## Built With

 - [FastAPI](https://fastapi.tiangolo.com): The async API framework for backend.
 - [Poetry](https://python-poetry.org/): Python package management.
 - [Docker](https://docker.com): Products that use OS-level virtualization to deliver software in packages called containers.
 - [Alembic](https://alembic.sqlalchemy.org/en/latest/): Lightweight database migration tool.


## Getting Started

### Prerequisites

1. Install Docker.

### Installation

1. Clone the project.
2. Run `docker-compose up`.

### Testing

```
poetry run pytest
```

### Migrations

Migrations should run automatically on `docker-compose up`. They can also be manually triggered:

```
docker compose run --rm alembic upgrade head
```

New migrations can be created with Alembic as well:

```
poetry install alembic
docker compose run --rm alembic revision -m "migration_name"
```

## Resources

Local URLs:
- API service: http://localhost:5065
- API documentation: http://localhost:5065/v1/api-doc
- pgAdmin: http://localhost:8750

pgAdmin's local config files have been committed to this repo for ease of development. Without the files, a connection between pgAdmin and Postgres will have to be manually established by the developer.

General resources:
- [API Document](https://pilotdataplatform.github.io/api-docs/) 
- [Helm Chart](https://github.com/PilotDataPlatform/helm-charts/)

## Contribution

You can contribute the project in following ways:

- Report a bug.
- Suggest a feature.
- Open a pull request for fixing issues or developing plugins.
