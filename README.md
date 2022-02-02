# service_notification

## About
Manages emails and system maintenance notifications.
### Built With
- Python
- FastAPI
## Getting Started

### Prerequisites
- Dependencies as defined in `requirements.txt` and `internal_requirements.txt`.
- Vault connection credentials or custom-set environment variables.

### Installation
1. Install dependencies from `requirements.txt` and `internal_requirements.txt`. Token username and password are required for internal packages.
2. Supply environment variables.
3. Run application from `run.py`.
4. Find service locally at `http://localhost:5065/`.

Example:
```
python3 -m venv venv
source venv/bin/activate
PIP_USERNAME=[...] PIP_PASSWORD=[...] pip install -r requirements.txt
CONFIG_CENTER_ENABLED=true VAULT_URL=[...] VAULT_CRT=[...] VAULT_TOKEN=[...] python run.py
```

## Usage
Swagger API documentation can be found locally at `http://localhost:5065/v1/api-doc`.
