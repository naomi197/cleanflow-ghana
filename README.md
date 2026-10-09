# CleanFlow Ghana

A water-pollution reporting and prioritization API for Ghana.

CleanFlow Ghana is a FastAPI backend for communities and response teams who need to record pollution incidents and sort them by urgency. Each report gets a priority score from the pollutant type and a severity level from 1 to 5.

Developer: Alireza Sani · [alirezafazeli@live.com](mailto:alirezafazeli@live.com)

## Features

- REST API for creating and listing pollution reports
- Automatic priority score, normalized from 0 to 100
- Categories: `critical`, `high`, `medium`, and `low`
- Reports returned in descending priority order
- SQLite storage, SQLAlchemy, and Pydantic validation
- Pytest coverage for health, creation, validation, listing, and sorting
- A small Vite frontend in `cleanflow-ghana-frontend/`

## Technology

- Python 3.12
- FastAPI and Uvicorn
- SQLAlchemy and SQLite
- Pydantic
- Pytest

## Setup

```bash
git clone https://github.com/naomi197/cleanflow-ghana.git
cd cleanflow-ghana
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with `.\.venv\Scripts\Activate.ps1`.

The API is at http://127.0.0.1:8000. Interactive docs are at http://127.0.0.1:8000/docs.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Check that the API is running |
| POST | `/reports` | Create a report and assign its priority |
| GET | `/reports` | List reports by descending `priority_score` |
| GET | `/reports/{report_id}` | Read one report |

```json
{
  "location": "Accra drainage channel",
  "pollutant_type": "chemical",
  "severity": 5,
  "description": "Severe chemical discharge"
}
```

## Priority

The score combines pollutant type and severity, then maps to `critical`, `high`, `medium`, or `low`. Response teams can take the highest-scoring incidents first.

## Tests

```bash
python -m pytest tests -q
```

The suite covers the health check, report creation, invalid severity, listing, priority sorting, and a missing report.

## Project structure

```text
app/
├── models/
├── routers/
├── schemas/
├── services/
└── main.py
cleanflow-ghana-frontend/
tests/
```

## Related work

- [ClimaScope](https://github.com/naomi197/climascope) — live climate observatory for Android and the browser
- [Water Network Optimizer](https://github.com/naomi197/water-network-optimizer) — Hazen-Williams pipe sizing
- [TreeGrow](https://github.com/naomi197/treegrow-android) — Android app for virtual tree planting
- [Climate Assistant](https://github.com/naomi197/weather-climate-assistant) — Android weather and air-quality client

## Author

Alireza Sani — [naomi197](https://github.com/naomi197)
