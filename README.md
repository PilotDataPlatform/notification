# service_notification
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green?style=for-the-badge)](https://www.python.org/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pilotdataplatform/notification/ci/main?style=for-the-badge)](https://github.com/PilotDataPlatform/notification/actions/workflows/ci.yml)
[![codecov](https://img.shields.io/codecov/c/github/PilotDataPlatform/notification?style=for-the-badge)](https://codecov.io/gh/PilotDataPlatform/notification)
## About
Manages emails and system maintenance notifications.
### Built With
- Python
- FastAPI
## Getting Started

### Prerequisites
- [Poetry](https://python-poetry.org/) dependency manager.
- Vault connection credentials or custom-set environment variables.

### Installation
#### Using Docker
1. Run Docker compose with environment variables.

       PIP_USERNAME=[...] PIP_PASSWORD=[...] docker-compose up

2. Find service locally at `http://localhost:5065/`.

#### Without Docker
1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Configure access to internal package registry.

       poetry config http-basic.pilot ${PIP_USERNAME} ${PIP_PASSWORD}

3. Install dependencies.

       poetry install

4. Add environment variables into `.env`.
5. Run application.

       poetry run python run.py

6. Find service locally at `http://localhost:5065/`.

Example:

```
poetry install
poetry run python run.py
CONFIG_CENTER_ENABLED=true VAULT_URL=[...] VAULT_CRT=[...] VAULT_TOKEN=[...] poetry run python run.py
```

## Usage
Swagger API documentation can be found locally at `http://localhost:5065/v1/api-doc`.

